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


def gen_tb_file(use_tb_p6=False):
    if not use_tb_p6:
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
    else:
        return """\
`timescale 1ns/1ps
module mips_tb;
    reg clk;
    reg reset;
    wire [31:0] i_inst_addr;
    wire [31:0] i_inst_rdata;
    wire [31:0] m_data_addr;
    wire [31:0] m_data_rdata;
    wire [31:0] m_data_wdata;
    wire [3 :0] m_data_byteen;
    wire [31:0] m_inst_addr;
    wire w_grf_we;
    wire [4:0] w_grf_addr;
    wire [31:0] w_grf_wdata;
    wire [31:0] w_inst_addr;
    mips uut(
        .clk(clk),
        .reset(reset),
        .i_inst_addr(i_inst_addr),
        .i_inst_rdata(i_inst_rdata),
        .m_data_addr(m_data_addr),
        .m_data_rdata(m_data_rdata),
        .m_data_wdata(m_data_wdata),
        .m_data_byteen(m_data_byteen),
        .m_inst_addr(m_inst_addr),
        .w_grf_we(w_grf_we),
        .w_grf_addr(w_grf_addr),
        .w_grf_wdata(w_grf_wdata),
        .w_inst_addr(w_inst_addr)
    );
    integer i;
    reg [31:0] fixed_addr;
    reg [31:0] fixed_wdata;
    reg [31:0] data[0:4095];
    reg [31:0] inst[0:4095];
    assign m_data_rdata = data[m_data_addr >> 2];
    assign i_inst_rdata = inst[(i_inst_addr - 32'h3000) >> 2];
    initial begin
        $readmemh("code.txt", inst);
        for (i = 0; i < 4096; i = i + 1) data[i] <= 0;
    end
    initial begin
        clk = 0;
        reset = 1;
        #20 reset = 0;
    end
    always @(*) begin
        fixed_wdata = data[m_data_addr >> 2];
        fixed_addr = m_data_addr & 32'hfffffffc;
        if (m_data_byteen[3]) fixed_wdata[31:24] = m_data_wdata[31:24];
        if (m_data_byteen[2]) fixed_wdata[23:16] = m_data_wdata[23:16];
        if (m_data_byteen[1]) fixed_wdata[15: 8] = m_data_wdata[15: 8];
        if (m_data_byteen[0]) fixed_wdata[7 : 0] = m_data_wdata[7 : 0];
    end
    always @(posedge clk) begin
        if (reset) for (i = 0; i < 4096; i = i + 1) data[i] <= 0;
        else if (|m_data_byteen) begin
            data[fixed_addr >> 2] <= fixed_wdata;
            $display("%d@%h: *%h <= %h", $time, m_inst_addr, fixed_addr, fixed_wdata);
        end
    end
    always @(posedge clk) begin
        if (~reset) begin
            if (w_grf_we && (w_grf_addr != 0)) begin
                $display("%d@%h: $%d <= %h", $time, w_inst_addr, w_grf_addr, w_grf_wdata);
            end
        end
    end
    always #2 clk <= ~clk;
endmodule
"""


def gen_tcl_file(run_us=2000):
    return f"run {run_us}us;\nexit"


if __name__ == "__main__":
    f = verilog_source_finder(pathlib.Path("/home/swkfk/ise_proj/SingleCycleMipsCPU"))
    copy_verilog_source(pathlib.Path("./run"), f)
    print(gen_prj_file(f))
