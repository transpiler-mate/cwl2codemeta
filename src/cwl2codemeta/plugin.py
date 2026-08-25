# Copyright 2026 Transpiler-Mate
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

"""Convert normalized CWL Schema.org metadata to CodeMeta JSON-LD."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any

from giturlparse import GitUrlParsed
from giturlparse import parse as gitparse
from loguru import logger
from pydantic import AnyUrl, BaseModel, ConfigDict, Field
from pyld import jsonld
from transpiler_mate.api import (
    PluginExecutionError,
    SoftwareApplication,
    SoftwareSourceCode,
    transpiler_plugin,
)

if TYPE_CHECKING:
    from collections.abc import MutableMapping

    from transpiler_mate.api import TranspilerContext


class CWL2CodeMetaOptions(BaseModel):
    """Options accepted by the CWL-to-CodeMeta plugin."""

    model_config = ConfigDict(extra="forbid")

    code_repository: Annotated[
        str | None,
        Field(
            default=None,
            description="The (SVN, GitHub, CodePlex, ...) code repository URL",
        ),
    ]

    output: Annotated[
        Path,
        Field(default=Path("codemeta.json"), description="The output file path"),
    ]


@transpiler_plugin(
    name="cwl2codemeta",
    description="Convert CWL Schema.org metadata to CodeMeta 3.0 JSON-LD.",
    options_model=CWL2CodeMetaOptions,
)
def cwl2codemeta(context: TranspilerContext, options: CWL2CodeMetaOptions) -> None:
    """Write normalized CWL software metadata as CodeMeta JSON-LD."""

    metadata: SoftwareApplication | SoftwareSourceCode = context.metadata

    try:
        if options.code_repository:
            logger.debug(
                f"code_repository detected, analyzing: {options.code_repository}"
            )

            parsed_url: GitUrlParsed = gitparse(options.code_repository)

            continuous_integration: str | None = None
            issue_tracker: str | None = None
            related_links: list[str] = []

            logger.debug(f"Creating URLs for Git URL platform: {parsed_url.platform}")

            match parsed_url.platform:
                case "github":
                    continuous_integration = parsed_url.url2https.replace(
                        ".git", "/actions"
                    )
                    issue_tracker = parsed_url.url2https.replace(".git", "/issues")
                    related_links = [
                        parsed_url.url2https.replace(".git", page)
                        for page in ["/wiki", "/releases", "/deployments"]
                    ]

                case "gitlab":
                    continuous_integration = parsed_url.url2https.replace(
                        ".git", "/-/pipelines"
                    )
                    issue_tracker = parsed_url.url2https.replace(".git", "/-/issues")
                    related_links = [
                        parsed_url.url2https.replace(".git", page)
                        for page in ["/-/wikis/home", "/-/packages", "/-/pipelines"]
                    ]

                case _:
                    logger.warning(f"Platform {parsed_url.platform} unsupported yet")

            logger.debug("Rebuilding SoftwareSourceCode...")

            metadata = SoftwareSourceCode(
                code_repository=parsed_url.url2https,
                target_product=context.metadata,
                continuous_integration=AnyUrl(continuous_integration)
                if continuous_integration
                else None,
                issue_tracker=AnyUrl(issue_tracker) if issue_tracker else None,
                related_link=[AnyUrl(related_link) for related_link in related_links],
            )

            logger.debug("SoftwareSourceCode successfully rebuilt.")

        logger.info("Converting CWL Metadata to CodeMeta via JSON-LD conversion...")

        doc: dict[str, Any] = metadata.model_dump(exclude_none=True, by_alias=True)

        compacted: MutableMapping[str, Any] = jsonld.compact(
            doc,
            {"@vocab": "https://schema.org/"},
            options={"processingMode": "json-ld-1.1"},
        )

        compacted["@context"] = "https://w3id.org/codemeta/3.0"

        logger.success("CWL Metadata successfully converted to CodeMeta via JSON-LD!")

        if context.metadata.keywords and isinstance(context.metadata.keywords, list):
            compacted["keywords"] = list(
                filter(
                    lambda keyword: isinstance(keyword, str), context.metadata.keywords
                )
            )
        logger.info(f"Serializing CodeMeta metadata to {options.output.absolute()}")

        with options.output.open("w") as output_stream:
            json.dump(compacted, output_stream, indent=2)

        logger.success(
            f"CodeMeta metadata successfully serialized to {options.output.absolute()}"
        )
    except Exception as e:
        raise PluginExecutionError(
            f"An error occurred when serializing to {options.output.absolute()}, see nested exception"
        ) from e
