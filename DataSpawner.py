import pathlib
import random

from TemplateParser import parser as template_parser


def list_template(template_used):
    def read_template(p: pathlib.Path):
        raw_list = p.read_text().split("\n")
        return [line for line in raw_list if len(line.strip()) > 0]

    template_dct = {}
    name_list = []
    if template_used is None:
        for path in pathlib.Path("templates").rglob("*.template"):
            template_dct[path.name] = read_template(path)
            name_list.append(path.name)
    else:
        for path in template_used:
            path = pathlib.Path(path)
            template_dct[path.name] = read_template(path)
            name_list.append(path.name)
    return template_dct, name_list


def gen_data(count, print_title=True, template_used=None):
    """
    生成供测评的 ASM 语句，返回一个生成器
    :param template_used: 允许使用的模板文件列表，None 表示无限制
    :param count: 数据组数
    :param print_title: 是否打印标题信息（默认为 True）
    :return: generator of ((index, template_file_name), asm_str)
    """
    templ_dct, name_lst = list_template(template_used)
    cycle, rest = divmod(count, len(name_lst))
    name_lst = name_lst * cycle + random.choices(name_lst, k=rest)
    random.shuffle(name_lst)

    temp_path = pathlib.Path("temporary")
    temp_path.mkdir(exist_ok=True)

    def generator():
        for i, name in enumerate(name_lst):
            if print_title:
                print(f"///// {i + 1} / {count}: {name} /////")
            asm_path = temp_path / "test.asm"
            asm_path.write_text(template_parser(templ_dct[name]))
            yield
    return generator()


if __name__ == "__main__":
    pass
    # temp_path = pathlib.Path("temporary")
    # temp_path.mkdir(exist_ok=True)
    # for _ in gen_data(11):
    #     pass
