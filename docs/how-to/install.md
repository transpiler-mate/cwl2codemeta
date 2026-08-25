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

# Install the plugin

## From PyPI

Install `cwl2codemeta` and a compatible Transpiler-Mate runtime into the same
Python environment:

```console
python -m pip install cwl2codemeta transpiler-mate-runtime
```

Verify that plugin discovery succeeded:

```console
transpiler-mate cwl2codemeta --help
```

The package registers a plugin entry point; it does not provide a standalone
`cwl2codemeta` executable.

## From source

```console
git clone https://github.com/Transpiler-Mate/cwl2codemeta.git
cd cwl2codemeta
python -m pip install . transpiler-mate-runtime
```

Python 3.10 or newer is required.
