<!--
Copyright 2026 Transpiler-Mate

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Conversion architecture

`cwl2codemeta` operates on metadata prepared by a Transpiler-Mate host. It does
not parse the CWL source itself.

The conversion has four stages:

1. The runtime resolves the CWL document and preserves its document-level
   metadata.
2. The runtime expands the prefixes declared in `$namespaces` and validates
   the result as a Schema.org `SoftwareApplication`.
3. The plugin optionally wraps that application in a Schema.org
   `SoftwareSourceCode` object built from `code_repository`.
4. PyLD compacts the full-IRI Schema.org representation with the Schema.org
   vocabulary and the plugin replaces the JSON-LD context with the CodeMeta
   3.0 context before serializing it.

```text
CWL document
  └─ document-level Schema.org metadata
       └─ Transpiler-Mate SoftwareApplication
            └─ optional SoftwareSourceCode repository wrapper
                 └─ JSON-LD compaction + CodeMeta 3.0 context
                      └─ codemeta.json
```

## Why the terms can be compacted

CodeMeta uses Schema.org as its base vocabulary and defines a profile for
describing software. The normalized model serializes properties as full IRIs,
such as `https://schema.org/softwareVersion`. Compacting with
`https://schema.org/` as `@vocab` turns that IRI into `softwareVersion`; setting
`https://w3id.org/codemeta/3.0` as `@context` makes the resulting document a
CodeMeta 3.0 JSON-LD document.

## Repository wrapper

When `code_repository` is set, the source repository and the runnable software
are represented separately:

- the top-level `SoftwareSourceCode` describes the repository;
- `targetProduct` contains the `SoftwareApplication` extracted from CWL;
- GitHub or GitLab URLs add platform-specific CI, issue, and related links.

Without a repository, direct API callers may pass `None` and receive the
`SoftwareApplication` as the top-level CodeMeta object. The generated CLI
currently requires `--code-repository` because the option has no model default.

## Keyword handling

The metadata model permits textual keywords, URLs, and `DefinedTerm` objects.
The plugin currently writes only string entries from a keyword list into the
final compacted document. Non-string list entries are omitted.
