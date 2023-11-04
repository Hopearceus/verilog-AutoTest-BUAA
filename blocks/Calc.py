from blocks.BlockBase import BlockBase
import random


class __Calculation(BlockBase):

    choice = [
        "add #r, #r, #r",
        "sub #r, #r, #r",
        "lui #r, #i",
        "ori #r, #r, #i",
        # "sll #r, #r, #s"
    ]

    def spawn(self, *args, **kwargs):
        """
        Spawn a random instruction that is about calculation
        :keyword pick: pick a specified instruction
        :keyword reg: choose the registers which are allowed to use
        :keyword repeat: repeat(random) `repeat` times, 1 by default
        :return: multi-line instructions(`repeat` lines)
        """
        choice_dict = dict([(choice.split()[0], choice) for choice in self.choice])

        try:
            repeat = int(kwargs.get("repeat", "1"))
        except ValueError as e:
            repeat = 1

        if kwargs.get("pick") in choice_dict:
            instr = "\n".join([choice_dict[kwargs.get("pick")]] * repeat)
        else:
            instr = "\n".join(random.choices(self.choice, k=repeat))

        reg = kwargs.get("reg", "vats")

        while instr.find("#r") != -1:
            instr = instr.replace("#r", self.reg(reg), 1)
        while instr.find("#i") != -1:
            instr = instr.replace("#i", self.imm16(), 1)
        while instr.find("#s") != -1:
            instr = instr.replace("#s", self.shamt(), 1)

        return instr + "\n"


def instance():
    return __Calculation()
