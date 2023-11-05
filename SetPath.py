import pathlib
import re
import os


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
    s = input("please enter your ISE path here, ending with ISE/(\\):\n")
    while re.match(".*[/\\\\]ISE[/\\\\]?$", s) is None or not pathlib.Path(s).exists() or not pathlib.Path(s).is_dir():
        s = input("Error path! Try again:\n")
    pathlib.Path("config/ISE_path").write_text(s)
    s = input("please enter your Java path here:\n")
    while os.system(s + " -version>nul") != 0:
        s = input("Error path! Try again:\n")
    pathlib.Path("config/Java_path").write_text(s)
    s = input("please enter your ise project path here:\n")
    while not pathlib.Path(s).exists():
        s = input("No such file! Try again:\n")
    pathlib.Path("config/Prj_path").write_text(s)


if __name__ == "__main__":
    write_config()
    set_path()
