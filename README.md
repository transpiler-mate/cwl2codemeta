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

[![PyPI - Version](https://img.shields.io/pypi/v/cwl2codemeta.svg)](https://pypi.org/project/cwl2codemeta)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cwl2codemeta.svg)](https://pypi.org/project/cwl2codemeta)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/transpiler-mate/cwl2codemeta/package.yaml?branch=develop&event=push&label=build&logo=githubactions)](https://github.com/transpiler-mate/cwl2codemeta/actions/workflows/package.yaml?query=branch%3Adevelop)
[![Code coverage](https://img.shields.io/codecov/c/github/transpiler-mate/cwl2codemeta/develop?logo=codecov)](https://app.codecov.io/gh/transpiler-mate/cwl2codemeta/tree/develop)

`cwl2codemeta` is a Transpiler-Mate plugin that converts Schema.org metadata
embedded in a Common Workflow Language (CWL) document into a CodeMeta 3.0
JSON-LD document.

The Transpiler-Mate runtime loads the CWL document and validates its
document-level metadata as a Schema.org `SoftwareApplication`. This plugin
then compacts the Schema.org terms and writes `codemeta.json`.

When a source repository is supplied, the output is a
`SoftwareSourceCode` object whose `targetProduct` contains the CWL software
metadata. GitHub and GitLab repository URLs are also used to derive links for
continuous integration, issue tracking, and related project pages.

## Installation

Install the plugin and a compatible Transpiler-Mate runtime in the same Python
environment:

```console
python -m pip install cwl2codemeta transpiler-mate-runtime
```

The package registers the `cwl2codemeta` plugin through the
`transpiler_mate.plugins` entry-point group. It does not install a standalone
`cwl2codemeta` executable.

## Usage

Your CWL document must carry the Schema.org metadata required by the
Transpiler-Mate `SoftwareApplication` model. Then run:

```console
transpiler-mate cwl2codemeta \
  --code-repository https://github.com/example/hello.git \
  --output codemeta.json \
  hello.cwl
```

Run `transpiler-mate cwl2codemeta --help` for the complete generated command
interface.

## Documentation

Project documentation is published at
<https://Transpiler-Mate.github.io/cwl2codemeta/>. It includes a complete CWL
example, the output contract, and details of the repository enrichment.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Submit issues at
<https://github.com/Transpiler-Mate/cwl2codemeta/issues>.

## License

Licensed under the [Apache License 2.0](LICENSE).
