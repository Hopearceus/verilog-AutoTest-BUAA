from blocks.BlockBase import BlockBase


class _InitialRegisters(BlockBase):

    def spawn(self, *args, **kwargs):
        """
        Initial all the registers with a random value
        :return: 32 * 2 lines
        """
        return (
            "".join([f"lui ${i}, {self.imm16()}\n" for i in range(32)]) +
            "".join([f"ori ${i} {self.reg('*')}, {self.imm16()}\n" for i in range(32)])
        )


def instance():
    return _InitialRegisters()
