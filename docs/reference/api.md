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

# Plugin API

The plugin registration and its options model are defined in
`cwl2codemeta.plugin`.

## Registration

```python
from cwl2codemeta.plugin import cwl2codemeta
```

| Attribute | Value |
| --- | --- |
| Entry-point group | `transpiler_mate.plugins` |
| Entry-point name | `cwl2codemeta` |
| Entry-point object | `cwl2codemeta.plugin:cwl2codemeta` |
| Registration name | `cwl2codemeta` |
| Options model | `CWL2CodeMetaOptions` |
| Execution return value | `None` |

`cwl2codemeta` is a `PluginRegistration`, not a plain conversion function.
Invoke it directly with `cwl2codemeta.execute(context, options)` or let a
Transpiler-Mate host invoke it.

## Options

```python
from cwl2codemeta.plugin import CWL2CodeMetaOptions
```

| Field | Type | Model default | Meaning |
| --- | --- | --- | --- |
| `code_repository` | `str \| None` | Required | Repository URL used for `SoftwareSourceCode` metadata; `None` disables the wrapper for direct API calls. |
| `output` | `pathlib.Path` | `codemeta.json` | JSON-LD file written by the plugin. |

Unknown fields are forbidden. Because `code_repository` has no default, the
generated CLI exposes `--code-repository` as required even though direct API
callers can explicitly provide `None`.

## Input contract

The plugin reads `context.metadata`, which must be a normalized
`SoftwareApplication` supplied by the host. The current model requires these
Schema.org properties:

- `name`
- `description`
- `dateCreated`
- `license`
- `softwareVersion`
- `softwareHelp`
- `publisher`
- `author`

The plugin serializes the model with Schema.org aliases, excludes properties
whose value is `None`, and converts the result through JSON-LD compaction.

## Output contract

The output is indented JSON with `@context` set to
`https://w3id.org/codemeta/3.0`.

When `code_repository` is a string, the top-level `@type` is
`SoftwareSourceCode` and `targetProduct` contains the input
`SoftwareApplication`. With an explicit `None`, the top-level object remains a
`SoftwareApplication`.

GitHub and GitLab URLs receive derived `continuousIntegration`, `issueTracker`,
and `relatedLink` properties. Other recognized Git URL forms are normalized to
HTTPS when supported by `giturlparse`, but do not receive derived links.

## Errors

Any exception raised while parsing the repository, converting JSON-LD, opening
the destination, or serializing the document is wrapped in
`PluginExecutionError`, with the original exception chained as `__cause__`.

## Python API details

::: cwl2codemeta.plugin
