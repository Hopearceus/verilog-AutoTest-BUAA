import pathlib

from blocks import Blocks


class LayerTree:

    def __init__(self, level, instruction, parent=None):
        self.child: [LayerTree] = []
        self.parent: LayerTree = parent
        self.level: int = level
        self.instruction: str = instruction

    def insert_child(self, child):
        self.child.append(child)
        child.parent = self

    @staticmethod
    def calc_level(s: str) -> int:
        count = 0
        for c in s:
            if c != ' ':
                break
            count += 1
        return count // 4


def parser(lines: [str]):
    cur_level = -1
    root = LayerTree(cur_level, "")
    stack = [root]
    for line in lines:
        level = LayerTree.calc_level(line)
        if level == cur_level:
            cur_node = LayerTree(level, line)
            stack[-1].parent.insert_child(cur_node)
            stack[-1] = cur_node
        elif level == cur_level + 1:
            cur_node = LayerTree(level, line)
            stack[-1].insert_child(cur_node)
            stack.append(cur_node)
            cur_level = level
        elif level < cur_level:
            for _ in range(cur_level - level):
                stack.pop()
            cur_node = LayerTree(level, line)
            stack[-1].parent.insert_child(cur_node)
            stack[-1] = cur_node
            cur_level = level
        else:
            raise Exception("Template syntax error @ " + line)

    return walk_tree(root)


def walk_tree(root: LayerTree):
    if root.instruction == "":
        return "".join([walk_tree(child) for child in root.child])
    tokens = root.instruction.split()
    if not tokens or tokens[0] not in Blocks:
        raise Exception("Template syntax error @ " + root.instruction)
    kwargs = {}
    insert = ""
    for kv in tokens[1:]:
        try:
            kwargs[kv.split('=')[0]] = kv.split('=')[1]
        except IndexError:
            raise Exception("Template syntax error @ " + root.instruction)
    for child in root.child:
        insert += walk_tree(child)
    return Blocks[tokens[0]].spawn(insert, **kwargs)


if __name__ == "__main__":
    template_file = pathlib.Path("templates/Extreme.DataMemoryThrough.template")
    output_file = pathlib.Path("temporary/out.asm")

    lines = [s for s in template_file.read_text().split('\n') if len(s.strip()) > 0]
    output_file.write_text(parser(lines))
