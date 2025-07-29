# from md2tree.md2tree import file2tree, lines2tree
# from md2tree.md2tree.utils.utils import tree2dict, tree2file
# from md2tree.md2tree.parse import str2dict, parse_heading

# __all__ = ['file2tree', 'lines2tree', 'tree2dict', 'tree2file']
# __all__.extend(['str2dict', 'parse_heading'])

from ._md2tree import file2tree, lines2tree, create_tree
from .utils import tree2dict, tree2file
