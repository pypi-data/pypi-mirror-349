import re
from typing import Optional

def parse_heading(line: str) -> Optional[dict]:
    match = re.match(r'^(#+)\s+(.*)$', line)
    if match:
        depth = len(match.group(1))
        title = match.group(2)
        return {'type': 'heading', 'depth': depth, 'title': title}
    else:
        return None


def parse_line(line: str | None) -> Optional[dict]:

    if line is None:
        return None
    
    match_list = re.match(r'^(\s*)[*+-]\s+(.*)$', line)
    match_table = re.findall(r'\|[^|]*\|', line)

    if match_list:
        indent = len(match_list.group(1))
        text = match_list.group(2)
        return {'type': 'list_item', 'indent': indent, 'text': text}
    elif match_table:
        row = [cell.strip() for cell in line.strip('|').split('|')]
        return {'type': 'table_row', 'row': row}
    else:
        return None


def parse_paragraph(lines: list[str]) -> dict:
    # print(type(lines[0]))
    text = ''.join(lines)  #.strip()
    return {'type': 'paragraph', 'text': text}


def parse_table(
    lines: list[str]
) -> Optional[dict]:

    lines_temp = [remove_rn(l) for l in lines if l[0] == '|']
    if len(lines_temp) < 3:
        return None

    # header = [cell.strip() for cell in lines_temp[0].strip('|').split('|')]
    # divider = [cell.strip() for cell in lines_temp[1].strip('|').split('|')]
    header = lines_temp[0].split("|")[1:-1]
    divider = lines_temp[1].replace(' ', '').split("|")[1:-1]

    # Ensure that the divider contains only dashes or pipes
    if any(c not in '-| ' for cell in divider for c in cell):
        return None

    # Ensure that the number of cells in the header and divider are the same
    if len(header) != len(divider):
        return None

    # Store the table data in a dictionary
    rows = []
    for row in lines_temp[2:]:
        cells = row.split("|")[1:-1]
        # Ensure that all rows have the same number of cells as the header
        if len(cells) != len(header):
            return None
        
        rows.append(cells)

    return {'type': 'table', 'header': header, 'rows': rows}


def extract(s: str):
    num_spaces = len(s) - len(s.lstrip())
    str_after_dash = s.split('- ')[1]
    return num_spaces, str_after_dash


def remove_rn(s: str):
    if s.endswith("\n"):
        return s[:-1]
    else:
        return s


def parse_list(
    lines: list[str]
):
    ret = list()
    for line in lines:
        indent, text = extract(line)
        ret.append(
            dict(
                indent=indent,
                text=remove_rn(text)
            )
        )
        
    return {'type': 'list', 'list': ret}


def str2dict(
    lines: list[str]
)-> list[dict]:
    
    ret = list()
    lines_current = list()
    for loop, line in enumerate(lines):

        # print(loop, line)
        line_prev = lines[loop-1] if loop > 0 else None
        line_next = lines[loop+1] if loop < len(lines) - 2 else None

        node = parse_line(line)
        node_prev = parse_line(line_prev)
        node_next = parse_line(line_next)
        # if node := parse_line(line):
        if node is None:
            lines_current.append(line)
            continue
        
        else:
            if node_prev is None:
                temp = parse_paragraph(lines_current)
                ret.append(temp)
                lines_current = list()

            lines_current.append(line)
            if node_next is None:
                # print('lines_current:', lines_current)
                # return {'type': 'list_item', 'indent': indent, 'text': text}
                # return {'type': 'table_row', 'row': row}
                if node['type'] == 'list_item':
                    temp = parse_list(lines_current)
                elif node['type'] == 'table_row':
                    temp = parse_table(lines_current)
                
                if temp is not None:
                    ret.append(temp)

                lines_current = list()

    temp = parse_paragraph(lines_current)
    ret.append(temp)
    return ret


if __name__ == '__main__':

    test0 = [
        "\n",
        "| Functions | Description |\n",
        "| --- | --- |\n",
        "| file2tree |  |\n",
        "| lines2tree |  |\n",
        "| tree2dict |  |\n",
        "| tree2file |  |\n",
        "\n"
    ]


    ret0 = str2dict(test0)
    print('ret0:')
    print(ret0)


    test1 = [
        "sentence0-0\n",
        "sentence0-1\n",
        "sentence0-2\n",
        "- list0\n",
        "- list1\n",
        "- list2\n",
        "\n",
        "sentence1-0\n",
        "sentence1-1\n",
        "sentence1-2\n",
    ]

    # for t in test1:
        # print(t.replace('\n', '\\n'))


    ret1 = str2dict(test1)
    print('ret1:')
    print(ret1)