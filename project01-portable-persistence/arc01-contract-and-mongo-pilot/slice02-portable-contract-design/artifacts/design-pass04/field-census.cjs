'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const [root,compiler,output]=process.argv.slice(2),ts=require(compiler);
const sources=[];
function read(name){const bytes=fs.readFileSync(path.join(root,name),'utf8');sources.push({path:name,sha256:crypto.createHash('sha256').update(bytes).digest('hex')});return ts.createSourceFile(name,bytes,ts.ScriptTarget.Latest,true);}
function variable(ast,name){for(const s of ast.statements)if(ts.isVariableStatement(s))for(const d of s.declarationList.declarations)if(d.name.getText(ast)===name)return d.initializer;throw new Error(name);}
const defaults=read('packages/data-schemas/src/schema/defaults.ts');
const preset=variable(defaults,'conversationPreset');assert(ts.isObjectLiteralExpression(preset));
function properties(ast,node){assert(ts.isObjectLiteralExpression(node));const fields=new Map(),overrides=[];
 for(const prop of node.properties){if(ts.isSpreadAssignment(prop)){assert.equal(prop.expression.getText(ast),'conversationPreset');for(const f of properties(defaults,preset).fields)fields.set(f.name,f);continue;}
 assert(ts.isPropertyAssignment(prop));const name=prop.name.getText(ast).replace(/^['"]|['"]$/g,'');
 if(fields.has(name))overrides.push(name);
 const flags={};if(ts.isObjectLiteralExpression(prop.initializer))for(const p of prop.initializer.properties)if(ts.isPropertyAssignment(p)&&['default','select','required','type'].includes(p.name.getText(ast)))flags[p.name.getText(ast)]=p.initializer.getText(ast);
 fields.set(name,{name,file:ast.fileName,line:ast.getLineAndCharacterOfPosition(prop.getStart(ast)).line+1,definition:prop.initializer.getText(ast),flags});}
 return {fields:[...fields.values()],overrides};}
const records=[];
for(const [schemaName,typeName,stem] of [['messageSchema','IMessage','message'],['convoSchema','IConversation','convo']]){
 const ast=read(`packages/data-schemas/src/schema/${stem}.ts`),decl=variable(ast,schemaName);assert(ts.isNewExpression(decl));assert.equal(decl.expression.getText(ast),'Schema');
 const schema=properties(ast,decl.arguments[0]);
 const typeAst=read(`packages/data-schemas/src/types/${stem}.ts`),type=typeAst.statements.find(n=>ts.isInterfaceDeclaration(n)&&n.name.text===typeName);assert(type);
 const members=type.members.map(p=>{assert(ts.isPropertySignature(p));return {name:p.name.getText(typeAst),optional:Boolean(p.questionToken),type:p.type.getText(typeAst),line:typeAst.getLineAndCharacterOfPosition(p.getStart(typeAst)).line+1};});
 const schemaKeys=new Set(schema.fields.map(f=>f.name)),typeKeys=new Set(members.map(m=>m.name));
 records.push({schemaName,typeName,...schema,options:decl.arguments[1].getText(ast),members,schemaOnly:[...schemaKeys].filter(k=>!typeKeys.has(k)),interfaceOnly:[...typeKeys].filter(k=>!schemaKeys.has(k)),hidden:schema.fields.filter(f=>f.flags.select==='false').map(f=>f.name)});
}
const result={scope:'Source AST top-level schema declarations plus expanded conversationPreset; not runtime schema, inherited Document fields, plugin fields, nested codec or consumer census',sources,records};
fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(records.map(r=>({schema:r.schemaName,fields:r.fields.length,interfaceFields:r.members.length,overrides:r.overrides,schemaOnly:r.schemaOnly,interfaceOnly:r.interfaceOnly,hidden:r.hidden})),null,2));
