from blocks.BlockBase import BlockBase


class __Nop(BlockBase):

    def spawn(self, *args, **kwargs):
        return "nop\n"


def instance():
    return __Nop()
