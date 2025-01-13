from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

if TYPE_CHECKING:
    from markdown import Markdown


class MermaidPreprocessor(Preprocessor):
    MERMAID_CODEBLOCK_START = re.compile(
        r"^(?P<code_block_sign>[\~\`]{3})[Mm]ermaid\s*$"
    )

    def __init__(self, md: Markdown, icon_packs: dict | None = None) -> None:
        self.icon_packs = icon_packs
        super().__init__(md)

    @property
    def icon_packs_calls(self) -> list[str]:
        return (
            [
                f"{{ name: '{name}', loader: () => fetch('{url}').then((res) => res.json()) }}"
                for name, url in self.icon_packs.items()
            ]
            if self.icon_packs
            else []
        )

    def generate_mermaid_init_script(self) -> list[str]:
        icon_packs_calls = ""

        calls = self.icon_packs_calls
        if len(calls):
            callstr = "\n,".join(calls)
            icon_packs_calls = f"""
mermaid.registerIconPacks([
    {callstr}
]);"""

        script_module = f"""
<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';{icon_packs_calls}
    mermaid.initialize({{ startOnLoad: true }});
</script>
"""

        return script_module.split("\n")

    def add_mermaid_script_and_tag(self, lines: list[str]) -> list[str]:
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

            match_mermaid_codeblock_start = self.MERMAID_CODEBLOCK_START.match(line)
            if match_mermaid_codeblock_start:
                exist_mermaid_codeblock = True
                in_mermaid_codeblock = True
                codeblock_sign = match_mermaid_codeblock_start.group("code_block_sign")
                codeblock_end_pattern = re.compile(rf"{codeblock_sign}\s*")
                result_lines.append('<div class="mermaid">')
                continue

            result_lines.append(line)

        if exist_mermaid_codeblock:
            result_lines.extend(self.generate_mermaid_init_script())
        return result_lines

    def run(self, lines: list[str]) -> list[str]:
        return self.add_mermaid_script_and_tag(lines)


class MermaidExtension(Extension):
    """Add mermaid diagram markdown codeblocks."""

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        self.config = {
            "icon_packs": [
                {},
                "Dictionary of icon packs to use: { name(str) : url(str) }.  Default: {} (no icon packs). example: { 'logos' : 'https://unpkg.com/@iconify-json/logos@1/icons.json' } corresponds to the json file example here: https://mermaid.js.org/config/icons.html",
            ],
        }

        super().__init__(**kwargs)

        self.icon_packs: dict[str, str] = {}
        config_packs = (
            self.getConfig("icon_packs", default={}) or {}
        )  # for the None case
        self.icon_packs.update(config_packs)

    def extendMarkdown(self, md: Markdown) -> None:
        """Add MermaidExtension to Markdown instance."""
        # Insert a preprocessor before ReferencePreprocessor

        md.preprocessors.register(
            MermaidPreprocessor(md, icon_packs=self.icon_packs), "mermaid", 35
        )
        md.registerExtension(self)


def makeExtension(**kwargs: dict[str, Any]) -> MermaidExtension:
    return MermaidExtension(**kwargs)
