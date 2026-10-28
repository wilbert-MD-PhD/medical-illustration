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
    # Retain offsets/newlines; optionally keep literals for argument parsing.
    token=re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
    def mask(match):
        value = match.group()
        if keep_strings and value[0] in ('"', "'"):
            return value
        return ''.join('\n' if x=='\n' else ' ' for x in value)
    return token.sub(mask, source)

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
        source=p.read_text(encoding='utf-8');clean=scrub(source)
        result['files'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        for code,pattern,message in RULES:
            for m in re.finditer(pattern,clean):result['errors'].append({'path':str(p),'line':clean[:m.start()].count('\n')+1,'code':code,'message':message})
        for pattern,message in [(r'\.characters\b','Per-character DOM access: restrict to a diagnosed text defect.'),(r'\.embed\s*\(','embed removes the placed item; prefer linked construction.'),(r'\.createOutline\s*\(','createOutline removes its source; never read the old reference.')]:
            if re.search(pattern,clean):result['warnings'].append({'path':str(p),'message':message})
        literal=re.compile(r'\$\.evalFile\s*\(\s*File\s*\(\s*((?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'))\s*\)\s*\)')
        # Preserve argument literals and offsets, but match only actual code.
        # Comments between call arguments become whitespace; examples inside
        # comments or other strings cannot create dependencies or hide warnings.
        found=[m for m in literal.finditer(scrub(source, keep_strings=True))
               if clean[m.start():m.start()+2] == '$.']
        for m in found:
            value=js_string(m.group(1));child=Path(value)
            if not child.is_absolute():
                result['errors'].append({'path':str(p),'code':'relative-code-path','message':'Use an absolute literal path for JSX dependencies.'});continue
            if not child.is_file():result['errors'].append({'path':str(child),'code':'missing-dependency','message':'JSX dependency does not exist.'})
            else:visit(child)
        if len(re.findall(r'\$\.evalFile\s*\(',clean))>len(found):result['warnings'].append({'path':str(p),'message':'Computed evalFile dependency cannot be inspected; inspect it explicitly before execution.'})
    visit(script)
    return result
