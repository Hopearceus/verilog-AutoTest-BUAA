import os
import pathlib
import platform
import shutil

import SetPath as sp
from JudgeCore import diff
from DataSpawner import gen_data


def hint_wrapper(s):
    return '\033[1m\033[34m' + s + '\033[0m'


def run():
    path = sp.set_path()
    xilinx_path = path['xilinx_path']
    java_path = path['java_path']
    # prj_path = path['prj_path']
    # cwd_path = os.getcwd()
    # for file in pathlib.Path(prj_path).rglob("*\\*.v"):
    #     print("copy " + str(file) + " " + cwd_path + "\\run\\" + file.name)
    #     os.system("copy " + str(file) + " " + cwd_path + "\\run\\" + file.name)
    # os.system("copy " + prj_path + "\\mips.prj " + cwd_path + "run\\mips.prj")
    print(hint_wrapper("Compiling the verilog projects ..."))
    if platform.system() == "Windows":
        os.system((pathlib.Path(xilinx_path) / "bin" / "nt64" / "fuse").__str__() +
                  " -nodebug -prj ./run/mips.prj -o mips.exe mips_tb")
    else:
        os.system((pathlib.Path(xilinx_path) / "bin" / "lin64" / "fuse").__str__() +
                  " -nodebug -prj ./run/mips.prj -o mips.exe mips_tb")
    print(hint_wrapper("Done!"))
    s = input("Do you want to enable delay branch? [y/N]")
    no_db = s.lower().find("y") == -1
    for _ in gen_data(10):
        print(hint_wrapper("Run Mars to get the code text ..."))
        os.system(java_path + " -jar ./Mars_CO_v0.4.1.jar mc CompactLargeText a dump .text HexText ./temporary/code.txt ./temporary/test.asm")
        # os.system(r"move .\temporary\code.txt .\code.txt")
        shutil.move("./temporary/code.txt", "./code.txt")
        print(hint_wrapper("Start the simulation ..."))
        os.system("./mips.exe -nolog -tclbatch ./run/mips.tcl > ./temporary/cpu.txt")

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
    current_path = pathlib.Path(__file__).resolve().parent
    os.chdir(current_path)
    run()
