[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)
[![Github Actions](https://github.com/Lee-W/markdown-mermaidjs/actions/workflows/python-check.yaml/badge.svg)](https://github.com/Lee-W/markdown-mermaidjs/actions/workflows/python-check.yaml)
[![PyPI Package latest release](https://img.shields.io/pypi/v/markdown-mermaidjs.svg?style=flat-square)](https://pypi.org/project/markdown-mermaidjs/)
[![PyPI Package download count (per month)](https://img.shields.io/pypi/dm/markdown-mermaidjs?style=flat-square)](https://pypi.org/project/markdown-mermaidjs/)
[![Supported versions](https://img.shields.io/pypi/pyversions/markdown-mermaidjs.svg?style=flat-square)](https://pypi.org/project/markdown-mermaidjs/)

# markdown-mermaidjs

Python-Markdown extension to add Mermaid graph

## Getting Started

### Prerequisites

* [Python](https://www.python.org/downloads/)

## Installation

For `pip` installation (only python version >=3.x) :

```shell
pip install markdown-mermaidjs
```

## Usage

### With Python Script

```python
import markdown


text = """
# Title

Some text.

​```mermaid
graph TB
    A --> B
    B --> C
​```

Some other text.

​```mermaid
graph TB
    D --> E
    E --> F
​```
"""

html = markdown.markdown(text, extensions=["markdown-mermaidjs"])

print(html)
```

Expected output

```html
<h1>Title</h1>
<p>Some text.</p>
<pre class="mermaid">
graph TB
    A --> B
    B --> C
</pre>

<p>Some other text.</p>
<pre class="mermaid">
graph TB
    D --> E
    E --> F
</pre>

<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
</script>
```

### Adding Custom Icon Packs

Some newer MermaidJS diagram types (most notably [Architecture](https://mermaid.js.org/syntax/architecture.html)),
support referencing custom icon packs that are registered (i.e. https://mermaid.js.org/config/icons.html).

To register packs, you can add them to the extension config with a structure of ```icon_packs: {"pack_name" : "pack_url" }```, i.e.:

```python
import markdown

html = markdown.markdown(
    text,
    extensions=["markdown-mermaidjs"],
    extension_configs={
        "markdown_mermaidjs": {
            "icon_packs": {
                "logos": "https://unpkg.com/@iconify-json/logos@1/icons.json",
                "hugeicons": "https://unpkg.com/@iconify-json/hugeicons@1/icons.json",
            }
        }
    },
)
```

The resulting HTML should be nearly identical, but the icon packs should be registered, e.g.:

```html
<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.registerIconPacks([
        { name: 'logos', loader: () => fetch('https://unpkg.com/@iconify-json/logos@1/icons.json').then((res) => res.json()) },
        { name: 'hugeicons', loader: () => fetch('https://unpkg.com/@iconify-json/hugeicons@1/icons.json').then((res) => res.json()) }
    ]);
    mermaid.initialize({ startOnLoad: true });
</script>
```

### Use it with [Pelican](https://getpelican.com/)

Add `"markdown_mermaidjs": {}` to `MARKDOWN["extension_configs"]` in your `pelicanconf.py`.
For the default `MARKDOWN` configuration, it will look like the string below:

```python
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown_mermaidjs": {},  # <------ Our addition!
    },
    "output_format": "html5",
}
```

#### Icon Packs via Pelican

Similarly, with the extension config, you can add it in the `pelicanconf.py`.

```python
MARKDOWN = {
    "extension_configs": {
        "markdown_mermaidjs": {
            "icon_packs": {
                "logos": "https://unpkg.com/@iconify-json/logos@1/icons.json",
                "hugeicons": "https://unpkg.com/@iconify-json/hugeicons@1/icons.json",
            }
        },
    },
}
```

## Contributing

See [Contributing](contributing.md)

## Authors

Wei Lee <weilee.rx@gmail.com>

This is a forked project of [oruelle/md_mermaid](https://github.com/oruelle/md_mermaid)

Created from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/3.0.0) version 3.0.0
