from __future__ import annotations

from pathlib import Path

import markdown
import pytest

from markdown_mermaidjs.markdown_mermaidjs import MermaidExtension, MermaidPreprocessor

data_dir = Path("tests/data")


@pytest.mark.parametrize(
    "input_file_path", [data_dir / "test_1.md", data_dir / "test_2.md"]
)
def test_add_mermaid_script_and_tag(data_regression, input_file_path):
    with open(input_file_path) as input_file:
        lines = input_file.readlines()

    mermaid_preprocessor = MermaidPreprocessor(MermaidExtension())

    result_lines = mermaid_preprocessor.add_mermaid_script_and_tag(lines)
    data_regression.check("\n".join(result_lines))


def test_configure_icon_packs():
    mermaid_extension = MermaidExtension(
        icon_packs={"logos": "https://unpkg.com/@iconify-json/logos@1/icons.json"}
    )
    assert mermaid_extension.icon_packs == {
        "logos": "https://unpkg.com/@iconify-json/logos@1/icons.json"
    }


def test_configure_icon_packs_default():
    mermaid_extension = MermaidExtension()
    assert mermaid_extension.icon_packs == {}


@pytest.mark.parametrize(
    ("input_icon_packs", "expected_output"),
    [
        (
            {"logos": "https://unpkg.com/@iconify-json/logos@1/icons.json"},
            {"logos": "https://unpkg.com/@iconify-json/logos@1/icons.json"},
        ),
        (
            {
                "logos": "https://unpkg.com/@iconify-json/logos@1/icons.json",
                "hugeicons": "https://unpkg.com/@iconify-json/hugeicons@1/icons.json",
            },
            {
                "logos": "https://unpkg.com/@iconify-json/logos@1/icons.json",
                "hugeicons": "https://unpkg.com/@iconify-json/hugeicons@1/icons.json",
            },
        ),
        (None, {}),
    ],
)
def test_extension_configuration_icon_packs(input_icon_packs, expected_output):
    mermaid_extension = MermaidExtension(icon_packs=input_icon_packs)

    markdown_instance = markdown.Markdown(extensions=[mermaid_extension])

    mermaid_preprocessor = markdown_instance.preprocessors[0]
    assert mermaid_preprocessor.icon_packs == expected_output

    markdown_instance2 = markdown.Markdown(
        extensions=["markdown_mermaidjs"],
        extension_configs={"markdown_mermaidjs": {"icon_packs": input_icon_packs}},
    )

    mermaid_preprocessor2 = markdown_instance2.preprocessors[0]
    assert mermaid_preprocessor2.icon_packs == expected_output


@pytest.mark.parametrize(
    "input_file_path", [data_dir / "test_icons_1.md", data_dir / "test_icons_2.md"]
)
def test_add_mermaid_script_and_tag_with_icons(data_regression, input_file_path):
    with open(input_file_path) as input_file:
        lines = input_file.readlines()

    markdown_instance = markdown.Markdown(
        extensions=["markdown_mermaidjs"],
        extension_configs={
            "markdown_mermaidjs": {
                "icon_packs": {
                    "logos": "https://unpkg.com/@iconify-json/logos@1/icons.json"
                }
            }
        },
    )
    mermaid_preprocessor = MermaidPreprocessor(
        md=markdown_instance,
        icon_packs={"logos": "https://unpkg.com/@iconify-json/logos@1/icons.json"},
    )

    result_lines = mermaid_preprocessor.add_mermaid_script_and_tag(lines)
    data_regression.check("\n".join(result_lines))
