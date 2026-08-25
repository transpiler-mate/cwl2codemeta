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

# Convert your first CWL document

This tutorial converts the document-level Schema.org metadata in a small CWL
tool into CodeMeta JSON-LD.

## 1. Install the runtime and plugin

Create and activate a virtual environment, then install both packages:

```console
python -m venv .venv
source .venv/bin/activate
python -m pip install cwl2codemeta transpiler-mate-runtime
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1` instead.

Confirm that the runtime discovered the plugin:

```console
transpiler-mate cwl2codemeta --help
```

## 2. Create a metadata-bearing CWL file

Save the following as `hello.cwl`:

```yaml
cwlVersion: v1.2
class: CommandLineTool
$namespaces:
  s: https://schema.org/
s:name: Hello tool
s:description: Print a greeting
s:dateCreated: "2026-08-24"
s:license: https://spdx.org/licenses/Apache-2.0
s:softwareVersion: 1.0.0
s:softwareHelp:
  s:name: Hello tool documentation
  s:url: https://example.org/hello/help
s:publisher:
  s:name: Example organization
s:author:
  s:givenName: Ada
  s:familyName: Lovelace
  s:email: ada@example.org
  s:affiliation:
    s:name: Example organization
$graph:
  - id: hello
    class: CommandLineTool
    baseCommand: echo
    inputs:
      message:
        type: string
        default: Hello, world!
        inputBinding:
          position: 1
    outputs: []
```

The `$namespaces` entry defines the `s` prefix. The `s:*` properties sit at
the document level around `$graph`, which lets the runtime preserve and
normalize them separately from the CWL process itself.

## 3. Generate `codemeta.json`

Run the plugin through Transpiler-Mate:

```console
transpiler-mate cwl2codemeta \
  --code-repository https://github.com/example/hello.git \
  --output codemeta.json \
  hello.cwl
```

The command validates the metadata, enriches it with repository links, and
writes `codemeta.json`. Its top-level structure is:

```json
{
  "@context": "https://w3id.org/codemeta/3.0",
  "@type": "SoftwareSourceCode",
  "codeRepository": "https://github.com/example/hello.git",
  "continuousIntegration": "https://github.com/example/hello/actions",
  "issueTracker": "https://github.com/example/hello/issues",
  "relatedLink": [
    "https://github.com/example/hello/wiki",
    "https://github.com/example/hello/releases",
    "https://github.com/example/hello/deployments"
  ],
  "targetProduct": {
    "@type": "SoftwareApplication",
    "name": "Hello tool",
    "description": "Print a greeting",
    "softwareVersion": "1.0.0"
  }
}
```

The shortened example omits some `targetProduct` properties for readability;
the generated file also contains the license, creation date, help, publisher,
and author from the CWL metadata.

## Next steps

- Review all [command options](../how-to/use-cli.md).
- Learn how the [conversion pipeline](../explanation/architecture.md) preserves
  Schema.org semantics while changing the JSON-LD context.
