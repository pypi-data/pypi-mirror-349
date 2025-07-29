
# Convert Markdown to Tree (Dictonary)

 This module is going to convert markdown(.md) file into tree-structure-object.
The tree object will be exported as treelib, which is defined on this repository (<https://github.com/caesar0301/treelib>)

## Set Up

```bash

poetry add git+https://github.com/kevin-tofu/md2tree.git

```

## Usage

### How to convert markdown file into treelib

```python

import md2tree

tree = md2tree.file2tree(
    'README.md'
)
print(tree)

md2tree.tree2file(
    './tree.json',
    tree,
    'root'
)

```

### print function shows graph structure like below using treelib

```txt

root
└── Convert Markdown to Tree (Dictonary)
    ├── Set Up
    └── Usage
        └── Functions

```

### The function 'md2tree.tree2file' exports graph with data as json file

```txt

{
  "name": "root",
  "data": null,
  "children": [
    {
      "name": "1",
      "data": {
        "title": "Convert Markdown to Tree (Dictonary)",
        "texts": [
          "\n",
          " This module is going to convert markdown(.md) file into tree-structure-object.\n",
          "\n"
        ]
      },
...

```

## Functions

| Functions | Description |
| --- | --- |
| file2tree |  |
| lines2tree |  |
| tree2dict |  |
| tree2file |  |

