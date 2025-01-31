from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

if TYPE_CHECKING:
    from markdown import Markdown


MERMAID_CODEBLOCK_START = re.compile(r"^(?P<code_block_sign>[\~\`]{3})[Mm]ermaid\s*$")
MERMAID_JS_SCRIPT = """
<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
</script>
"""


def add_mermaid_script_and_tag(lines: list[str]) -> list[str]:
    result_lines: list[str] = []
    in_mermaid_codeblock: bool = False
    exist_mermaid_codeblock: bool = False

    codeblock_end_pattern = re.compile("```")
    for line in lines:
        if in_mermaid_codeblock:
            match_codeblock_end = codeblock_end_pattern.match(line)
            if match_codeblock_end:
                in_mermaid_codeblock = False
                result_lines.append("</div>")
                continue

        match_mermaid_codeblock_start = MERMAID_CODEBLOCK_START.match(line)
        if match_mermaid_codeblock_start:
            exist_mermaid_codeblock = True
            in_mermaid_codeblock = True
            codeblock_sign = match_mermaid_codeblock_start.group("code_block_sign")
            codeblock_end_pattern = re.compile(rf"{codeblock_sign}\s*")
            result_lines.append('<div class="mermaid">')
            continue

        result_lines.append(line)

    if exist_mermaid_codeblock:
        result_lines.extend(MERMAID_JS_SCRIPT.split("\n"))
    return result_lines


class MermaidPreprocessor(Preprocessor):
    def run(self, lines: list[str]) -> list[str]:
        return add_mermaid_script_and_tag(lines)


class MermaidExtension(Extension):
    """Add source code highlighting to markdown codeblocks."""

    def extendMarkdown(self, md: Markdown) -> None:
        """Add HilitePostprocessor to Markdown instance."""
        # Insert a preprocessor before ReferencePreprocessor
        md.preprocessors.register(MermaidPreprocessor(md), "mermaid", 35)
        md.registerExtension(self)


def makeExtension(**kwargs: dict[str, Any]) -> MermaidExtension:
    return MermaidExtension(**kwargs)
