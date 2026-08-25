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

# Use the command line

Invoke the installed plugin through the Transpiler-Mate runtime:

```console
transpiler-mate cwl2codemeta [OPTIONS] SOURCE
```

For example:

```console
transpiler-mate cwl2codemeta \
  --code-repository https://gitlab.com/example/hello.git \
  --output build/codemeta.json \
  hello.cwl
```

`SOURCE` is a CWL document location understood by the installed runtime. Its
document-level Schema.org metadata must satisfy the Transpiler-Mate
`SoftwareApplication` model.

## Plugin options

| Option | Required | Default | Description |
| --- | --- | --- | --- |
| `--code-repository TEXT` | Yes | — | Git repository URL used to build a `SoftwareSourceCode` wrapper. |
| `--output PATH` | No | `codemeta.json` | Destination for the CodeMeta JSON-LD document. |

The runtime may expose additional source-access options, such as OCI or OAuth
credentials. Run the installed command's help to see its complete interface:

```console
transpiler-mate cwl2codemeta --help
```

The destination's parent directory must already exist. An existing output file
is replaced.

## Repository enrichment

For GitHub repositories, the plugin derives the Actions, issues, wiki,
releases, and deployments URLs. For GitLab repositories, it derives the
pipelines and issues URLs plus related wiki, packages, and pipelines links.
Other Git platforms still produce `codeRepository`, but the plugin does not
currently derive additional platform links.
