import pathlib
import shutil


def verilog_source_finder(path: pathlib.Path) -> [pathlib.Path, pathlib.Path]:
    ret = []
    for file in path.rglob("*.v"):
        ret.append((file.relative_to(path), file))
    return ret


def copy_verilog_source(run_path: pathlib.Path, files: [pathlib.Path, pathlib.Path]):
    for relative, file in files:
        (run_path / relative.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy(str(file), str(run_path / relative))


def gen_prj_file(files: [pathlib.Path, pathlib.Path]):
    ret = []
    for relative, _ in files + [("mips_tb.v", None)]:
        ret.append(f'verilog work "{relative}"')
    return "\n".join(ret)


def gen_tb_file():
    return """\
`timescale 1ns / 1ps
module mips_tb;
    reg clk;
    reg reset;
    mips uut (
        .clk(clk), 
        .reset(reset)
    );
    initial begin
        clk = 0;
        reset = 1;
        #2 reset = 0;
    end
    always #1 clk = ~clk;
endmodule
"""


def gen_tcl_file(run_us=2000):
    return f"run {run_us}us;\nexit"


if __name__ == "__main__":
    f = verilog_source_finder(pathlib.Path("/home/swkfk/ise_proj/SingleCycleMipsCPU"))
    copy_verilog_source(pathlib.Path("./run"), f)
    print(gen_prj_file(f))
