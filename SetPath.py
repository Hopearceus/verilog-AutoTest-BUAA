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
    if not os.path.exists("./config"):
        os.mkdir("config")
    s = input(f"Please enter your ISE path (end with ISE{os.path.sep}): ")
    while re.match(".*[/\\\\]ISE[/\\\\]?$", s) is None or not pathlib.Path(s).exists() or not pathlib.Path(s).is_dir():
        s = input("Error path! Try again: ")
    pathlib.Path("config/ISE_path").write_text(s)

    s = input("Please enter your Java path: ")
    right = False
    while not right:
        try:
            subprocess.check_call([s, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            right = True
        except (FileNotFoundError, subprocess.CalledProcessError) as _:
            s = input("Error path! Try again: ")

    pathlib.Path("config/Java_path").write_text(s)
    s = input("Please enter your ise project path: ")
    while not pathlib.Path(s).exists():
        s = input("No such folder! Try again: ")
    pathlib.Path("config/Prj_path").write_text(s)


if __name__ == "__main__":
    write_config()
    set_path()
