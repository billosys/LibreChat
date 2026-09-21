'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const [root,compiler,priorHandle,output]=process.argv.slice(2),ts=require(compiler);
const {beginTurnWrite}=require(priorHandle),sources=[];
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
function read(file){const text=fs.readFileSync(path.join(root,file),'utf8');sources.push({path:file,sha256:hash(path.join(root,file))});return {text,ast:ts.createSourceFile(file,text,ts.ScriptTarget.Latest,true)};}
const controlledProcess={env:{TENANT_ISOLATION_STRICT:'true'}};
function compile(text,requireFn=()=>{throw Error('Unexpected import');},extra={}){const o=ts.transpileModule(text,{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022},reportDiagnostics:true});assert.equal(o.diagnostics.length,0);const m={exports:{}};vm.runInNewContext(o.outputText,{module:m,exports:m.exports,require:requireFn,process:controlledProcess,...extra},{timeout:5000});return m.exports;}
const tenantSource=read('packages/data-schemas/src/config/tenantContext.ts');
const tenant=compile(tenantSource.text,n=>{assert.equal(n,'async_hooks');return require('node:async_hooks');});
const policySource=read('packages/data-schemas/src/tenant/policy.ts');
const logger={warn(){},error(){},info(){}};
const policy=compile(policySource.text,n=>n==='~/config/tenantContext'?tenant:{default:logger,...logger});
const middlewareSource=read('packages/api/src/middleware/messageValidation.ts');
const middleware=compile(middlewareSource.text);
const routeSource=read('api/server/routes/messages.js');
let reload;
for(const s of routeSource.ast.statements){if(!ts.isExpressionStatement(s)||!ts.isCallExpression(s.expression))continue;const c=s.expression;if(c.expression.getText(routeSource.ast)==='router.get'&&c.arguments[0]?.text==='/:conversationId')reload=c.arguments[2].getText(routeSource.ast);}
assert(reload);
const messageSource=read('packages/data-schemas/src/methods/message.ts');
let saveFunction,uuid,projection;
function visit(n){if(ts.isFunctionDeclaration(n)&&n.name?.text==='saveMessage')saveFunction=n.getText(messageSource.ast);if(ts.isVariableDeclaration(n)&&n.name.getText(messageSource.ast)==='UUID_REGEX')uuid=n.initializer.getText(messageSource.ast);if(ts.isVariableDeclaration(n)&&n.name.getText(messageSource.ast)==='CLIENT_MESSAGE_SELECT')projection=n.initializer.getText(messageSource.ast);ts.forEachChild(n,visit);}visit(messageSource.ast);assert(saveFunction&&uuid&&projection);
const select=vm.runInNewContext(projection,{}, {timeout:1000});
const canon=x=>JSON.parse(JSON.stringify(x));
const specs=[
 {name:'stored'}, {name:'missing',convo:null}, {name:'foreign-owner',convo:{user:'u2'}}, {name:'child',convo:{user:'u1',subagentThread:{}}},
 {name:'new',id:'new'}, {name:'mismatch',body:{conversationId:'other'}}, {name:'message-error',messageError:true}, {name:'ownership-error',ownershipError:true},
 {name:'active-owner',convo:null,job:{status:'running',metadata:{userId:'u1',tenantId:'t1'}}},
 {name:'active-other-owner',convo:null,job:{status:'running',metadata:{userId:'u2',tenantId:'t1'}}},
 {name:'active-other-tenant',convo:null,job:{status:'running',metadata:{userId:'u1',tenantId:'t2'}}},
 {name:'paused-live',convo:null,job:{status:'requires_action',metadata:{userId:'u1'}}},
 {name:'paused-stale',convo:null,job:{status:'requires_action',metadata:{userId:'u1'}},stale:true},
 {name:'by-id-no-active-exception',convo:null,messageId:'m1',job:{status:'running',metadata:{userId:'u1'}}},
 {name:'empty',messages:[]}, {name:'job-error',convo:null,jobError:true},
];
const defer=()=>{let resolve;const promise=new Promise(r=>{resolve=r;});return {promise,resolve};};
async function run(spec,candidate,mutant,gate){
 const trace=[],responses=[];
 const db={
  async getConvoOwnership(...args){trace.push({method:'ownership',args});if(gate)await gate.promise;if(spec.ownershipError)throw Error('ownership failed');return Object.hasOwn(spec,'convo')?spec.convo:{user:'u1'};},
  async getMessages(...args){trace.push({method:'messages',args});if(spec.messageError)throw Error('messages failed');return spec.messages??[{messageId:'m1',conversationId:'c1',text:'synthetic'}];},
 };
 const port={probeConversationAccess:(user,id)=>db.getConvoOwnership(user,id),readPublicMessages:({userId,conversationId})=>db.getMessages({conversationId,user:mutant==='wrong-owner'?'u2':userId},mutant==='no-projection'?undefined:select)};
 const validation=middleware.createMessageRequestMiddleware({getConvo:candidate?port.probeConversationAccess:db.getConvoOwnership,async getJob(id){trace.push({method:'job',args:[id]});if(spec.jobError)throw Error('job failed');return spec.job??null;},isPendingActionStale:()=>Boolean(spec.stale),logger});
 const req={method:'GET',params:{conversationId:spec.id??'c1',...(spec.messageId?{messageId:spec.messageId}:{})},body:spec.body??{},user:{id:'u1',tenantId:'t1'}};
 req.messageRequestValidation=validation.createMessageRequestValidation(req);
 const res={statusCode:200,status(code){this.statusCode=code;return this;},json(body){responses.push({status:this.statusCode,body,send:false});return this;},send(body){responses.push({status:this.statusCode,body,send:true});return this;}};
 let body=reload;if(candidate){const target='db.getMessages({ conversationId, user: req.user.id }, CLIENT_MESSAGE_SELECT)';assert.equal(body.split(target).length,2);body=body.replace(target,'port.readPublicMessages({ conversationId, userId: req.user.id })');}
 const handler=vm.runInNewContext(`(${body})`,{db,port,CLIENT_MESSAGE_SELECT:select,logger,sendValidationResponse:validation.sendValidationResponse},{timeout:1000});
 const pending=handler(req,res);
 if(gate){await Promise.resolve();await Promise.resolve();assert.equal(responses.length,0);gate.resolve();}
 await pending;
 return canon({trace,responses,shouldFetchMessages:req.messageRequestValidation.shouldFetchMessages});
}
const result={sourceHead:execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),node:process.version,compiler:{path:compiler,version:ts.version,sha256:hash(compiler)},sources,experimentSha256:hash(__filename),priorHandle:{path:priorHandle,sha256:hash(priorHandle)},readCases:[],gateCases:[],preflightCases:[],negativeControls:[],success:false};
(async()=>{try{
 const expectedStatuses=[200,404,403,404,200,400,500,500,200,404,404,200,404,404,200,404];
 for(const [index,spec] of specs.entries()){const reference=await run(spec,false),candidate=await run(spec,true);const passed=JSON.stringify(reference)===JSON.stringify(candidate)&&reference.responses.length===1&&reference.responses[0].status===expectedStatuses[index];result.readCases.push({name:spec.name,expectedStatus:expectedStatuses[index],passed,reference,candidate});assert(passed,spec.name);}
 for(const messageError of [false,true]){const entry=await run({convo:null,messageError},true,undefined,defer());assert.equal(entry.responses[0].status,404);result.gateCases.push({messageError,passed:true,...entry});}
 for(const mutant of ['wrong-owner','no-projection']){const ref=await run(specs[0],false),actual=await run(specs[0],true,mutant);const detected=JSON.stringify(ref)!==JSON.stringify(actual);assert(detected);result.negativeControls.push({name:mutant,detected,actual});}
 let accesses=0;
 const mongoose={get models(){accesses++;throw Error('Unexpected model access');}};
 const legacy=compile(`const UUID_REGEX = ${uuid};\n${saveFunction}\nexports.saveMessage=saveMessage;`,undefined,{mongoose,logger}).saveMessage;
 const inputCases=[{name:'missing-owner',ctx:{userId:''},fields:{conversationId:'bad'}},{name:'missing-conversation',ctx:{userId:'u1'},fields:{}},{name:'malformed-conversation',ctx:{userId:'u1'},fields:{conversationId:'bad'}}];
 async function observe(fn){try{return {returned:await fn()??'<undefined>'};}catch(e){return {error:e.message};}}
 for(const spec of inputCases){const direct=await observe(()=>legacy(spec.ctx,spec.fields,{}));let h;
  const deferred=await observe(async()=>{h=beginTurnWrite({saveMessage:legacy},spec.ctx,policy.currentTenantScope);try{return await h.saveMessage(spec.ctx,spec.fields,{});}finally{h.release();}});
  const eager=await observe(async()=>{const x=beginTurnWrite({saveMessage:legacy},spec.ctx,policy.resolveTenantScope);try{return await x.saveMessage(spec.ctx,spec.fields,{});}finally{x.release();}});
  const passed=JSON.stringify(direct)===JSON.stringify(deferred);assert(passed);assert.notDeepEqual(direct,eager);result.preflightCases.push({name:spec.name,direct,deferred,eager,passed});
 }
 assert.equal(accesses,0);result.modelAccesses=accesses;
 result.negativeControls.push({name:'eager-strict-scope',detected:result.preflightCases.every(c=>JSON.stringify(c.direct)!==JSON.stringify(c.eager))});
 result.success=true;
}catch(e){result.error={message:e.message,stack:e.stack};process.exitCode=1;}finally{fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({success:result.success,readCases:result.readCases.length,gateCases:result.gateCases.length,preflightCases:result.preflightCases,negativeControls:result.negativeControls.map(({name,detected})=>({name,detected})),error:result.error},null,2));}})();
