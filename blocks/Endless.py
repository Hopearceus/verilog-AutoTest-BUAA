from blocks.BlockBase import BlockBase


class _EndlessBeq(BlockBase):

    def spawn(self, *args, **kwargs):
        """
        An endless beq loop
        :keyword label: indicate the branch label, "_e" by default
        :return: A multi-line block
        """
        end_label = kwargs.get("label", "_e")

        return f"""\
{end_label}:
beq $0, $0, {end_label}
"""


def instance():
    return _EndlessBeq()
