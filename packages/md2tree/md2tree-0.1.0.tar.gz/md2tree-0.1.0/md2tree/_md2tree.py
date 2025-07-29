import sys
import pathlib
print(__name__)

from .parse import str2dict, parse_heading
import treelib



def create_tree(
    node_list: list[dict],
    text_list: list[list[str]],
    text2node: bool = True,
    tag_is_title: bool=True
) -> treelib.Tree:

    mytree = treelib.Tree()
    mytree.create_node('root', 'root')
    idx_prev = 'root'
    index_list = range(len(node_list))
    # print(node_list)
    depth_prev = node_list[0]['depth']
    _node_list = node_list[1::]

    idx2tags = dict(root=idx_prev)
    for i, node, text in zip(index_list[1::], node_list[1::], text_list[1::]):

        idx = str(i)
        
        idx2tags[idx] = idx if node['title'] == '' or not 'title' in node.keys() else node['title']
        # print('node-title:', node)
        # print('text:', text)
        if text2node:
            data = dict(
                title=node['title'],
                objects=str2dict(text)
            )
        else:
            data = dict(
                title=node['title'],
                texts=text
            )
        if depth_prev + 1 <= node['depth']:
            idx_parent = idx_prev

        elif depth_prev >= node['depth']:
            _idx = None
            for j in range(len(_node_list[0:i])-1, -1, -1):
                if _node_list[j]['depth'] < node['depth']:
                    _idx = j+1  #
                    break
            idx_parent = str(_idx) if _idx is not None else 'root'

        else:
            raise ValueError('err')

        if tag_is_title:
            mytree.create_node(
                tag=idx2tags[idx],
                identifier=idx2tags[idx],
                parent=idx2tags[idx_parent],
                data=data
            )
        else:
            mytree.create_node(
                tag=idx,
                identifier=idx,
                parent=idx_parent,
                data=data
            )
        depth_prev = node['depth']
        idx_prev = idx

    return mytree


def lines2tree(
    lines: list[str],
    text2node: bool = True
) -> treelib.Tree:
    
    current_lines = list()
    node_list = list()
    text_list = list()
    
    depth_prev = dict(
        type='heading',
        depth=0,
        text=''   
    )
    node_list.append(depth_prev)

    for i, line in enumerate(lines):

        idx = str(i)
        if node := parse_heading(line):
            # print(node)
            node_list.append(node)
            text_list.append(current_lines)
            current_lines = list()

        else:
            current_lines.append(line)
    
    text_list.append(current_lines)
    mytree = create_tree(
        node_list,
        text_list,
        text2node=text2node
    )
    
    return mytree


def file2tree(
    file_path: pathlib.Path,
    text2node: bool = True
) -> treelib.Tree:
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # print(type(lines), type(lines[0]))
    # for i, line in enumerate(lines):
        # print(i, line)

    return lines2tree(lines, text2node=text2node)

