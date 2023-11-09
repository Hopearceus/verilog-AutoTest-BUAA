from blocks.BlockBase import BlockBase


class _ProcedureNormal(BlockBase):

    def spawn(self, *args, **kwargs):
        """
        Procedure block, without recursion
        :param args: Things to be inserted in the procedure
        :return: A multi-line block
        """
        end_label = self.label()
        procedure_label = self.label()

        if len(args) > 0:
            insert = args[0]
        else:
            insert = ""

        return f"""\
beq $0, $0, {end_label}
nop
{procedure_label}:

{insert}

jr $ra
nop

{end_label}:
jal {procedure_label}
nop
"""


def instance():
    return _ProcedureNormal()
