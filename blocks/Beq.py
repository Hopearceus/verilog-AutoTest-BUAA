from blocks.BlockBase import BlockBase


class __BeqBlock(BlockBase):

    def spawn(self, *args, **kwargs):
        """
        Branch block, which will not fall into an endless loop
        :param args: Things to be inserted
        :keyword end: loop end(register), $s* by default
        :keyword var: loop var(register), $t* by default
        :return: A multi-line block
        """
        if len(args) > 0:
            insert = args[0]
        else:
            insert = ""
        loop_var_r = kwargs.get("var", self.reg("t"))
        loop_end_r = kwargs.get("end", self.reg("s"))

        loop_var = self.imm(low=0, high=200)
        loop_end = self.imm(low=100, high=300)
        loop_inc = "sub" if int(loop_end) < int(loop_var) else "add"

        loop_label = self.label()
        end_label = self.label()

        return f"""\
ori {loop_var_r}, $zero, {loop_var}
ori {loop_end_r}, $zero, {loop_end}
{loop_label}:

beq {loop_var_r}, {loop_end_r}, {end_label}

{insert}

ori $at, $zero, 1
{loop_inc} {loop_var_r}, {loop_var_r}, $at
beq $0, $0, {loop_label}
{end_label}:
"""


def instance():
    return __BeqBlock()
