#!/usr/bin/env python3
"""Check explicit mechanism-graph record consistency, not biological truth. MIT."""
import argparse
import json
from pathlib import Path

RELATIONS = {'activation','inhibition','association','transport','process','localization'}

def check(data):
    errors=[]
    if not isinstance(data,dict): return ['root must be an object']
    groups={}
    for key in ('nodes','edges','sources'):
        items=data.get(key)
        if not isinstance(items,list):
            errors.append(f'{key}: expected an array');items=[]
        groups[key]={}
        for i,item in enumerate(items):
            if not isinstance(item,dict): errors.append(f'{key}[{i}]: expected object');continue
            ident=item.get('id')
            if not isinstance(ident,str) or not ident.strip():errors.append(f'{key}[{i}]: missing ID');continue
            if ident in groups[key]: errors.append(f'{key}: duplicate ID {ident}')
            groups[key][ident]=item
    for ident,n in groups['nodes'].items():
        for k in ('label','compartment'):
            if not isinstance(n.get(k),str) or not n[k].strip():errors.append(f'{ident}: missing {k}')
    for ident,s in groups['sources'].items():
        for k in ('citation','checked_scope'):
            if not isinstance(s.get(k),str) or not s[k].strip():errors.append(f'{ident}: missing {k}')
    for ident,e in groups['edges'].items():
        for k in ('source','target'):
            if not isinstance(e.get(k),str) or e[k] not in groups['nodes']: errors.append(f'{ident}: unknown {k}')
        refs=e.get('source_ids')
        if not isinstance(refs,list) or not refs: errors.append(f'{ident}: no evidence/proposal source')
        elif any(not isinstance(x,str) or x not in groups['sources'] for x in refs):errors.append(f'{ident}: unknown source ID')
        r=e.get('relation');status=e.get('evidence_status');style=e.get('line_style')
        if r not in RELATIONS:errors.append(f'{ident}: invalid relation')
        if status not in ('established','observed','hypothesis'):errors.append(f'{ident}: invalid evidence status')
        if e.get('directness') not in ('direct','indirect','unspecified'):errors.append(f'{ident}: invalid directness')
        if style not in ('solid','dashed','dotted'):errors.append(f'{ident}: invalid line style')
        if status=='hypothesis' and style!='dashed':errors.append(f'{ident}: hypothesis must be dashed in this schema')
        expected='bar' if r=='inhibition' else 'none' if r in ('association','localization') else 'arrow'
        if e.get('arrowhead')!=expected:errors.append(f'{ident}: {r} requires {expected} endpoint')
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('graph',type=Path);a=p.parse_args()
    try: errors=check(json.loads(a.graph.read_text(encoding='utf-8')))
    except (OSError,ValueError,TypeError) as exc:errors=[str(exc)]
    print(json.dumps({'errors':errors,'scope':'Record consistency only; literature, anatomy, rendering and human approval are not checked.'},ensure_ascii=False,indent=2))
    return bool(errors)
if __name__=='__main__':raise SystemExit(main())
