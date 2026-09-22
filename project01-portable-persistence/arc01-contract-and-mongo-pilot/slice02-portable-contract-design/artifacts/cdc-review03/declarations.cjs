'use strict';
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const [root, compiler] = process.argv.slice(2);
const ts = require(compiler);
const requests = [
 ['packages/data-provider/src/types/agents.ts', 'ToolCall'],
 ['packages/data-provider/src/types/files.ts', 'TFile'],
 ['packages/data-provider/src/types/content.ts', 'SummaryContentPart'],
 ['packages/data-provider/src/types/content.ts', 'TMessageContentParts'],
 ['packages/data-provider/src/filters.ts', 'userSubmittedMessageFieldPathSchema'],
 ['packages/data-provider/src/schemas.ts', 'tExampleSchema'],
 ['packages/data-provider/src/schemas.ts', 'subagentThreadLineageSchema'],
 ['packages/data-provider/src/schemas.ts', 'TMessage'],
 ['packages/data-provider/src/schemas.ts', 'TAttachment'],
 ['packages/data-provider/src/schemas.ts', 'tMessageSchema'],
 ['packages/data-schemas/src/methods/message.ts', 'CLIENT_MESSAGE_SELECT'],
];
const declarations = [];
for (const [file, symbol] of requests) {
 const source = ts.createSourceFile(file, fs.readFileSync(path.join(root, file), 'utf8'), ts.ScriptTarget.Latest, true);
 const matches = [];
 function visit(node) {
  if ((ts.isTypeAliasDeclaration(node) || ts.isVariableDeclaration(node)) && node.name.getText(source) === symbol) matches.push(node);
  ts.forEachChild(node, visit);
 }
 visit(source);
 assert.equal(matches.length, 1, `${file}:${symbol} must identify one declaration`);
 const node = matches[0];
 const properties = [];
 function members(current) {
  if (ts.isPropertySignature(current)) properties.push({name:current.name.getText(source), type:current.type?.getText(source) ?? null, optional:!!current.questionToken, line:source.getLineAndCharacterOfPosition(current.getStart(source)).line+1, declaration:current.getText(source)});
  if (ts.isPropertyAssignment(current)) properties.push({name:current.name.getText(source), expression:current.initializer.getText(source), line:source.getLineAndCharacterOfPosition(current.getStart(source)).line+1, declaration:current.getText(source)});
  ts.forEachChild(current, members);
 }
 members(node);
 declarations.push({file,symbol,start:source.getLineAndCharacterOfPosition(node.getStart(source)).line+1,end:source.getLineAndCharacterOfPosition(node.getEnd()).line+1,declaration:node.getText(source),properties});
}
process.stdout.write(JSON.stringify({kind:'syntax-only source declarations; paths and wrapper effects require separate interpretation',declarations},null,2)+'\n');
