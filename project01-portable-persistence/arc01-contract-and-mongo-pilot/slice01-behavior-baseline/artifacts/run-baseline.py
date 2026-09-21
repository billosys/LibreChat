import datetime, hashlib, json, os, pathlib, subprocess, sys
root = pathlib.Path('/Users/oubiwann/lab/billosys/LibreChat')
out = pathlib.Path('/tmp/guildhall-slice01-20260920')
out.mkdir(exist_ok=True)
sets = {
 '01-data-schemas': ('packages/data-schemas', ['src/tenant/conformance.mongoose.spec.ts','src/methods/message.spec.ts','src/methods/conversation.spec.ts','src/methods/convoStructure.spec.ts','src/methods/message.traces.spec.ts']),
 '02-save-orchestration': ('packages/api', ['src/conversations/save.spec.ts']),
 '03-import': ('api', ['server/utils/import/importers.spec.js','server/utils/import/importers-timestamp.spec.js','server/utils/import/importConversations.database.spec.js']),
 '04-client-read': ('api', ['app/clients/specs/BaseClient.test.js','server/routes/__tests__/messages-get.spec.js','server/routes/__tests__/messages-get-real-validation.spec.js']),
}
name = sys.argv[1]
workspace, tests = sets[name]
dest = out / name
dest.mkdir(exist_ok=False)
overrides = {'CI':'true','NODE_ENV':'test','MONGO_URI':'mongodb://127.0.0.1:1/guildhall_slice01_forbidden_live','MONGOMS_SYSTEM_BINARY':str(root/'node_modules/.cache/mongodb-memory-server/mongod-arm64-darwin-8.2.1'),'MONGOMS_VERSION':'8.2.1','MONGOMS_RUNTIME_DOWNLOAD':'false','JEST_JUNIT_OUTPUT_DIR':str(dest),'JEST_JUNIT_OUTPUT_NAME':'junit.xml','LOG_TO_FILE':'false'}
cmd = ['/Users/oubiwann/.local/bin/node',str(root/'node_modules/jest/bin/jest.js'),'--runInBand','--watch=false','--coverage=false','--runTestsByPath',*tests,'--json','--outputFile',str(dest/'jest.json'),'--cacheDirectory',str(out/'jest-cache')]
if workspace == 'api':
 overrides.update(USE_REDIS='false',USE_REDIS_STREAMS='false',MEILI_HOST='',MEILI_MASTER_KEY='')
 cmd += ['--setupFilesAfterEnv', '/tmp/guildhall-slice01-mongo-guard.cjs']
record = {'name':name,'cwd':str(root/workspace),'argv':cmd,'environment_overrides':overrides,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'node_version':subprocess.check_output([cmd[0],'--version'],text=True).strip()}
(dest/'attempt.json').write_text(json.dumps(record,indent=2)+'\n')
with (dest/'output.log').open('w') as log:
 result = subprocess.run(cmd,cwd=root/workspace,env={**os.environ,**overrides},stdout=log,stderr=subprocess.STDOUT)
record.update(exit_code=result.returncode,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
(dest/'attempt.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
if (dest/'jest.json').exists():
 data=json.loads((dest/'jest.json').read_text())
 print(json.dumps({k:v for k,v in data.items() if k.startswith('num') or k=='success'},indent=2))
else:
 print((dest/'output.log').read_text()[-6000:])
sys.exit(result.returncode)
