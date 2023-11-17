import random

from blocks.BlockBase import BlockBase

word = ["400", "404", "420"]
half = ["402", "404", "422"]
byte = ["401", "403", "420"]


def rand_nop(max_count=1):
    return "".join(["\nnop"] * random.randint(0, max_count))


def rand_tw():
    return random.randint(0, 1) == 1


def rand_two_reg(instr, reg, other):
    if rand_tw():
        return instr.replace("#r", reg, 1).replace("#r", other, 1)
    return instr.replace("#r", other, 1).replace("#r", reg, 1)


class InstrCategory:
    name: str
    lst: list[str]


class __CoverP6(BlockBase):
    class CalcRR(InstrCategory):
        name = "calc_rr"
        lst = [
            "add  #t, #r, #r",
            "sub  #t, #r, #r",
            "and  #t, #r, #r",
            "or   #t, #r, #r",
            "slt  #t, #r, #r",
            "sltu #t, #r, #r",
        ]

    class CalcRI(InstrCategory):
        name = "calc_ri"
        lst = [
            "ori  #t, #r, #i",
            "addi #t, #r, #i",
            "andi #t, #r, #i",
        ]

    class Lui(InstrCategory):
        name = "lui"
        lst = [
            "lui  #t, #i",
        ]

    class Load(InstrCategory):
        name = "load"
        lst = [
            "lw   #t, #i(#r)",
            "lh   #t, #i(#r)",
            "lb   #t, #i(#r)",
        ]

    class Store(InstrCategory):
        name = "store"
        lst = [
            "sw   #t, #i(#r)",
            "sh   #t, #i(#r)",
            "sb   #t, #i(#r)",
        ]

    class Jal(InstrCategory):
        name = "jal"
        lst = [
            "jal  #l",
        ]

    class Jr(InstrCategory):
        name = "jr"
        lst = [
            "jr   #r"
        ]

    class Branch(InstrCategory):
        name = "br_r2"
        lst = [
            "beq  #r, #r, #l",
            "bne  #r, #r, #l",
        ]

    class Mul(InstrCategory):
        name = "mul_div"
        lst = [
            "mult #r, #r",
            "multu #r, #r",
        ]

    class Div(InstrCategory):
        name = "mul_div"
        lst = [
            "div  #r, #r",
            "divu #r, #r",
        ]

    class MvTo(InstrCategory):
        name = "mv_to"
        lst = [
            "mthi #r",
            "mtlo #r"
        ]

    class MvFr(InstrCategory):
        name = "mv_fr"
        lst = [
            "mfhi #t",
            "mflo #t",
        ]

    def supply_calc_rr(self, reg):
        instr = random.choice(self.CalcRR.lst)
        instr = instr.replace("#t", reg).replace("#r", self.reg("t"), 1).replace("#r", self.reg("t"), 1)
        return instr

    def consume_calc_rr(self, reg):
        instr = random.choice(self.CalcRR.lst).replace("#t", self.reg("t"))
        return rand_two_reg(instr, reg, self.reg("t"))

    def supply_calc_ri(self, reg):
        instr = random.choice(self.CalcRI.lst)
        imm = self.imm(low=-32768, high=32767) if instr.startswith("addi") else self.imm16()
        instr = instr.replace("#t", reg).replace("#r", self.reg("t")).replace("#i", imm)
        return instr

    def consume_calc_ri(self, reg):
        instr = random.choice(self.CalcRI.lst).replace("#t", self.reg("t"))
        imm = self.imm(low=-32768, high=32767) if instr.startswith("addi") else self.imm16()
        instr = instr.replace("#i", imm).replace("#r", reg, 1)
        return instr

    def supply_lui(self, reg):
        instr = random.choice(self.Lui.lst).replace("#t", reg).replace("#i", self.imm16())
        return instr

    def supply_move_from(self, reg):
        instr = random.choice(self.MvFr.lst).replace("#t", reg)
        return instr

    def consume_move_to(self, reg):
        instr = random.choice(self.MvTo.lst).replace("#r", reg)
        return instr

    def consume_branch_rr(self, reg):
        label = self.label()
        insert = self.consume_calc_rr("$s0")
        instr = random.choice(self.Branch.lst).replace("#l", label)
        instr = rand_two_reg(instr, reg, self.reg("t"))
        instr += "\n" + insert
        instr += "\n" + label + ":"
        return instr

    def consume_mul(self, reg):
        instr = random.choice(self.Mul.lst)
        return rand_two_reg(instr, reg, self.reg("t"))

    def consume_div(self, reg1, reg2):
        instr = random.choice(self.Div.lst)
        return instr.replace("#r", reg1, 1).replace("#r", reg2, 1)

    def supply_jal(self, insert, nop_pos):
        label = self.label()
        instr = f"jal {label}\n&0\n{label}:"
        if nop_pos == 0:
            return instr.replace("&0", insert)
        if nop_pos == 1:
            return instr.replace("&0", "nop") + "\n" + insert
        return instr.replace("&0", "nop") + "\nnop\n" + insert

    def consume_stor_load_ra(self, reg):
        instr = random.choice(self.Load.lst + self.Store.lst).replace("#r", reg).replace("#t", self.reg("t"))
        if reg == "$ra":
            if instr.startswith("lw") or instr.startswith("sw"):
                imm = -12888
            elif instr.startswith("lh") or instr.startswith("sh"):
                imm = -12890
            else:
                imm = -12891
            instr = instr.replace("#i", str(imm))
        else:
            pass
        return instr

    def supply_load(self, reg):
        instr = random.choice(self.Load.lst).replace("#t", reg).replace("#r", "$0")
        if instr.startswith("lw"):
            return instr.replace("#i", random.choice(word))
        if instr.startswith("lh"):
            return instr.replace("#i", random.choice(half))
        return instr.replace("#i", random.choice(byte))

    def supply_for_dm_addr(self, reg):
        reg1 = random.choice(["$s1", "$s2"])
        reg2 = random.choice(["$s1", "$s0"])
        instr = random.choice(self.CalcRR.lst + self.CalcRI.lst + self.Load.lst + self.Lui.lst + self.MvFr.lst)
        instr = instr.replace("#i", self.imm_4(low=0, high=0)).replace("#t", reg)
        instr = instr.replace("#r", reg1, 1).replace("#r", reg2, 1)
        return instr

    def supply_for_div(self, reg):
        instr = random.choice(self.CalcRR.lst + self.CalcRI.lst + self.Load.lst + self.Lui.lst + self.MvFr.lst)
        instr = instr.replace("#i", self.imm(low=0, high=0)).replace("#t", reg)
        instr = instr.replace("#r", random.choice(["$s1", "$s0"]), 1).replace("#r", self.reg("t"), 1)
        return instr

    def consume_load(self, reg):
        instr = random.choice(self.Load.lst).replace("#r", reg).replace("#t", self.reg("v"))
        if instr.startswith("lw"):
            return instr.replace("#i", random.choice(word))
        if instr.startswith("lh"):
            return instr.replace("#i", random.choice(half))
        return instr.replace("#i", random.choice(byte))

    def consume_store(self, reg):
        instr = random.choice(self.Store.lst).replace("#r", reg).replace("#t", self.reg("v"))
        if instr.startswith("sw"):
            return instr.replace("#i", random.choice(word))
        if instr.startswith("sh"):
            return instr.replace("#i", random.choice(half))
        return instr.replace("#i", random.choice(byte))

    def init_t_reg(self):
        instr = []
        for i in range(10):
            instr.append(f"ori $t{i}, $0, {self.imm16()}")
        instr.append(f"sw $t{random.randint(0, 9)}, {word[0]}($0)")
        instr.append(f"sw $t{random.randint(0, 9)}, {word[1]}($0)")
        instr.append(f"sw $t{random.randint(0, 9)}, {word[2]}($0)\n")
        return instr

    def init_for_lw(self):
        instr = [
            f"ori $s0, $0, {self.imm_4(low=0, high=100)}",
            f"ori $s1, $0, {self.imm_4(low=100, high=200)}",
            f"ori $s2, $0, {self.imm_4(low=200, high=300)}",
            f"mthi $s0",
            f"mtlo $s1",
        ]
        return instr

    def init_for_div(self):
        instr = [
            f"ori $s0, $0, {self.imm_4_1(low=0, high=100)}",
            f"ori $s1, $0, {self.imm_4_1(low=104, high=200)}",
            f"ori $s2, $0, {self.imm_4_1(low=204, high=300)}",
            f"mthi $s0",
            f"mtlo $s1",
        ]
        return instr

    def to_jr(self):
        def func(line):
            return line.rstrip().replace("nop", random.choice(
                [self.supply_calc_ri("$ra"), self.supply_calc_rr("$ra"),
                 self.consume_calc_ri("$ra"), self.consume_calc_rr("$ra")]
            )).replace("NOP", "nop")
        res = open("blocks/P6_FWD_JR", "r").readlines()
        return list(map(func, res))

    def spawn(self, *args, **kwargs):
        instructions = self.init_t_reg()

        consume = [self.consume_calc_rr] * 6 + [self.consume_calc_ri] * 3 + \
                  [self.consume_branch_rr] * 2 + [self.consume_move_to] * 2 + [self.consume_mul] * 2
        supply = [self.supply_calc_rr] * 6 + [self.supply_calc_ri] * 3 + \
                 [self.supply_lui] + [self.supply_move_from] * 2 + [self.supply_load] * 3

        for _ in range(400):
            consumer = random.choice(consume)
            supplier = random.choice(supply)
            tar_reg = self.reg("t")
            nop_insert = random.randint(0, 2)
            for _ in range(nop_insert, 2):
                instructions.append(self.supply_calc_rr(tar_reg))
            instructions.append(supplier(tar_reg))
            instructions.extend(["nop"] * nop_insert)
            instructions.append(consumer(tar_reg) + "\n")

        j_consume = [self.consume_calc_rr] * 6 + [self.consume_calc_ri] * 3 + \
                    [self.consume_move_to] * 2 + [self.consume_mul] * 2 + \
                    [self.consume_stor_load_ra] * 6
        for _ in range(40):
            consumer = random.choice(j_consume)
            nop_insert = random.randint(0, 2)
            for _ in range(nop_insert, 2):
                instructions.append(self.supply_calc_rr("$ra"))
            instructions.append(self.supply_jal(consumer("$ra"), nop_insert) + "\n")

        instructions.extend(self.init_for_lw())
        for _ in range(100):
            nop_insert = random.randint(0, 2)
            for _ in range(nop_insert, 2):
                instructions.append(self.supply_calc_rr("$v0"))
            instructions.append(self.supply_for_dm_addr("$v0"))
            instructions.extend(["nop"] * nop_insert)
            instructions.append(random.choice([self.consume_store, self.consume_load])("$v0") + "\n")

        for _ in range(200):
            nop_insert = random.randint(0, 2)
            for _ in range(nop_insert, 2):
                instructions.append(self.supply_calc_rr("$v0"))
            instructions.append(self.supply_for_div("$v0"))
            instructions.extend(["nop"] * nop_insert)
            if random.randint(0, 100) < 90:
                instructions.append(self.consume_div("$v0", random.choice(["$s1", "$s2"])) + "\n")
            else:
                instructions.append(
                    self.supply_jal(self.consume_div("$ra", random.choice(["$s1", "$s2"])), nop_insert) + "\n"
                )

        for _ in range(10):
            nop_insert = random.randint(1, 2)
            instructions.append(self.supply_jal(self.consume_branch_rr("$ra"), nop_insert) + "\n")

        instructions.extend(self.to_jr())

        return "\n".join(instructions)


def instance():
    return __CoverP6()
