import pathlib
import re
import os
import subprocess


class PathError(BaseException):
    def __init__(self, s):
        super().__init__(s)


def set_path():
    if not pathlib.Path("./config").exists() or not pathlib.Path("./config/ISE_path").exists()\
            or not pathlib.Path("./config/Java_path").exists() or not pathlib.Path("./config/Prj_path").exists():
        write_config()
    xilinx_path = pathlib.Path("./config/ISE_path").read_text()
    os.environ['XILINX'] = xilinx_path
    java_path = pathlib.Path("./config/Java_path").read_text()
    prj_path = pathlib.Path("./config/Prj_path").read_text()
    return {"xilinx_path": xilinx_path, "java_path": java_path, "prj_path": prj_path}


def write_config():
    def hint_wrapper(prompt: str, severity=False):
        return ('\033[1m\033[31m' if severity else '\033[1m\033[36m') + prompt + '\033[0m'

    if not os.path.exists("./config"):
        os.mkdir("config")
    s = input(hint_wrapper(f"Please enter your ISE path (end with ISE{os.path.sep}): "))
    while re.match(".*[/\\\\]ISE[/\\\\]?$", s) is None or not pathlib.Path(s).exists() or not pathlib.Path(s).is_dir():
        s = input(hint_wrapper("Error path! Try again: ", True))
    pathlib.Path("config/ISE_path").write_text(s)

    s = input(hint_wrapper("Please enter your Java path: "))
    right = False
    while not right:
        try:
            subprocess.check_call([s, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            right = True
        except (FileNotFoundError, subprocess.CalledProcessError) as _:
            s = input(hint_wrapper("Error path! Try again: ", True))

    pathlib.Path("config/Java_path").write_text(s)
    s = input(hint_wrapper("Please enter your ise project path: "))
    while not pathlib.Path(s).exists():
        s = input(hint_wrapper("No such folder! Try again: ", True))
    pathlib.Path("config/Prj_path").write_text(s)


if __name__ == "__main__":
    write_config()
    set_path()
