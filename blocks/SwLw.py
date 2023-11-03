from blocks.BlockBase import BlockBase


class _StoreAndLoad(BlockBase):

    def spawn(self, *args, **kwargs):
        """
        Store word and load word
        :param args: Things to be inserted between the `sw` and `lw`
        :keyword reg_s: reg to `sw`
        :keyword reg_l: reg to `lw`
        :keyword low: lower address (of word), 0 by default
        :keyword high: higher address (of word), 3071 by default
        :keyword repeat: times to repeat
        :return: `repeat` multi-line blocks
        """
        reg_s = self.reg(kwargs.get("reg_s", "vats"))
        reg_l = self.reg(kwargs.get("reg_l", "vats"))
        low_addr = int(kwargs.get("low", "0"))
        hgh_addr = int(kwargs.get("high", "3071"))
        repeat = int(kwargs.get("repeat", "1"))

        if len(args) > 0:
            insert = args[0]
        else:
            insert = ""

        ret = []

        for _ in range(repeat):

            addr = int(self.imm(low=low_addr, high=hgh_addr)) * 4
            addr_imm = int(self.imm(low=low_addr, high=hgh_addr))
            addr_reg = hex(0xffffffff & (addr - addr_imm))[2:].zfill(8)

            ret.append(f"""\
lui $at, 0x{addr_reg[0:4]}
ori $at, $at, 0x{addr_reg[4:8]}
sw  {reg_s}, {addr_imm}($at)

{insert}

lw  {reg_l}, {addr_imm}($at)
""")

        # end of for _ in range(repeat)
        return "\n".join(ret)


def instance():
    return _StoreAndLoad()
