from blocks.BlockBase import BlockBase


class _Wildness(BlockBase):

    def spawn(self, *args, **kwargs):
        # TODO How to shuffle all the blocks and how to support nested blocks?
        return ""


def instance():
    return _Wildness()
