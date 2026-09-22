#!/usr/bin/env python3
"""CC iteration03 evidence driver.

This is an evidence driver, not an application test or a DTO implementation.
The TypeScript helper is intentionally syntax-only: it records literal source
declarations and does not evaluate modules or infer historical BSON values.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable


PLAN = Path(__file__).resolve().parents[5]
SLICE = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = Path("/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall")
NODE = Path("/Users/oubiwann/.local/bin/node")
COMPILER = Path("/Users/oubiwann/lab/billosys/LibreChat/node_modules/typescript/lib/typescript.js")
EXPERIMENT = SLICE / "artifacts/design-pass05/experiment.cjs"
HANDLE = SLICE / "artifacts/design-pass04/handle.cjs"
MATRIX = SLICE / "artifacts/design-pass05/field-matrix.json"
BASELINE = SLICE / "artifacts/design-pass05/result-01.json"
PRIOR_PACKET = SLICE / "artifacts/cc-evidence03"
REVIEW03 = SLICE / "artifacts/cdc-review03/result.json"
SOURCE_HEAD = "3e3c5410d3863118fdba694fb0cd51baeb7102f9"
NODE_VERSION = "v22.22.3"
COMPILER_VERSION = "5.9.3"
COMPILER_SHA = "3ae902c92cc44dace175c0e69e13a4b0899f6983c6121d76b9ab8dd5795e7675"
REVIEW03_SHA = "de65a055a5c9d32d503ee67a6285e0fef8706b2e954c2722c79f7261dd80a0ca"
PROMPT_SHA = "9f1aafceeedab3d1070945faf366a91237d41a9e130c584284335aeafd732848"
INTRODUCING_COMMIT = "d31a81ab341225303f0861a3c85396ca5a9ddacf"

PACKET_NAMES = {
    "intake.md",
    "report.md",
    "nested-fields.json",
    "replay-result.json",
    "execution.log",
    "replay.py",
    "SHA256SUMS",
}

DECLARATION_REQUESTS = [
    ("packages/data-provider/src/types/agents.ts", "ToolCall"),
    ("packages/data-provider/src/types/files.ts", "RunFileProvenance"),
    ("packages/data-provider/src/types/files.ts", "TFile"),
    ("packages/data-provider/src/types/content.ts", "CodeToolCall"),
    ("packages/data-provider/src/types/content.ts", "FunctionToolCall"),
    ("packages/data-provider/src/types/content.ts", "RetrievalToolCall"),
    ("packages/data-provider/src/types/content.ts", "FileSearchToolCall"),
    ("packages/data-provider/src/types/content.ts", "PartMetadata"),
    ("packages/data-provider/src/types/content.ts", "ContentMetadata"),
    ("packages/data-provider/src/types/content.ts", "ImageFile"),
    ("packages/data-provider/src/types/content.ts", "FileCitation"),
    ("packages/data-provider/src/types/content.ts", "FileCitationDetails"),
    ("packages/data-provider/src/types/content.ts", "FilePath"),
    ("packages/data-provider/src/types/content.ts", "FilePathDetails"),
    ("packages/data-provider/src/types/content.ts", "Text"),
    ("packages/data-provider/src/types/content.ts", "SummaryContentPart"),
    ("packages/data-provider/src/types/content.ts", "SteerContentPart"),
    ("packages/data-provider/src/types/content.ts", "TMessageContentParts"),
    ("packages/data-provider/src/types/web.ts", "Highlight"),
    ("packages/data-provider/src/types/web.ts", "ProcessedSource"),
    ("packages/data-provider/src/types/web.ts", "ProcessedOrganic"),
    ("packages/data-provider/src/types/web.ts", "ProcessedTopStory"),
    ("packages/data-provider/src/types/web.ts", "ResultReference"),
    ("packages/data-provider/src/types/web.ts", "SearchResultData"),
    ("packages/data-provider/src/types/web.ts", "References"),
    ("packages/data-provider/src/types/web.ts", "OrganicResult"),
    ("packages/data-provider/src/types/web.ts", "TopStoryResult"),
    ("packages/data-provider/src/types/web.ts", "MediaReference"),
    ("packages/data-provider/src/types/web.ts", "UsedReferences"),
    ("packages/data-provider/src/codeEnvRef.ts", "CodeEnvRefBase"),
    ("packages/data-provider/src/codeEnvRef.ts", "CodeExecutionProfile"),
    ("packages/data-provider/src/codeEnvRef.ts", "CodeEnvRef"),
    ("packages/data-provider/src/codeEnvRef.ts", "CodeEnvRefMap"),
    ("packages/data-provider/src/feedback.ts", "TFeedbackTag"),
    ("packages/data-provider/src/feedback.ts", "feedbackSchema"),
    ("packages/data-provider/src/feedback.ts", "TFeedback"),
    ("packages/data-provider/src/code/workspace.ts", "CodeWorkspaceSelection"),
    ("packages/data-provider/src/schemas.ts", "agentFadingTierSchema"),
    ("packages/data-provider/src/schemas.ts", "tExampleSchema"),
    ("packages/data-provider/src/schemas.ts", "tMessageSchema"),
    ("packages/data-provider/src/schemas.ts", "TAttachmentMetadata"),
    ("packages/data-provider/src/schemas.ts", "TAttachment"),
    ("packages/data-provider/src/schemas.ts", "TMessage"),
    ("packages/data-provider/src/schemas.ts", "subagentThreadLineageSchema"),
    ("packages/data-provider/src/filters.ts", "userSubmittedMessageFieldPathSchema"),
    ("packages/data-schemas/src/methods/message.ts", "CLIENT_MESSAGE_SELECT"),
]

SOURCE_FINGERPRINT_FILES = sorted({path for path, _ in DECLARATION_REQUESTS} | {
    "packages/data-schemas/src/methods/conversation.ts",
})


TS_EXTRACTOR = r'''
const fs = require('fs');
const ts = require(process.argv[2]);
const sourceRoot = process.argv[3];
const requests = JSON.parse(process.argv[4]);

function lineOf(sf, pos) { return sf.getLineAndCharacterOfPosition(pos).line + 1; }
function text(sf, node) { return node ? node.getText(sf) : null; }
function nameOf(sf, node) {
  if (!node || !node.name) return null;
  return node.name.getText(sf);
}
function isArrayType(node) {
  return !!node && (ts.isArrayTypeNode(node) || (ts.isTypeReferenceNode(node) && node.typeName.getText(sfGlobal) === 'Array'));
}
function addArraySuffix(path, node, expr) {
  const typeText = text(sfGlobal, node) || '';
  const exprText = expr || '';
  if ((typeText.endsWith('[]') || /^Array\s*</.test(typeText) || /\.array\s*\(/.test(exprText)) && !path.endsWith('[]')) return path + '[]';
  return path;
}
let sfGlobal = null;

function walkType(sf, node, prefix, branch, properties) {
  if (!node) return;
  if (ts.isParenthesizedTypeNode(node)) return walkType(sf, node.type, prefix, branch, properties);
  if (ts.isUnionTypeNode(node) || ts.isIntersectionTypeNode(node)) {
    const kind = ts.isUnionTypeNode(node) ? 'union' : 'intersection';
    node.types.forEach((child, i) => walkType(sf, child, prefix, branch + '|' + kind + ':' + i, properties));
    return;
  }
  if (ts.isArrayTypeNode(node)) return walkType(sf, node.elementType, prefix + '[]', branch, properties);
  if (ts.isTypeLiteralNode(node) || ts.isInterfaceDeclaration(node)) {
    const members = node.members || [];
    members.forEach(member => {
      if (!ts.isPropertySignature(member) && !ts.isPropertyDeclaration(member)) return;
      const rawName = nameOf(sf, member);
      if (!rawName) return;
      const p = prefix ? prefix + '.' + rawName : rawName;
      const typeNode = member.type || null;
      const rec = {
        path: p,
        name: rawName,
        type: text(sf, typeNode),
        expression: null,
        optional: !!member.questionToken,
        line: lineOf(sf, member.getStart(sf)),
        declaration: text(sf, member),
        branch,
      };
      properties.push(rec);
      if (typeNode) walkType(sf, typeNode, p, branch, properties);
    });
  }
}

function walkZod(sf, node, prefix, properties) {
  if (!node) return;
  if (ts.isCallExpression(node)) {
    const callee = node.expression;
    if (ts.isPropertyAccessExpression(callee) && callee.name.text === 'object' && node.arguments.length) {
      const object = node.arguments[0];
      if (ts.isObjectLiteralExpression(object)) {
        object.properties.forEach(member => {
          if (!ts.isPropertyAssignment(member) && !ts.isShorthandPropertyAssignment(member)) return;
          const rawName = nameOf(sf, member) || member.name.getText(sf);
          const p = prefix ? prefix + '.' + rawName : rawName;
          const initializer = member.initializer || member.name;
          const expression = text(sf, initializer);
          properties.push({
            path: p,
            name: rawName,
            type: null,
            expression,
            optional: /\.optional\s*\(/.test(expression),
            line: lineOf(sf, member.getStart(sf)),
            declaration: text(sf, member),
            branch: 'zod-object',
          });
          walkZod(sf, initializer, p, properties);
        });
      }
    }
    walkZod(sf, node.expression, prefix, properties);
    node.arguments.forEach(arg => walkZod(sf, arg, prefix, properties));
    return;
  }
  if (ts.isPropertyAccessExpression(node)) return walkZod(sf, node.expression, prefix, properties);
  if (ts.isPropertyAssignment(node)) return walkZod(sf, node.initializer, prefix, properties);
}

function findDeclaration(sf, symbol) {
  let found = null;
  function visit(node) {
    if (found) return;
    if ((ts.isTypeAliasDeclaration(node) || ts.isInterfaceDeclaration(node) || ts.isEnumDeclaration(node)) && nameOf(sf, node) === symbol) found = node;
    else if (ts.isVariableDeclaration(node) && nameOf(sf, node) === symbol) found = node;
    if (!found) ts.forEachChild(node, visit);
  }
  visit(sf);
  return found;
}

const declarations = [];
for (const [file, symbol] of requests) {
  const absolute = sourceRoot + '/' + file;
  const contents = fs.readFileSync(absolute, 'utf8');
  sfGlobal = ts.createSourceFile(absolute, contents, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS);
  const node = findDeclaration(sfGlobal, symbol);
  if (!node) { declarations.push({file, symbol, missing: true}); continue; }
  const start = lineOf(sfGlobal, node.getStart(sfGlobal));
  const end = lineOf(sfGlobal, node.getEnd());
  const sourceText = text(sfGlobal, node);
  const properties = [];
  const literals = [];
  if (ts.isTypeAliasDeclaration(node)) walkType(sfGlobal, node.type, '', 'root', properties);
  else if (ts.isInterfaceDeclaration(node)) walkType(sfGlobal, node, '', 'root', properties);
  else if (ts.isVariableDeclaration(node)) {
    if (node.type) walkType(sfGlobal, node.type, '', 'root', properties);
    walkZod(sfGlobal, node.initializer, '', properties);
    function collectStrings(n) {
      if (ts.isStringLiteral(n) || ts.isNoSubstitutionTemplateLiteral(n)) literals.push(n.text);
      ts.forEachChild(n, collectStrings);
    }
    collectStrings(node.initializer);
  }
  declarations.push({
    file, symbol, kind: ts.SyntaxKind[node.kind], start, end, sourceText,
    properties, literals,
  });
}
process.stdout.write(JSON.stringify({kind: 'syntax-only source declarations; paths and wrapper effects require separate interpretation', declarations}));
'''


class EvidenceError(RuntimeError):
    pass


class Logger:
    def __init__(self, path: Path, truncate: bool = False):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.fp = path.open("w" if truncate else "a", encoding="utf-8")

    def command(self, argv: list[str], cwd: Path, result: subprocess.CompletedProcess[str]) -> None:
        self.fp.write(json.dumps({
            "kind": "command",
            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "argv": [str(x) for x in argv],
            "cwd": str(cwd),
            "status": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }, sort_keys=True) + "\n")
        self.fp.flush()

    def event(self, name: str, value: Any) -> None:
        self.fp.write(json.dumps({"kind": "event", "name": name, "value": value}, sort_keys=True) + "\n")
        self.fp.flush()

    def close(self) -> None:
        self.fp.close()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fp:
        return json.load(fp)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_logged(argv: list[str], cwd: Path, logger: Logger | None, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)
    if logger:
        logger.command(argv, cwd, result)
    if check and result.returncode != 0:
        raise EvidenceError(f"command failed ({result.returncode}): {argv}")
    return result


def git_output(args: list[str], logger: Logger | None = None) -> str:
    result = run_logged(["git", "-C", str(SOURCE), *args], SOURCE, logger, check=True)
    return result.stdout.strip()


def preflight(logger: Logger | None = None) -> dict[str, Any]:
    head = git_output(["rev-parse", "HEAD"], logger)
    status = git_output(["status", "--short"], logger)
    node = run_logged([str(NODE), "--version"], PLAN, logger, check=True).stdout.strip()
    compiler_digest = sha256(COMPILER)
    if head != SOURCE_HEAD:
        raise EvidenceError(f"source head mismatch: {head}")
    if status:
        raise EvidenceError(f"source worktree dirty: {status}")
    if node != NODE_VERSION:
        raise EvidenceError(f"node mismatch: {node}")
    if compiler_digest != COMPILER_SHA:
        raise EvidenceError(f"compiler digest mismatch: {compiler_digest}")
    return {
        "sourceHead": head,
        "sourceStatus": "clean",
        "node": node,
        "compiler": {"path": str(COMPILER), "version": COMPILER_VERSION, "sha256": compiler_digest},
    }


def run_extractor(logger: Logger | None = None) -> dict[str, Any]:
    with tempfile.NamedTemporaryFile("w", suffix="-cc-iteration03-extractor.cjs", delete=False, encoding="utf-8") as fp:
        fp.write(TS_EXTRACTOR)
        helper = Path(fp.name)
    try:
        result = run_logged(
            [str(NODE), str(helper), str(COMPILER), str(SOURCE), json.dumps(DECLARATION_REQUESTS)],
            PLAN, logger, check=True,
        )
        return json.loads(result.stdout)
    finally:
        helper.unlink(missing_ok=True)


def decl_index(extraction: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    result = {}
    for declaration in extraction["declarations"]:
        result[(declaration["file"], declaration["symbol"])] = declaration
    return result


def declaration_ref(declaration: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": declaration["file"],
        "symbol": declaration["symbol"],
        "lines": [declaration.get("start"), declaration.get("end")],
        "sha256": hashlib.sha256(declaration.get("sourceText", "").encode()).hexdigest(),
    }


def is_array(p: dict[str, Any]) -> bool:
    value = (p.get("type") or p.get("expression") or "").strip()
    return value.endswith("[]") or value.startswith("Array<") or value.startswith("ReadonlyArray<") or value.startswith("z.array(")


def actual_property_path(p: dict[str, Any]) -> str:
    path = p["path"]
    if is_array(p) and not path.endswith("[]"):
        path += "[]"
    return path


def member_row(p: dict[str, Any], declaration: dict[str, Any], prefix: str = "", context: str = "declaration", branch: str | None = None, use_site: dict[str, Any] | None = None) -> dict[str, Any]:
    declared = p.get("type") or p.get("expression") or "unknown"
    default = "none"
    if ".default(" in declared:
        default = declared[declared.index(".default(") + 1 : declared.rfind(")") + 1]
    nullable = "nullable" in declared or "null" in declared or "undefined" in declared
    row = {
        "path": prefix + actual_property_path(p),
        "declaredType": declared,
        "declarationContext": context,
        "branch": branch if branch is not None else p.get("branch"),
        "localOptional": bool(p.get("optional")) or ".optional(" in declared,
        "requiredness": "optional" if bool(p.get("optional")) or ".optional(" in declared else "required",
        "default": default,
        "nullable": nullable,
        "sourceRefs": [{
            **declaration_ref(declaration),
            "line": p.get("line"),
            "declaration": p.get("declaration"),
        }],
    }
    if use_site:
        row["useSite"] = use_site
    return row


def props(index: dict[tuple[str, str], dict[str, Any]], file: str, symbol: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    declaration = index.get((file, symbol))
    if not declaration or declaration.get("missing"):
        raise EvidenceError(f"required declaration missing: {file}:{symbol}")
    return declaration, declaration.get("properties", [])


def rows_from(index: dict[tuple[str, str], dict[str, Any]], file: str, symbol: str, prefix: str = "", context: str = "declaration", branch: str | None = None, use_site: dict[str, Any] | None = None, names: set[str] | None = None) -> list[dict[str, Any]]:
    declaration, properties = props(index, file, symbol)
    rows = []
    for p in properties:
        if names and p["path"].split(".", 1)[0] not in names:
            continue
        rows.append(member_row(p, declaration, prefix, context, branch, use_site))
    return rows


def add_unique(rows: list[dict[str, Any]], new_rows: list[dict[str, Any]]) -> None:
    seen = {(r["path"], r.get("branch"), r["sourceRefs"][0]["path"], r["sourceRefs"][0]["symbol"]) for r in rows}
    for row in new_rows:
        key = (row["path"], row.get("branch"), row["sourceRefs"][0]["path"], row["sourceRefs"][0]["symbol"])
        if key not in seen:
            rows.append(row)
            seen.add(key)


def applicable(record: str, field: str) -> dict[str, Any]:
    if record == "message":
        result = {
            "serverHistory": {"status": "established", "disposition": "message-view member"},
            "publicMessages": {"status": "established", "disposition": "included; nested projection exclusions apply"},
            "turnConversation": {"status": "not applicable", "disposition": "not a conversation result member"},
            "accessProbe": {"status": "not applicable", "disposition": "not a conversation ownership member"},
        }
        if field == "metadata":
            result["publicMessages"] = {"status": "established", "disposition": "included with nested metadata.thoughtSignatures exclusion"}
        return result
    result = {
        "serverHistory": {"status": "not applicable", "disposition": "conversation result is not a message history row"},
        "publicMessages": {"status": "not applicable", "disposition": "conversation root is not a message projection"},
        "turnConversation": {"status": "established", "disposition": "conversation-view member"},
        "accessProbe": {"status": "not selected", "disposition": "not used for this root"},
    }
    if field == "subagentThread":
        result["accessProbe"] = {
            "status": "established",
            "disposition": "selected full lineage object",
            "sourceRefs": [{"path": "packages/data-schemas/src/methods/conversation.ts", "lines": [2060, 2078], "symbol": "getConvoOwnership", "kind": "consumer", "observation": "projection selects user tenantId subagentThread"}],
        }
    return result


def source_refs_for(declaration: dict[str, Any], observation: str = "syntax-only declaration") -> list[dict[str, Any]]:
    return [{**declaration_ref(declaration), "kind": "type-only", "observation": observation}]


def build_coverage(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    selected = {
        ("message", "content"), ("message", "files"), ("message", "attachments"), ("message", "metadata"),
        ("message", "feedback"), ("message", "contextMeta"), ("message", "userSubmittedMessageFieldPaths"),
        ("convo", "examples"), ("convo", "codeWorkspaces"), ("convo", "subagentThread"),
    }
    coverage = []
    for record in matrix["records"]:
        record_name = "message" if record["name"] == "messageSchema" else "conversation"
        for field in record["fields"]:
            classification = "selected nested root" if (record_name, field["name"]) in selected else "other scalar/array field outside this deep inspection"
            if field["name"] in {"_id", "__v"}:
                classification = "adapter-private physical relationship"
            coverage.append({
                "record": record_name,
                "field": field["name"],
                "classification": classification,
                "source": field.get("source"),
                "storageDefinition": field.get("storageDefinition"),
                "interfaceType": field.get("interfaceType"),
                "provider": field.get("provider"),
                "defaultRead": field.get("defaultRead"),
                "publicRead": field.get("publicRead"),
                "portableServerRead": field.get("portableServerRead"),
                "endpointUnsetRule": field.get("endpointUnsetRule"),
            })
    if len(coverage) != 117 or len({(x["record"], x["field"]) for x in coverage}) != 117:
        raise EvidenceError("fresh matrix coverage is not exactly 117 unique fields")
    return coverage


def build_roots(index: dict[tuple[str, str], dict[str, Any]]) -> list[dict[str, Any]]:
    roots: list[dict[str, Any]] = []
    def root(record: str, field: str, schema: dict[str, Any], direct: str, members: list[dict[str, Any]], wrapper: str, boundary: str, exclusions: list[str]) -> None:
        roots.append({
            "record": record, "field": field,
            "schema": schema,
            "directType": direct,
            "wrapperAndRequiredness": wrapper,
            "openBoundary": boundary,
            "members": members,
            "applicability": applicable(record, field),
            "applicableNestedExclusions": exclusions,
        })

    tmsg, _ = props(index, "packages/data-provider/src/schemas.ts", "TMessage")
    tschema, _ = props(index, "packages/data-provider/src/schemas.ts", "tMessageSchema")
    tfile, _ = props(index, "packages/data-provider/src/types/files.ts", "TFile")
    tool, _ = props(index, "packages/data-provider/src/types/agents.ts", "ToolCall")
    content_rows: list[dict[str, Any]] = []
    add_unique(content_rows, rows_from(index, "packages/data-provider/src/types/content.ts", "TMessageContentParts", "content[].", "discriminated content branch"))
    add_unique(content_rows, rows_from(index, "packages/data-provider/src/types/agents.ts", "ToolCall", "content[].tool_call.", "nested tool-call declaration", "tool_call"))
    add_unique(content_rows, rows_from(index, "packages/data-provider/src/types/content.ts", "SummaryContentPart", "content[].", "summary branch; no wrapper path", "summary"))
    add_unique(content_rows, rows_from(index, "packages/data-provider/src/types/content.ts", "SteerContentPart", "content[].", "steer branch", "steer"))
    root("message", "content", declaration_ref(tschema), "TMessage.content?: TMessageContentParts[]", content_rows,
         "content is an optional array; discriminated branches keep branch IDs outside literal paths", "external AgentToolCall and provider media branches remain named open boundaries", [
             "content[].tool_call.backgroundTask.resultClaim", "content[].tool_call.backgroundTask.completionWakeup"])

    file_rows = rows_from(index, "packages/data-provider/src/types/files.ts", "TFile", "files[].", "TFile declaration", use_site={"wrapper": "Partial<TFile>[]", "effect": "outer properties optional at TMessage.files use site; nested TFile requiredness unchanged"})
    add_unique(file_rows, rows_from(index, "packages/data-provider/src/types/files.ts", "RunFileProvenance", "files[].metadata.runFile.", "nested local provenance declaration"))
    add_unique(file_rows, rows_from(index, "packages/data-provider/src/codeEnvRef.ts", "CodeEnvRefBase", "files[].metadata.codeEnvRef.", "nested local code environment declaration"))
    root("message", "files", declaration_ref(tmsg), "files?: Partial<TFile>[]", file_rows,
         "TMessage.files is a shallow Partial<TFile>[] use-site wrapper; TFile's local required/optional members are retained", "CodeEnvRef union branches and CodeEnvRefMap keyed values are local named boundaries; no historical BSON inference", [])

    attachment_rows: list[dict[str, Any]] = []
    add_unique(attachment_rows, rows_from(index, "packages/data-provider/src/schemas.ts", "TAttachment", "attachments[].", "attachment union declaration", "attachment-union"))
    add_unique(attachment_rows, rows_from(index, "packages/data-provider/src/types/files.ts", "TFile", "attachments[].", "attachment branch: TFile intersection", "tfile-intersection"))
    add_unique(attachment_rows, rows_from(index, "packages/data-provider/src/types/files.ts", "TFile", "attachments[].", "attachment branch: numeric expiry Pick", "numeric-expiry-pick", names={"filename", "filepath", "conversationId"}))
    add_unique(attachment_rows, rows_from(index, "packages/data-provider/src/schemas.ts", "TAttachmentMetadata", "attachments[].", "attachment metadata intersection", "attachment-metadata"))
    root("message", "attachments", declaration_ref(tmsg), "attachments?: TAttachment[]", attachment_rows,
         "TAttachment is a union with analytical branch IDs separate from actual attachments[]. member paths; Pick preserves selected TFile requiredness and Partial changes only selected outer fields", "SearchResultData and provider tool metadata remain open at their named declarations; web_search and file_search projections are distinct", [
             "attachments.web_search.knowledgeGraph", "attachments.web_search.peopleAlsoAsk", "attachments.web_search.relatedSearches", "attachments.web_search.shopping", "attachments.web_search.places", "attachments.web_search.news", "attachments.web_search.organic.sitelinks", "attachments.web_search.organic.highlights", "attachments.web_search.topStories.highlights"])

    metadata_rows = rows_from(index, "packages/data-provider/src/schemas.ts", "tMessageSchema", "", "message schema Zod declaration", names={"metadata"})
    root("message", "metadata", declaration_ref(tschema), "z.record(z.unknown()).optional()", metadata_rows,
         "message metadata is an open record; TFile.metadata members are not transferred to this root", "unknown record values are intentionally unresolved; no JSON-only or BSON-value claim", ["metadata.thoughtSignatures"])

    feedback_rows = rows_from(index, "packages/data-provider/src/feedback.ts", "feedbackSchema", "feedback.", "feedback Zod declaration")
    add_unique(feedback_rows, rows_from(index, "packages/data-provider/src/feedback.ts", "TFeedback", "feedback.", "provider feedback declaration"))
    add_unique(feedback_rows, rows_from(index, "packages/data-provider/src/feedback.ts", "TFeedbackTag", "feedback.tag.", "nested feedback tag declaration"))
    root("message", "feedback", declaration_ref(tschema), "feedback?: feedbackSchema / TFeedback", feedback_rows,
         "feedback has a minimal Zod input shape and a richer provider TFeedback tag shape; these declarations are not silently collapsed", "feedback tag key vocabulary comes from the local feedback module; runtime persistence compatibility remains CDC-owned", [])

    context_rows = rows_from(index, "packages/data-provider/src/schemas.ts", "tMessageSchema", "", "message schema contextMeta object", names={"contextMeta"})
    add_unique(context_rows, rows_from(index, "packages/data-provider/src/schemas.ts", "agentFadingTierSchema", "contextMeta.fading.", "nested fading declaration", "fading"))
    add_unique(context_rows, rows_from(index, "packages/data-provider/src/schemas.ts", "agentFadingTierSchema", "contextMeta.fadingTiers[].", "nested fading declaration", "fadingTiers"))
    context_rows.append({"path": "contextMeta.fadingTiers[].agentId", "declaredType": "z.string().min(1)", "declarationContext": "tMessageSchema inline extend", "branch": "fadingTiers", "localOptional": False, "requiredness": "required", "default": "none", "nullable": False, "sourceRefs": [{**declaration_ref(tschema), "line": 952, "declaration": "agentFadingTierSchema.extend({ agentId: z.string().min(1) })"}]})
    root("message", "contextMeta", declaration_ref(tschema), "optional z.object contextMeta", context_rows,
         "contextMeta has an optional ancestor; its local fading/fadingTiers leaves retain their own requiredness", "agentFadingTierSchema is local and closed; provider/runtime calibration semantics remain distinct from storage", ["contextMeta"])

    marker_rows = rows_from(index, "packages/data-provider/src/filters.ts", "userSubmittedMessageFieldPathSchema", "userSubmittedMessageFieldPaths[].", "strict path-marker Zod declaration")
    root("message", "userSubmittedMessageFieldPaths", declaration_ref(tschema), "array(userSubmittedMessageFieldPathSchema).optional()", marker_rows,
         "each path marker has exactly required path and field members; source/operation are not declared", "HITL_MESSAGE_FILTER_FIELDS is an enum boundary; no extra keys are source-established", [])

    example_rows = rows_from(index, "packages/data-provider/src/schemas.ts", "tExampleSchema", "examples[].", "example Zod declaration")
    root("conversation", "examples", declaration_ref(index[("packages/data-provider/src/schemas.ts", "tExampleSchema")]), "examples?: TExample[]", example_rows,
         "input and output each require content:string; role/files are not declared by tExampleSchema", "example records remain a provider/schema boundary; storage Mixed breadth is not inferred away", [])

    workspace_rows = rows_from(index, "packages/data-provider/src/code/workspace.ts", "CodeWorkspaceSelection", "codeWorkspaces[].", "workspace entry declaration")
    root("conversation", "codeWorkspaces", declaration_ref(index[("packages/data-provider/src/code/workspace.ts", "CodeWorkspaceSelection")]), "codeWorkspaces?: CodeWorkspaceSelection[]", workspace_rows,
         "the codeWorkspaces root is optional; each selected entry preserves its declared required env/workspace members", "workspace selection is a named provider boundary; no root-required claim", [])

    lineage_rows = rows_from(index, "packages/data-provider/src/schemas.ts", "subagentThreadLineageSchema", "subagentThread.", "lineage Zod declaration")
    root("conversation", "subagentThread", declaration_ref(index[("packages/data-provider/src/schemas.ts", "subagentThreadLineageSchema")]), "subagentThread?: subagentThreadLineageSchema", lineage_rows,
         "the root is optional; parentAgentId is optional while the other seven lineage members are required", "getConvoOwnership selects the full lineage object for its access probe; public admission use is separate", [])
    return roots


def projection(index: dict[tuple[str, str], dict[str, Any]]) -> dict[str, Any]:
    projection_decl = index[("packages/data-schemas/src/methods/message.ts", "CLIENT_MESSAGE_SELECT")]
    nested = sorted(x[1:] for x in projection_decl.get("literals", []) if x.startswith("-") and "." in x)
    if len(nested) != 12:
        raise EvidenceError(f"expected 12 nested projection exclusions, got {len(nested)}")
    def canonical_projection_path(source_path: str) -> str:
        pieces = source_path.split(".")
        rendered = []
        for i, piece in enumerate(pieces):
            if i == 0 and piece in {"content", "attachments"}:
                rendered.append(piece + "[]")
            elif piece in {"organic", "topStories"}:
                rendered.append(piece + "[]")
            else:
                rendered.append(piece)
        return ".".join(rendered)
    exclusions = [{"path": canonical_projection_path(x), "sourcePath": x, "sourceRef": {**declaration_ref(projection_decl), "kind": "projection-literal"}} for x in nested]
    return {
        "sourceRef": declaration_ref(projection_decl),
        "nestedExclusions": exclusions,
        "survivors": [
            "metadata", "metadata.* except metadata.thoughtSignatures", "content[].tool_call.backgroundTask.status", "content[].tool_call.backgroundTask.settledAt",
            "attachments[].web_search.organic[]", "attachments[].web_search.topStories[]", "attachments[].web_search.images[]", "attachments[].web_search.videos[]",
            "attachments[].file_search.organic[]", "attachments[].file_search.topStories[]", "attachments[].file_search.places[]", "attachments[].file_search.news[]",
        ],
        "partialContainers": [
            {"container": "attachments[].web_search.organic[]", "removed": ["sitelinks", "highlights"]},
            {"container": "attachments[].web_search.topStories[]", "removed": ["highlights"]},
        ],
        "viewDistinctions": {
            "web_search": "the twelve CLIENT_MESSAGE_SELECT nested exclusions apply to web_search; organic/topStories remain partial containers",
            "file_search": "web_search exclusions are not copied to file_search; its named SearchResultData remains a separate open/provider boundary",
        },
    }


def build_inventory(extraction: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    index = decl_index(extraction)
    missing = [f"{f}:{s}" for f, s in DECLARATION_REQUESTS if (f, s) not in index or index[(f, s)].get("missing")]
    if missing:
        raise EvidenceError("missing source declarations: " + ", ".join(missing))
    declarations = []
    for declaration in extraction["declarations"]:
        declaration = copy.deepcopy(declaration)
        declaration["sourceRef"] = declaration_ref(declaration)
        declarations.append(declaration)
    sources = []
    for rel in SOURCE_FINGERPRINT_FILES:
        path = SOURCE / rel
        sources.append({"path": rel, "sha256": sha256(path), "sourceHead": SOURCE_HEAD})
    roots = build_roots(index)
    return {
        "contract": "iteration03 source-declaration inventory; syntax extraction is structural evidence, not semantic DTO acceptance",
        "sourceHead": SOURCE_HEAD,
        "sources": sources,
        "declarations": declarations,
        "coverage": build_coverage(matrix),
        "roots": roots,
        "nestedExclusions": projection(index)["nestedExclusions"],
        "projection": projection(index),
        "unresolved": [
            {"question": "Which historical Mixed/BSON values occur in metadata and provider open boundaries?", "evidence": "current declarations are open/unknown; no private corpus or database was read", "affectedRoots": ["message.metadata", "message.attachments"], "owner": "CDC"},
            {"question": "What codec and patch policy preserves absent/undefined/null/empty/populated states?", "evidence": "field matrix and source declarations do not choose a portable codec", "affectedRoots": ["message.content", "message.files", "message.metadata", "conversation.examples"], "owner": "CDC"},
            {"question": "What is the implementation fence and D07 source-build proof?", "evidence": "this packet uses Node 22 and storage doubles; pinned source/build acceptance remains open", "affectedRoots": ["all"], "owner": "CDC"},
        ],
    }


def flatten_members(inventory: dict[str, Any]) -> dict[tuple[str, str, str | None, str], dict[str, Any]]:
    result = {}
    for root in inventory["roots"]:
        for member in root["members"]:
            ref = member["sourceRefs"][0]
            key = (f"{root['record']}.{root['field']}", member["path"], member.get("branch"), f"{ref['path']}:{ref['symbol']}")
            result[key] = member
    return result


def canonical(path: str) -> str:
    return path.replace("[]", "")


def is_descendant(path: str, ancestor: str) -> bool:
    p, a = canonical(path), canonical(ancestor)
    return p == a or p.startswith(a + ".")


def validate_projection(inventory: dict[str, Any]) -> None:
    exclusions = [x["path"] for x in inventory["nestedExclusions"]]
    projection_data = inventory["projection"]
    for survivor in projection_data["survivors"]:
        if " except " in survivor:
            continue
        if any(is_descendant(survivor, excluded) for excluded in exclusions):
            raise EvidenceError(f"projection survivor is excluded or descends from exclusion: {survivor}")
    for partial in projection_data["partialContainers"]:
        container = partial["container"]
        if any(is_descendant(container, excluded) for excluded in exclusions):
            raise EvidenceError(f"partial container itself excluded: {container}")
        expected = {canonical(container + "." + child) for child in partial["removed"]}
        actual = {canonical(x) for x in exclusions if canonical(x).startswith(canonical(container) + ".")}
        if actual and not expected:
            raise EvidenceError(f"container falsely marked fully preserved despite nested exclusions: {container}")
        if not expected <= actual:
            raise EvidenceError(f"partial container removals incomplete: {container}")
    if "attachments[].web_search.organic[]" not in projection_data["survivors"]:
        raise EvidenceError("organic[] survivor was lost")


def validate_semantics(inventory: dict[str, Any], fresh: dict[str, Any]) -> dict[str, Any]:
    if inventory["sourceHead"] != SOURCE_HEAD:
        raise EvidenceError("inventory source head mismatch")
    if inventory["coverage"] != fresh["coverage"]:
        raise EvidenceError("coverage differs from fresh matrix-derived coverage")
    if inventory["nestedExclusions"] != fresh["nestedExclusions"]:
        raise EvidenceError("nested projection exclusions differ from fresh source extraction")
    submitted_declarations = {(x["file"], x["symbol"]): x for x in inventory["declarations"]}
    fresh_declarations = {(x["file"], x["symbol"]): x for x in fresh["declarations"]}
    if set(submitted_declarations) != set(fresh_declarations):
        raise EvidenceError("declaration identity set differs from fresh extraction")
    for key, expected_decl in fresh_declarations.items():
        candidate = submitted_declarations[key]
        for field in ("kind", "start", "end", "sourceText", "properties", "literals"):
            if candidate.get(field) != expected_decl.get(field):
                raise EvidenceError(f"declaration record differs from fresh extraction: {key} field={field}")
    submitted = flatten_members(inventory)
    expected = flatten_members(fresh)
    if set(submitted) != set(expected):
        missing, extra = sorted(set(expected) - set(submitted)), sorted(set(submitted) - set(expected))
        raise EvidenceError(f"member closed set differs: missing={missing[:4]} extra={extra[:4]}")
    for key in expected:
        left, right = submitted[key], expected[key]
        for field in ("path", "declaredType", "branch", "localOptional", "requiredness", "default", "nullable"):
            if left.get(field) != right.get(field):
                raise EvidenceError(f"member {key} differs in {field}")
        if left["sourceRefs"] != right["sourceRefs"]:
            raise EvidenceError(f"member {key} has stale or invented source reference")
    validate_projection(inventory)
    bad = [m["path"] for r in inventory["roots"] for m in r["members"] if ".variant" in m["path"] or ".summary." in m["path"] or ".error." in m["path"]]
    if bad:
        raise EvidenceError("invented wrapper/branch paths: " + ", ".join(bad[:5]))
    marker = next(r for r in inventory["roots"] if r["field"] == "userSubmittedMessageFieldPaths")
    if {m["path"] for m in marker["members"]} != {"userSubmittedMessageFieldPaths[].path", "userSubmittedMessageFieldPaths[].field"}:
        raise EvidenceError("path-marker member set is not the strict path/field pair")
    examples = next(r for r in inventory["roots"] if r["field"] == "examples")
    example_paths = {m["path"] for m in examples["members"]}
    if example_paths != {"examples[].input", "examples[].input.content", "examples[].output", "examples[].output.content"}:
        raise EvidenceError("example member set contains non-declared fields")
    lineage = next(r for r in inventory["roots"] if r["field"] == "subagentThread")
    parent = next(m for m in lineage["members"] if m["path"] == "subagentThread.parentAgentId")
    if parent["requiredness"] != "optional":
        raise EvidenceError("parentAgentId requiredness changed")
    files = next(r for r in inventory["roots"] if r["field"] == "files")
    file_id = next(m for m in files["members"] if m["path"] == "files[].file_id")
    if file_id["requiredness"] != "required" or file_id.get("useSite", {}).get("effect") != "outer properties optional at TMessage.files use site; nested TFile requiredness unchanged":
        raise EvidenceError("TFile local/use-site requiredness distinction lost")
    metadata = next(r for r in inventory["roots"] if r["field"] == "metadata")
    if any(m["path"] != "metadata" for m in metadata["members"]):
        raise EvidenceError("TFile metadata fields leaked into open message metadata")
    settled = next(m for r in inventory["roots"] for m in r["members"] if m["path"] == "content[].tool_call.backgroundTask.settledAt")
    if settled["declaredType"] != "Date" or settled["requiredness"] != "required":
        raise EvidenceError("settledAt Date/required declaration lost")
    app = next(r for r in inventory["roots"] if r["field"] == "metadata")["applicability"]["publicMessages"]
    if "nested metadata.thoughtSignatures" not in app["disposition"]:
        raise EvidenceError("metadata public mapping incorrectly became whole-root exclusion")
    access = next(r for r in inventory["roots"] if r["field"] == "subagentThread")["applicability"]["accessProbe"]
    if access["status"] != "established" or "full lineage" not in access["disposition"]:
        raise EvidenceError("full access-probe lineage mapping was not established")
    return {
        "freshDeclarationCount": len(fresh["declarations"]),
        "freshMemberCount": len(expected),
        "submittedMemberCount": len(submitted),
        "closedSet": "exact source-derived member identity/type/reference equality",
    }


def matrix_queries(logger: Logger) -> tuple[dict[str, Any], dict[str, Any]]:
    query = ["jq", "-c", ".records[] | {name, fields: [.fields[].name], providerOnly, interfaceOnly, implicit}", str(MATRIX)]
    result = run_logged(query, PLAN, logger, check=True)
    records = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    wrong_name = run_logged(["jq", "-e", '.records[] | select(.name == "conversationSchema")', str(MATRIX)], PLAN, logger)
    wrong_level = run_logged(["jq", "-e", '.providerOnly', str(MATRIX)], PLAN, logger)
    logger.event("matrix-query-controls", {"wrongRecordNameStatus": wrong_name.returncode, "wrongLevelAncillaryStatus": wrong_level.returncode})
    data = read_json(MATRIX)
    if {x["name"] for x in records} != {"messageSchema", "convoSchema"}:
        raise EvidenceError("fresh matrix query missed messageSchema/convoSchema")
    expected = {"messageSchema": (44, 10, 4), "convoSchema": (73, 13, 3)}
    summary = {}
    for row in records:
        name = row["name"]
        counts = (len(row["fields"]), len(row["providerOnly"]), len(row["interfaceOnly"]))
        if counts != expected[name] or set(row["implicit"]) != {"createdAt", "updatedAt", "_id", "__v"}:
            raise EvidenceError(f"matrix query population mismatch for {name}: {counts}")
        summary[name] = {"fields": counts[0], "uniqueFields": len(set(row["fields"])), "providerOnly": counts[1], "interfaceOnly": counts[2], "implicit": row["implicit"]}
    return data, summary


def harness_result(logger: Logger | None = None) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="cc-evidence04-harness-") as temp:
        output = Path(temp) / "result.json"
        result = run_logged([str(NODE), str(EXPERIMENT), str(SOURCE), str(COMPILER), str(HANDLE), str(output)], PLAN, logger, check=True)
        if not output.exists():
            raise EvidenceError(f"pass05 harness did not create {output}: {result.stderr}")
        return read_json(output)


def compare_replay(result: dict[str, Any], submitted: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    if result != baseline or result != submitted:
        raise EvidenceError("pass05 behavior/provenance result differs from submitted or baseline")
    return {"submittedEqualsBaseline": True, "freshEqualsSubmitted": True, "freshEqualsBaseline": True, "readCases": len(result["readCases"]), "gateCases": len(result["gateCases"]), "preflightCases": len(result["preflightCases"]), "negativeControls": len(result["negativeControls"])}


def manifest_entries(packet: Path) -> dict[str, str]:
    lines = (packet / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    entries = {}
    for line in lines:
        if not line.strip():
            continue
        digest, name = line.split("  ", 1)
        entries[name] = digest
    return entries


def seal(packet: Path) -> None:
    entries = {name: sha256(packet / name) for name in sorted(PACKET_NAMES - {"SHA256SUMS"})}
    (packet / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in entries.items()), encoding="utf-8")


def verify_manifest(packet: Path) -> None:
    if set(p.name for p in packet.iterdir()) != PACKET_NAMES:
        raise EvidenceError("packet inventory is not exactly seven files")
    entries = manifest_entries(packet)
    if set(entries) != PACKET_NAMES - {"SHA256SUMS"}:
        raise EvidenceError("manifest does not seal exactly six payload files")
    for name, digest in entries.items():
        if sha256(packet / name) != digest:
            raise EvidenceError(f"manifest digest mismatch: {name}")


def validate_packet(packet: Path, runner: Callable[[], dict[str, Any]] | None = None, observed: dict[str, Any] | None = None) -> dict[str, Any]:
    verify_manifest(packet)
    submitted = read_json(packet / "replay-result.json")
    inventory = read_json(packet / "nested-fields.json")
    if observed:
        for key, expected in (("sourceHead", SOURCE_HEAD), ("node", NODE_VERSION)):
            if observed.get(key, expected) != expected:
                raise EvidenceError(f"preflight rejected observation {key}={observed[key]}")
    fresh = build_inventory(run_extractor(), read_json(MATRIX))
    validate_semantics(inventory, fresh)
    baseline = read_json(BASELINE)
    fresh_result = runner() if runner else harness_result()
    replay_check = compare_replay(fresh_result, submitted, baseline)
    return {"manifest": "pass", "sourceDeclarationValidation": "pass", "replay": replay_check}


def copy_packet(packet: Path) -> Path:
    temp = Path(tempfile.mkdtemp(prefix="cc-evidence04-control-")) / "packet"
    shutil.copytree(packet, temp)
    return temp


def mutate_and_reseal(packet: Path, filename: str, mutation: Callable[[Any], None]) -> Path:
    copy = copy_packet(packet)
    path = copy / filename
    value = read_json(path)
    mutation(value)
    write_json(path, value)
    seal(copy)
    return copy


def self_test(packet: Path) -> dict[str, Any]:
    positive = []
    negative = []
    before = {name: sha256(packet / name) for name in PACKET_NAMES}
    validate_packet(packet)
    positive.append({"name": "unchanged sealed packet", "accepted": True})
    validate_projection(read_json(packet / "nested-fields.json"))
    positive.append({"name": "organic[] retained with declared nested removals", "accepted": True})

    def expect(name: str, func: Callable[[], Any]) -> None:
        try:
            func()
        except Exception as exc:  # controls intentionally exercise rejection paths
            negative.append({"name": name, "rejected": True, "reason": str(exc)})
        else:
            negative.append({"name": name, "rejected": False})

    expect("wrong source head preflight", lambda: validate_packet(packet, runner=lambda: (_ for _ in ()).throw(AssertionError("runner called")), observed={"sourceHead": "wrong"}))
    expect("submitted success false resealed", lambda: validate_packet(mutate_and_reseal(packet, "replay-result.json", lambda x: x.__setitem__("success", False))))
    expect("submitted node provenance resealed", lambda: validate_packet(mutate_and_reseal(packet, "replay-result.json", lambda x: x.__setitem__("node", "v99.0.0"))))
    expect("invented path-marker member", lambda: validate_packet(mutate_and_reseal(packet, "nested-fields.json", lambda x: next(r for r in x["roots"] if r["field"] == "userSubmittedMessageFieldPaths")["members"].append({"path": "userSubmittedMessageFieldPaths[].source"}))))
    expect("invented summary wrapper", lambda: validate_packet(mutate_and_reseal(packet, "nested-fields.json", lambda x: next(r for r in x["roots"] if r["field"] == "content")["members"].append({"path": "content[].summary.tokenCount"}))))
    expect("wrong parentAgentId optionality", lambda: validate_packet(mutate_and_reseal(packet, "nested-fields.json", lambda x: next(m for r in x["roots"] if r["field"] == "subagentThread" for m in r["members"] if m["path"] == "subagentThread.parentAgentId").__setitem__("requiredness", "required"))))
    expect("Date to string mutation", lambda: validate_packet(mutate_and_reseal(packet, "nested-fields.json", lambda x: next(m for r in x["roots"] for m in r["members"] if m["path"] == "content[].tool_call.backgroundTask.settledAt").__setitem__("declaredType", "string"))))
    expect("required TMessage.files.file_id", lambda: validate_packet(mutate_and_reseal(packet, "nested-fields.json", lambda x: next(m for r in x["roots"] if r["field"] == "files" for m in r["members"] if m["path"] == "files[].file_id").__setitem__("requiredness", "optional"))))
    expect("resultClaim survives completionWakeup exclusion", lambda: validate_packet(mutate_and_reseal(packet, "nested-fields.json", lambda x: x["projection"]["survivors"].append("content[].tool_call.backgroundTask.resultClaim"))))
    expect("exact excluded projection path", lambda: validate_packet(mutate_and_reseal(packet, "nested-fields.json", lambda x: x["projection"]["survivors"].append("attachments[].web_search.organic.highlights"))))
    expect("fully preserved organic container", lambda: validate_packet(mutate_and_reseal(packet, "nested-fields.json", lambda x: x["projection"]["partialContainers"].append({"container": "attachments[].web_search.organic[]", "removed": []}))))
    after = {name: sha256(packet / name) for name in PACKET_NAMES}
    if before != after:
        raise EvidenceError("sealed self-test mutated its input packet")
    if any(x["rejected"] is not True for x in negative):
        raise EvidenceError("one or more negative controls was accepted")
    return {"positive": positive, "negative": negative, "positiveCount": len(positive), "negativeCount": len(negative), "inputPreserved": before == after}


def run_capture() -> None:
    if (OUT / "SHA256SUMS").exists():
        raise EvidenceError("capture destination is sealed; refusing overwrite")
    if OUT.exists() and any(p.name not in {"replay.py", "intake.md", "report.md", "execution.log", "nested-fields.json", "replay-result.json"} for p in OUT.iterdir()):
        raise EvidenceError("capture destination contains generated payloads; refusing overwrite")
    OUT.mkdir(parents=True, exist_ok=True)
    logger = Logger(OUT / "execution.log", truncate=not (OUT / "execution.log").exists())
    try:
        logger.event("assignment", {"prompt": "cc-prompt-iteration03.md", "introducingCommit": INTRODUCING_COMMIT, "promptSha256": PROMPT_SHA, "context": "separate CC execution context; no exposed session identifier"})
        env = preflight(logger)
        matrix, matrix_summary = matrix_queries(logger)
        extraction = run_extractor(logger)
        inventory = build_inventory(extraction, matrix)
        semantic = validate_semantics(inventory, inventory)
        baseline = read_json(BASELINE)
        replay = harness_result(logger)
        replay_check = compare_replay(replay, baseline, baseline)
        write_json(OUT / "nested-fields.json", inventory)
        write_json(OUT / "replay-result.json", replay)
        logger.event("capture-summary", {"environment": env, "matrixQueries": matrix_summary, "sourceDeclarations": len(extraction["declarations"]), "sourceMemberCount": semantic["freshMemberCount"], "replay": replay_check})
        logger.close()
        # Intake/report are authored after the measured capture.  A later
        # explicit --seal freezes all seven payloads together.
        if (OUT / "intake.md").exists() and (OUT / "report.md").exists():
            seal(OUT)
    except Exception as exc:
        logger.event("capture-failure", {"error": repr(exc)})
        logger.close()
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--seal", action="store_true")
    parser.add_argument("--packet", type=Path, default=OUT)
    args = parser.parse_args()
    modes = sum(bool(x) for x in (args.capture, args.verify, args.self_test, args.seal))
    if modes != 1:
        parser.error("choose exactly one of --capture, --verify, --self-test")
    packet = args.packet.resolve()
    if args.capture:
        run_capture()
        return 0
    if args.seal:
        if not (OUT / "intake.md").exists() or not (OUT / "report.md").exists():
            raise EvidenceError("cannot seal before intake.md and report.md exist")
        seal(packet)
        verify_manifest(packet)
        return 0
    if args.verify:
        result = validate_packet(packet)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    result = self_test(packet)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EvidenceError as exc:
        print(f"evidence-driver: {exc}", file=sys.stderr)
        raise SystemExit(2)
