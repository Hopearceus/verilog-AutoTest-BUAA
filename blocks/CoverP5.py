import random

from blocks.BlockBase import BlockBase


def rand_nop(max_count=1):
    return "".join(["\nnop"] * random.randint(0, max_count))


class __CoverP5(BlockBase):
    cal_rr_lst = [
        ("add", "#t, #r, #r"),
        ("sub", "#t, #r, #r"),
    ]

    cal_ri_lst = [
        ("ori", "#t, #r, #i"),
    ]

    br_r2_lst = [
        ("beq", "#r, #r, #l")
    ]

    def init_four(self):
        return f"ori $v0, $0, {int(self.imm(low=0, high=100)) * 4}\n" \
               f"ori $v1, $0, {int(self.imm(low=0, high=100)) * 4}\n"

    def fwd_cal_r(self, fwd_reg, four_times=False):
        choose = random.choice(self.cal_rr_lst + self.cal_ri_lst)
        instr: str = choose[0] + " " + choose[1]
        if not four_times:
            instr = instr \
                .replace("#t", fwd_reg) \
                .replace("#r", self.reg("st"), 1) \
                .replace("#r", self.reg("st"), 1) \
                .replace("#i", self.imm16())
        else:
            instr = self.init_four() + instr
            instr = instr \
                .replace("#t", fwd_reg) \
                .replace("#r", self.reg("v"), 1) \
                .replace("#r", self.reg("v"), 1) \
                .replace("#i", str(int(self.imm(low=0, high=100)) * 4))
        return instr

    def tar_cal_r(self, fwd_reg="$ra", fwd_ra=False):
        choose = random.choice(self.cal_rr_lst + self.cal_ri_lst)
        instr: str = choose[0] + " " + choose[1]
        if fwd_ra:
            fwd_reg = self.reg("a")
            instr = f"add {fwd_reg}, $ra, $0\nori $ra, $0, 0\n{instr}{rand_nop(2)}"
        if random.randint(0, 1) and instr.count("#r") == 2 and not fwd_ra:
            instr = instr.replace("#r", self.reg("st"), 1)
            instr = instr.replace("#r", fwd_reg, 1)
        else:
            instr = instr.replace("#r", fwd_reg, 1)
            instr = instr.replace("#r", self.reg("st") if not fwd_ra else "$0", 1)
        instr = instr.replace("#i", self.imm16() if not fwd_ra else "0")
        instr = instr.replace("#t", self.reg("st") if not fwd_ra else "$ra")
        return instr

    def fwd_lui(self, fwd_reg, four_times=False):
        if not four_times:
            return f"lui {fwd_reg}, {self.imm16()}"
        else:
            return f"ori {fwd_reg}, $0, {int(self.imm(low=0, high=100)) * 4}\nlui {fwd_reg}, 0"

    def fwd_load(self, fwd_reg, four_times=False):
        reg = self.reg("a")
        asm = f"ori {reg}, $0, {self.imm16() if not four_times else int(self.imm(low=0, high=100)) * 4}\n"
        asm += f"sw {reg}, 3000($0)\n"
        asm += f"lw {fwd_reg}, 3000($0)"
        return asm

    def tar_store(self, fwd_reg):
        return f"sw {fwd_reg}, {2048}($0)"

    def tar_load(self, fwd_reg, for_ra=False):
        return f"lw {self.reg('s')}, {800 if not for_ra else -12288}({fwd_reg})"

    def tar_br(self, fwd_reg, insert="nop"):
        choose = random.choice(self.br_r2_lst)
        label = self.label()
        instr: str = (choose[0] + " " + choose[1]).replace("#l", label)
        flag = random.randint(0, 4)
        if flag == 0:
            instr = instr.replace("#r", fwd_reg, 1).replace("#r", self.reg("s"), 1)
        elif flag == 1:
            instr = instr.replace("#r", self.reg("s"), 1).replace("#r", fwd_reg, 1)
        else:
            instr = instr.replace("#r", fwd_reg)
        instr += f"\n{insert}"
        instr += f"\n{label}:"
        return instr

    def fwd_jal_1(self, jump_back=True, insert="nop"):
        label = self.label()
        instr = f"jal {label}"
        instr += f"\n{insert}"
        instr += f"\n{label}:"
        if jump_back:
            instr += "\njr $ra"
            instr += "\nnop"
        return instr

    def fwd_jal_2(self, jump_back=True, insert="nop"):
        label = self.label()
        instr = f"jal {label}"
        instr += "\nnop"
        instr += f"\n{label}:"
        instr += rand_nop(2)
        instr += f"\n{insert}"
        if jump_back:
            instr += "\njr $ra"
            instr += "\nnop"
        return instr

    def load_to_jr(self):
        label1, label2 = self.label(), self.label()
        return f"""\
jal {label1}
nop
beq $0, $0, {label2}
nop
{label1}:
sw $ra, 1088($0)
sub $ra, $0, $ra
lw $ra, 1088($0)
{'nop' if random.randint(0, 1) else ''}
jr $ra
nop
{label2}:
"""

    def load_to_store(self):
        reg = self.reg("vts")
        return f"""\
lw {reg}, 1088($0)
{'nop' if random.randint(0, 1) else ''}
sw {self.reg('a')}, -12288({reg})
lw {reg}, 1088($0)
{'nop' if random.randint(0, 1) else ''}
sw {reg}, -12288({reg})
"""

    def jal_to_jr(self):
        label1, label2 = self.label(), self.label()
        return f"""\
jal {label1}
nop
beq $0, $0, {label2}
nop
{label1}:
{'nop' if random.randint(0, 1) else ''}
jr $ra
nop
{label2}:
"""

    def tar_jr(self, insert):
        label1, label2 = self.label(), self.label()
        return f"""\
jal {label1}
nop
beq $0, $0, {label2}
nop
{label1}:
{insert}
jr $ra
nop
{label2}:
"""

    def spawn(self, *args, **kwargs):
        asm = ""

        for _ in range(40):
            fwd_reg = self.reg("va")
            asm += "\n" + self.fwd_cal_r(fwd_reg)
            asm += rand_nop(2)
            asm += "\n" + self.tar_cal_r(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("va")
            asm += "\n" + self.fwd_lui(fwd_reg)
            asm += rand_nop(2)
            asm += "\n" + self.tar_cal_r(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("va")
            asm += "\n" + self.fwd_load(fwd_reg)
            asm += rand_nop(2)
            asm += "\n" + self.tar_cal_r(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("va")
            asm += "\n" + self.fwd_cal_r(fwd_reg)
            asm += rand_nop(2)
            asm += "\n" + self.tar_store(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("va")
            asm += "\n" + self.fwd_load(fwd_reg)
            asm += rand_nop(2)
            asm += "\n" + self.tar_store(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("va")
            asm += "\n" + self.fwd_lui(fwd_reg)
            asm += rand_nop(2)
            asm += "\n" + self.tar_store(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("t")
            asm += "\n" + self.fwd_cal_r(fwd_reg, four_times=True)
            asm += rand_nop(2)
            asm += "\n" + self.tar_load(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("t")
            asm += "\n" + self.fwd_load(fwd_reg, four_times=True)
            asm += rand_nop(2)
            asm += "\n" + self.tar_load(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("t")
            asm += "\n" + self.fwd_lui(fwd_reg, four_times=True)
            asm += rand_nop(2)
            asm += "\n" + self.tar_load(fwd_reg)

        for _ in range(40):
            fwd_reg = self.reg("t")
            asm += "\n" + self.fwd_cal_r(fwd_reg, four_times=True)
            asm += rand_nop(2)
            asm += "\n" + self.tar_br(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("t")
            asm += "\n" + self.fwd_lui(fwd_reg, four_times=True)
            asm += rand_nop(2)
            asm += "\n" + self.tar_br(fwd_reg)

        for _ in range(20):
            fwd_reg = self.reg("t")
            asm += "\n" + self.fwd_load(fwd_reg, four_times=True)
            asm += rand_nop(2)
            asm += "\n" + self.tar_br(fwd_reg)

        for _ in range(40):
            asm += "\n" + self.fwd_jal_1(False, self.tar_cal_r("$ra"))
            asm += "\n" + self.fwd_jal_2(False, self.tar_cal_r("$ra"))

        for _ in range(20):
            asm += "\n" + self.fwd_jal_1(False, self.tar_load("$ra", True))
            asm += "\n" + self.fwd_jal_2(False, self.tar_load("$ra", True))

        for _ in range(20):
            asm += "\n" + self.fwd_jal_1(False, self.tar_store("$ra"))
            asm += "\n" + self.fwd_jal_2(False, self.tar_store("$ra"))

        for _ in range(20):
            asm += "\n" + self.fwd_jal_2(False, self.tar_br("$ra"))

        for _ in range(5):
            asm += "\n" + self.jal_to_jr()
            asm += "\n" + self.load_to_jr()
            asm += "\n" + self.load_to_store()

        for _ in range(40):
            asm += "\n" + self.tar_jr(self.tar_cal_r(fwd_ra=True))

        return asm


def instance():
    return __CoverP5()
