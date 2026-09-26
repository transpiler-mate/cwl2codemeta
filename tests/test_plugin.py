# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

from cwl2codemeta.plugin import CWL2CodeMetaOptions, cwl2codemeta


class MetadataStub:
    """Supply metadata with mixed keyword values for serialization tests."""

    def __init__(self) -> None:
        self.keywords: list[str | int] = ["workflow", 42]

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return {
            "@type": "https://schema.org/SoftwareApplication",
            "https://schema.org/name": "Example application",
        }


def test_plugin_serializes_compacted_metadata(tmp_path: Any) -> None:
    output = tmp_path / "codemeta.json"
    context: Any = SimpleNamespace(metadata=MetadataStub())

    cwl2codemeta.execute(
        context,
        CWL2CodeMetaOptions(code_repository=None, output=output),
    )

    document = json.loads(output.read_text())
    assert document["@context"] == "https://w3id.org/codemeta/3.0"
    assert document["@type"] == "SoftwareApplication"
    assert document["name"] == "Example application"
    assert document["keywords"] == ["workflow"]
