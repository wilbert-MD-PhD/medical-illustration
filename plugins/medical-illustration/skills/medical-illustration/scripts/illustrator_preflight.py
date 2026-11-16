# MIT License; see ../LICENSE-CODE.
"""Conservative source checks, not a JavaScript sandbox or full static analyzer."""
import hashlib,re
from pathlib import Path

def js_string(literal):
    """Decode ES3 string escapes without applying Python's escape semantics."""
    value = literal[1:-1]
    result = []
    i = 0
    simple = {'b':'\b', 'f':'\f', 'n':'\n', 'r':'\r', 't':'\t', 'v':'\v'}
    while i < len(value):
        c = value[i]; i += 1
        if c != '\\':
            result.append(c); continue
        if i >= len(value): raise ValueError('Incomplete JavaScript string escape')
        c = value[i]; i += 1
        if c in 'xu':
            n = 2 if c == 'x' else 4
            digits = value[i:i+n]
            if len(digits) != n or not re.fullmatch(r'[0-9a-fA-F]+', digits):
                raise ValueError('Invalid JavaScript hexadecimal escape')
            result.append(chr(int(digits, 16))); i += n
        elif c in '01234567':
            digits = c
            limit = 3 if c in '0123' else 2
            while len(digits) < limit and i < len(value) and value[i] in '01234567':
                digits += value[i]; i += 1
            result.append(chr(int(digits, 8)))
        else:
            result.append(simple.get(c, c))
    return ''.join(result).encode('utf-16', 'surrogatepass').decode('utf-16', 'surrogatepass')

def scrub(source, keep_strings=False):
    """Mask comments, strings and regex literals while preserving positions.

    ES3 uses the same slash for division and regex. Where a regex following an
    expression cannot be distinguished safely, reject it instead of silently
    hiding later code. This is deliberately not a complete JavaScript parser.
    """
    out = list(source)
    i, regex_allowed = 0, True

    def mask(start, end):
        for n in range(start, end):
            if source[n] not in '\r\n': out[n] = ' '

    def regex_end(start):
        j, char_class = start + 1, False
        while j < len(source) and source[j] not in '\r\n':
            c = source[j]
            if c == '\\':
                j += 2
                continue
            if c == '[': char_class = True
            elif c == ']': char_class = False
            elif c == '/' and not char_class:
                return j + 1
            j += 1
        return None

    while i < len(source):
        c = source[i]
        if c.isspace():
            i += 1
        elif source.startswith('//', i):
            end = source.find('\n', i)
            end = len(source) if end < 0 else end
            mask(i, end); i = end
        elif source.startswith('/*', i):
            end = source.find('*/', i + 2)
            if end < 0: raise ValueError('Unterminated JavaScript comment')
            end += 2; mask(i, end); i = end
        elif c in ('"', "'"):
            start = i; i += 1
            while i < len(source) and source[i] not in '\r\n':
                if source[i] == '\\': i += 2
                elif source[i] == c:
                    i += 1; break
                else: i += 1
            else: raise ValueError('Unterminated JavaScript string')
            if not keep_strings: mask(start, i)
            regex_allowed = False
        elif c == '/':
            end = regex_end(i)
            if regex_allowed and end is not None:
                mask(i, end); i = end
                while i < len(source) and source[i].isalpha(): i += 1
                regex_allowed = False
            else:
                # A slash after an expression might begin a regex statement
                # (e.g. after `if (...)`). Quotes/escapes could conceal code.
                if end is not None and any(x in source[i+1:end-1] for x in ('"', "'", '\\')):
                    raise ValueError('Ambiguous division/regex literal; rewrite or inspect manually')
                i += 1; regex_allowed = True
        elif c.isalpha() or c in '_$':
            match = re.match(r'[\w$]+', source[i:])
            word = match.group(); i += len(word)
            regex_allowed = word in ('return', 'throw', 'case', 'delete', 'void', 'typeof', 'new', 'in', 'instanceof', 'else', 'do')
        elif c.isdigit():
            match = re.match(r'[\w.]+', source[i:])
            i += len(match.group()); regex_allowed = False
        elif source[i:i+2] in ('++', '--'):
            # Prefix keeps expecting an expression; postfix still ends one.
            i += 2
        else:
            i += 1
            regex_allowed = c not in ')]}'
    return ''.join(out)

RULES=[
 ('unmanaged-open',r'\bapp\s*\.\s*open\s*\(', 'Use session.open(path, mode).'),
 ('unmanaged-create',r'\bapp\s*\.\s*documents\s*\.\s*add\s*\(', 'Use session.create(...).'),
 ('direct-document-close',r'\.\s*close\s*\(\s*SaveOptions\b', 'Use session.close(doc); clear old references.'),
 ('quit-application',r'\bapp\s*\.\s*quit\s*\(', 'Keep Illustrator running.'),
 ('active-document',r'\bapp\s*\.\s*activeDocument\b', 'Use the explicit owned document reference.'),
]

def inspect_script(script):
    result={'files':[],'errors':[],'warnings':[]};seen=set()
    def visit(p):
        p=Path(p).resolve()
        if p in seen:return
        seen.add(p)
        source=p.read_text(encoding='utf-8')
        result['files'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        try:
            clean=scrub(source)
            with_strings=scrub(source, keep_strings=True)
        except ValueError as exc:
            result['errors'].append({'path':str(p),'code':'unrecognized-syntax','message':str(exc)})
            return
        for code,pattern,message in RULES:
            for m in re.finditer(pattern,clean):result['errors'].append({'path':str(p),'line':clean[:m.start()].count('\n')+1,'code':code,'message':message})
        for pattern,message in [(r'\.characters\b','Per-character DOM access: restrict to a diagnosed text defect.'),(r'\.embed\s*\(','embed removes the placed item; prefer linked construction.'),(r'\.createOutline\s*\(','createOutline removes its source; never read the old reference.')]:
            if re.search(pattern,clean):result['warnings'].append({'path':str(p),'message':message})
        literal=re.compile(r'\$\.evalFile\s*\(\s*(?:new\s+)?File\s*\(\s*((?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'))\s*\)\s*\)')
        include=re.compile(r'^[ \t]*#include[ \t]+((?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'))', re.M)
        # Preserve argument literals and offsets, but match only actual code.
        # Comments between call arguments become whitespace; examples inside
        # comments or other strings cannot create dependencies or hide warnings.
        found=[m for m in literal.finditer(with_strings)
               if clean[m.start():m.start()+2] == '$.']
        includes=[m for m in include.finditer(with_strings)
                  if re.match(r'[ \t]*#include\b', clean[m.start():])]
        for m in found + includes:
            value=js_string(m.group(1));child=Path(value)
            if not child.is_absolute():
                result['errors'].append({'path':str(p),'code':'relative-code-path','message':'Use an absolute literal path for JSX dependencies.'});continue
            if not child.is_file():result['errors'].append({'path':str(child),'code':'missing-dependency','message':'JSX dependency does not exist.'})
            else:visit(child)
        if len(re.findall(r'\$\.evalFile\s*\(',clean))>len(found):result['warnings'].append({'path':str(p),'message':'Computed evalFile dependency cannot be inspected; inspect it explicitly before execution.'})
        if len(re.findall(r'^[ \t]*#include\b', clean, re.M))>len(includes):result['warnings'].append({'path':str(p),'message':'Unrecognized include dependency cannot be inspected; inspect it explicitly before execution.'})
    visit(script)
    return result
