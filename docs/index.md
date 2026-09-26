<!--
Copyright 2026 Terradue

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

# CWL to CodeMeta

`cwl2codemeta` converts Schema.org metadata embedded at the document level of
a CWL file into a CodeMeta 3.0 JSON-LD document.

The package is a Transpiler-Mate plugin, not a standalone command. Once it is
installed alongside the Transpiler-Mate runtime, it is available as the
`cwl2codemeta` subcommand:

```console
transpiler-mate cwl2codemeta \
  --code-repository https://github.com/example/hello.git \
  --output codemeta.json \
  hello.cwl
```

The output uses the CodeMeta 3.0 context:

```json
{
  "@context": "https://w3id.org/codemeta/3.0",
  "@type": "SoftwareSourceCode",
  "codeRepository": "https://github.com/example/hello.git",
  "targetProduct": {
    "@type": "SoftwareApplication",
    "name": "Hello tool",
    "softwareVersion": "1.0.0"
  }
}
```

The actual `targetProduct` contains all supported metadata supplied by the CWL
document. GitHub and GitLab repository URLs also produce platform-specific
project links.

## Choose your path

- [Convert your first CWL document](tutorials/first-steps.md).
- [Install the plugin](how-to/install.md) or look up the
  [command options](how-to/use-cli.md).
- Consult the exact [plugin API](reference/api.md).
- Understand the [conversion pipeline](explanation/architecture.md).
