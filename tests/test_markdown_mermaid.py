from __future__ import annotations

from pathlib import Path

import pytest

from markdown_mermaidjs.markdown_mermaidjs import add_mermaid_script_and_tag

data_dir = Path("tests/data")


@pytest.mark.parametrize(
    "input_file_path", [data_dir / "test_1.md", data_dir / "test_2.md"]
)
def test_add_mermaid_script_and_tag(data_regression, input_file_path):
    with open(input_file_path) as input_file:
        lines = input_file.readlines()
    result_lines = add_mermaid_script_and_tag(lines)
    data_regression.check("\n".join(result_lines))
