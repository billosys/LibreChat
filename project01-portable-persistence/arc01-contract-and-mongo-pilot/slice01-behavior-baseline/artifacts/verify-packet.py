import collections, hashlib, json, pathlib, re, subprocess
source=pathlib.Path('/Users/oubiwann/lab/billosys/LibreChat')
planning=source/'.worktrees/planning'; project=planning/'project01-portable-persistence'
slice=project/'arc01-contract-and-mongo-pilot/slice01-behavior-baseline'; artifacts=slice/'artifacts'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
assert head=='ba44443fdb232bbe6d4977e2619774b5a72586ac'
assert subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all'],cwd=source,text=True)==''
fingerprints={}
for name in ['source-fingerprints.json','dist-fingerprints.json']:
 records=json.loads((artifacts/name).read_text())
 for r in records:
  content=(source/r['path']).read_bytes(); assert hashlib.sha256(content).hexdigest()==r['sha256'],r['path']
 fingerprints[name]=len(records)
tests=suites=0; perrun={}
for run in sorted((artifacts/'runs').iterdir()):
 meta=json.loads((run/'attempt.json').read_text()); results=json.loads((run/'jest.json').read_text())
 assert meta['source_head']==head and meta['exit_code']==0 and results['success']
 assert results['numTotalTests']==results['numPassedTests']
 assert results['numTotalTestSuites']==results['numPassedTestSuites']
 for key in ['numFailedTests','numPendingTests','numTodoTests','numRuntimeErrorTestSuites','numFailedTestSuites']: assert results[key]==0
 assertions=[a for suite in results['testResults'] for a in suite['assertionResults']]
 assert len(assertions)==results['numTotalTests'] and all(a['status']=='passed' for a in assertions)
 tests+=len(assertions); suites+=len(results['testResults']); perrun[run.name]={'tests':len(assertions),'suites':len(results['testResults'])}
assert (tests,suites)==(641,12)
assert len((artifacts/'assertions.tsv').read_text().splitlines())==642
refs=json.loads((artifacts/'symbol-references.json').read_text()); calls=json.loads((artifacts/'callsite-candidates.json').read_text())
assert (len(refs),len({x['path'] for x in refs}),len(calls),len({x['path'] for x in calls}))==(305,60,155,43)
ledger=(slice/'ledger.md').read_text(); close=(slice/'closing-report.md').read_text()
ids=re.findall(r'^\| (S\d\d) \|',ledger,re.M); assert ids==['S01','S02','S03','S04','S05','S06','S07']
assert re.findall(r'^\| (S\d\d) \|',close,re.M)==ids
assert all(line.split('|')[6].strip()=='open' for line in ledger.splitlines() if re.match(r'^\| S\d\d \|',line))
assert len(re.findall(r'^\| B\d\d \|',(artifacts/'behavior-matrix.md').read_text(),re.M))==22
assert len(re.findall(r'^\| D\d\d \|',(artifacts/'design-inputs.md').read_text(),re.M))==9
for forbidden in ['cc-prompt.md','cdc-verification.md','crc-verification.md']: assert not (slice/forbidden).exists()
subprocess.run(['git','diff','--check'],cwd=planning,check=True)
# First-class reports are outside this supporting-artifact inventory.
names={str(p.relative_to(artifacts)) for p in artifacts.rglob('*') if p.is_file()}
names.update(['artifact-inventory.txt','validation.json','SHA256SUMS'])
(artifacts/'artifact-inventory.txt').write_text('\n'.join(sorted(names))+'\n')
# Materialize verification output before checking all links, then fill in final counts.
(artifacts/'validation.json').write_text('{}\n')
(artifacts/'SHA256SUMS').write_text('')
checked=0
docs=list(slice.rglob('*.md'))+[project/'project-plan.md',project/'ledger.md',slice.parent/'arc-plan.md',slice.parent/'ledger.md']
for doc in docs:
 for target in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  if '://' in target or target.startswith('#'): continue
  target=target.split('#')[0]
  assert (doc.parent/target).exists(),(doc,target)
  checked+=1
report={'evidence_strength':'self-checked / attested','source_head':head,'source_clean':True,'fingerprints_rechecked':fingerprints,'attempts':perrun,'passed_tests':tests,'passed_suites':suites,'ledger_rows':ids,'ledger_status':'all open for independent acceptance','behavior_rows':22,'decision_rows':9,'markdown_targets_checked':checked,'git_diff_check':'passed','new_application_source_files':0,'forbidden_fake_contributor_records':0}
(artifacts/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
paths=sorted(p for p in artifacts.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(artifacts))+'\n' for p in paths)
(artifacts/'SHA256SUMS').write_text(manifest)
assert set((artifacts/'artifact-inventory.txt').read_text().splitlines())=={str(p.relative_to(artifacts)) for p in artifacts.rglob('*') if p.is_file()}
print(json.dumps(report,indent=2)); print('Artifact hashes:',len(paths))
