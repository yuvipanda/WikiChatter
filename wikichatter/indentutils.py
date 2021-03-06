import mwparserfromhell as mwp


def extract_indent_blocks(text):
    old_indent = 0
    block_list = []
    cur_block_lines = []
    for line in text.split('\n'):
        indent = find_line_indent(line)
        if indent != old_indent and line.strip() != "":
            block = "\n".join(cur_block_lines)
            if block.strip() != "":
                block_list.append(block)
            cur_block_lines = []
            old_indent = indent
        cur_block_lines.append(line)
    block = "\n".join(cur_block_lines)
    if block.strip() != "":
        block_list.append(block)
    return block_list


def find_min_indent(text):
    lines = text.split('\n')
    non_empty = [line for line in lines if line.strip() != ""]
    indents = [find_line_indent(line) for line in non_empty]
    return min(indents)


def find_line_indent(line):
    return _count_indent_in_some_order(line)


def _count_indent_in_some_order(line):
    line = line.strip()
    count = 0
    indent_chars = [':', '*', '#']
    while len(indent_chars) > 0:
        if len(line) > count and line[count] in indent_chars:
            char = line[count]
            count += _count_leading_char(line[count:], line[count])
            indent_chars.remove(char)
        else:
            break
    return count


def _count_leading_char(line, char):
    line = line.strip()
    if len(line) == 0 or line[0] != char:
        return 0
    else:
        return 1 + _count_leading_char(line[1:], char)


def has_continuation_indent(text):
    wikicode = mwp.parse(text, skip_style_tags=True)
    templates = wikicode.filter_templates()
    if len(templates) > 0:
        potential_cont = str(templates[0])
        if text.startswith(potential_cont):
            if "outdent" in potential_cont:
                return True
    return False
