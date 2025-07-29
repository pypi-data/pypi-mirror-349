import json
import treelib

def tree2dict(tree:treelib.Tree, root_node_name: str='root') -> dict:
    
    tree_id = tree.identifier
    node = tree[root_node_name]
    n_children = node.successors(tree_id)

    if node.data is None:
        name = node.identifier
    else:
        name = node.data['title'] if node.data['title'] is not None else None

    # print('name', name)
    d = dict(
        name=name,
        data=node.data,
        children=list()
    )
    if name != node.identifier and name != '':
        # d[name] = name
        d['id'] = node.identifier

    for nc_name in n_children:
        d['children'].append(
            tree2dict(tree, nc_name)
        )
    
    return d

def tree2file(
    path_export: str,
    tree:treelib.Tree,
    root_node_name: str='root',
    indent: int=2
):
    with open(path_export, 'w') as f:
        json.dump(tree2dict(tree, root_node_name), f, indent=indent)
