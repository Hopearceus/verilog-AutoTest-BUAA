from blocks.BlockBase import BlockBase


class _DataReadWrite(BlockBase):

    def spawn(self, *args, **kwargs):
        """
        Through store and load blocks
        :keyword AddrStart: The start address to s/l, 0 by default
        :keyword AddrEnd: The end address to s/l, 12284 by default
        :keyword AddrStep: The step between two address, 4 by default
        :keyword SL: Store or load, "load" by default, the other option is "store"
        :return: A multi-line block
        """
        addr_s = int(kwargs.get("AddrStart", "0"))
        addr_step = int(kwargs.get("AddrStep", "4"))
        addr_e = int(kwargs.get("AddrEnd", "12284")) + addr_step

        sl = "l" if kwargs.get("SL", "load") == "load" else "s"
        width = "_bh_w"[addr_step]

        addr_imm = int(self.imm(low=addr_s, high=addr_e))
        addr_reg = hex(0xffffffff & (addr_s - addr_imm))[2:].zfill(8)

        start_label = self.label()
        end_label = self.label()

        return f"""\
ori $t0, $zero, {addr_s}
ori $t1, $zero, {addr_e}
ori $t2, $zero, {addr_step}
lui $at, 0x{addr_reg[0:4]}
ori $at, $at, 0x{addr_reg[4:8]}
{start_label}:
beq $t0, $t1, {end_label}
nop

{sl}{width} $v0, {addr_imm}($at)
add $v0, $v0, $v1

add $t0, $t0, $t2
add $at, $at, $t2
beq $0, $0, {start_label}
nop
{end_label}:
"""


def instance():
    return _DataReadWrite()
