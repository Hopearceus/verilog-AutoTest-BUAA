import os
import pathlib
import platform
import shutil

from SetPath import set_path
from JudgeCore import diff
from DataSpawner import gen_data
from VerilogFileSystem import verilog_source_finder, copy_verilog_source, gen_prj_file

current_path = pathlib.Path(__file__).resolve().parent


def hint_wrapper(s):
    return '\033[1m\033[34m' + s + '\033[0m'


def prompt_wrapper(s):
    return '\033[1m\033[36m' + s + '\033[0m'


def fatal_wrapper(s):
    return '\033[1m\033[31m' + s + '\033[0m'


def run():
    path = set_path()
    xilinx_path = path['xilinx_path']
    java_path = path['java_path']
    prj_path = path['prj_path']

    # cwd_path = os.getcwd()
    # for file in pathlib.Path(prj_path).rglob("*\\*.v"):
    #     print("copy " + str(file) + " " + cwd_path + "\\run\\" + file.name)
    #     os.system("copy " + str(file) + " " + cwd_path + "\\run\\" + file.name)
    # os.system("copy " + prj_path + "\\mips.prj " + cwd_path + "run\\mips.prj")

    print(hint_wrapper("Copying the verilog source files ..."))
    v_files = verilog_source_finder(pathlib.Path(prj_path))
    copy_verilog_source(pathlib.Path("./run"), v_files)

    print(hint_wrapper("Rewrite the prj file ..."))
    pathlib.Path("./run/mips.prj").write_text(gen_prj_file(v_files))

    print(hint_wrapper("Compiling the verilog projects ..."))
    bin_folder = "nt64" if platform.system() == "Windows" else "lin64"
    fuse_path = (pathlib.Path(xilinx_path) / 'bin' / bin_folder / 'fuse')
    os.chdir(current_path / "run")
    ret = os.system(f"{fuse_path} -nodebug -prj mips.prj -o mips.exe mips_tb")
    os.chdir(current_path)
    if ret == 0:
        print(hint_wrapper("Done!"))
    else:
        print(fatal_wrapper("Compile Error!"))
        return

    s = input(prompt_wrapper("Enable the delay branch? [y/N] "))
    no_db = s.lower().find("y") == -1

    for _ in gen_data(10):
        print(hint_wrapper("Run Mars to get the code text ..."))
        os.system(java_path + " -jar ./Mars_CO_v0.4.1.jar nc mc CompactLargeText a dump .text HexText ./temporary/code.txt ./temporary/test.asm")
        # os.system(r"move .\temporary\code.txt .\code.txt")
        shutil.move("./temporary/code.txt", "./run/code.txt")

        print(hint_wrapper("Start the simulation ..."))
        os.chdir(current_path / "run")
        os.system("./mips.exe -nolog -tclbatch ./mips.tcl > ../temporary/cpu.txt")
        os.chdir(current_path)

        print(hint_wrapper("Run Mars to get the right output ..."))
        if no_db:
            os.system(java_path +
                      " -jar Mars_CO_v0.4.1.jar ig 1000000 mc CompactLargeText nc ./temporary/test.asm coL1 > ./temporary/ans.txt")
        else:
            os.system(java_path +
                      " -jar Mars_CO_v0.4.1.jar ig 1000000 db mc CompactLargeText nc ./temporary/test.asm coL1 > ./temporary/ans.txt")

        print(hint_wrapper("Compare the outputs ..."))
        if not diff(pathlib.Path("./temporary/ans.txt").read_text(),
                    pathlib.Path("./temporary/cpu.txt").read_text()):
            break
        print(hint_wrapper("Right!\n"))


if __name__ == "__main__":
    os.chdir(current_path)
    run()
