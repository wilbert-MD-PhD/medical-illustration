# MIT License; see ../LICENSE-CODE.
"""Conservative source checks, not a JavaScript sandbox or full static analyzer."""
import hashlib,re,ast
from pathlib import Path

def scrub(source):
    # Retain newlines for diagnostics while hiding literals and comments.
    token=re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
    return token.sub(lambda m: ''.join('\n' if x=='\n' else ' ' for x in m.group()),source)

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
        found=list(literal.finditer(source))
        for m in found:
            value=ast.literal_eval(m.group(1));child=Path(value)
            if not child.is_absolute():
                result['errors'].append({'path':str(p),'code':'relative-code-path','message':'Use an absolute literal path for JSX dependencies.'});continue
            if not child.is_file():result['errors'].append({'path':str(child),'code':'missing-dependency','message':'JSX dependency does not exist.'})
            else:visit(child)
        if len(re.findall(r'\$\.evalFile\s*\(',clean))>len(found):result['warnings'].append({'path':str(p),'message':'Computed evalFile dependency cannot be inspected; inspect it explicitly before execution.'})
    visit(script)
    return result
