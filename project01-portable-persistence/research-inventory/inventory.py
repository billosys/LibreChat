import subprocess, re, pathlib, collections, json
root=pathlib.Path('/Users/oubiwann/lab/billosys/LibreChat')
sha='ba44443fdb232bbe6d4977e2619774b5a72586ac'
roots=['api/','packages/api/src/','packages/data-schemas/src/','packages/data-provider/src/','client/src/']
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',sha],cwd=root,text=True).splitlines()
excluded={'node_modules','dist','generated','__generated__','__tests__','__mocks__','test','tests','spec','specs'}
def production(p):
 return any(p.startswith(r) for r in roots) and pathlib.Path(p).suffix in {'.js','.jsx','.ts','.tsx','.mjs','.cjs','.mts','.cts'} and not (set(p.split('/'))&excluded) and not re.search(r'\.(?:test|spec)\.',p) and not re.search(r'(?:^|/)(?:test[-.]|jest[.-])',p)
patterns={
 'static_or_require': re.compile(r'''\b(?:from\s+|require\s*\(\s*|import\s+)["'](mongoose|mongodb)["']'''),
 'inline_import_reference': re.compile(r'''\bimport\s*\(\s*["'](mongoose|mongodb)["']'''),
}
counts={}
allmatches={k:[] for k in patterns}
for p in paths:
 if not production(p): continue
 content=subprocess.check_output(['git','show',sha+':'+p],cwd=root,text=True)
 for kind, pattern in patterns.items():
  for n,line in enumerate(content.splitlines(),1):
   for match in pattern.finditer(line): allmatches[kind].append((p,n,match[1],line.strip()))
for kind,matches in allmatches.items():
 pathlib.Path('/tmp/guildhall-librechat-inventory/'+kind+'.txt').write_text('\n'.join(f'{p}:{n}:{mod}:{line}' for p,n,mod,line in matches)+'\n')
 counts[kind]={r:{mod:len({p for p,n,m,l in matches if p.startswith(r) and m==mod}) for mod in ['mongoose','mongodb']} for r in roots}
 counts[kind]['distinct_files']=len({p for p,n,m,l in matches})
print(json.dumps(counts,indent=2))
print('production files',sum(production(p) for p in paths))
