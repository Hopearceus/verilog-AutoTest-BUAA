import pathlib
import random

from TemplateParser import parser as template_parser


def list_template():
    def read_template(p: pathlib.Path):
        raw_list = p.read_text().split("\n")
        return [line for line in raw_list if len(line.strip()) > 0]

    template_dct = {}
    name_list = []
    for path in pathlib.Path("templates").rglob("*.template"):
        template_dct[path.name] = read_template(path)
        name_list.append(path.name)
    return template_dct, name_list


def gen_data(count, print_title=True):
    """
    生成供测评的 ASM 语句，返回一个生成器
    :param count: 数据组数
    :param print_title: 是否打印标题信息（默认为 True）
    :return: generator of ((index, template_file_name), asm_str)
    """
    templ_dct, name_lst = list_template()
    cycle, rest = divmod(count, len(name_lst))
    name_lst = name_lst * cycle + random.choices(name_lst, k=rest)
    random.shuffle(name_lst)

    def generator():
        for i, name in enumerate(name_lst):
            if print_title:
                print(f"///// {i + 1} / {count}: {name} /////")
            asm_path = temp_path / "test.asm"
            asm_path.write_text(template_parser(templ_dct[name]))
            yield
    return generator()


if __name__ == "__main__":
    temp_path = pathlib.Path("temporary")
    temp_path.mkdir(exist_ok=True)
    for _ in gen_data(11):
        pass
