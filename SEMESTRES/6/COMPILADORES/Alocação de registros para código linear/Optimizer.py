from abc import ABC, abstractmethod
from Asm import *


class Optimizer(ABC):
    """
    This class implements an "Optimization Pass". The pass receives a sequence
    of instructions stored in a program, and produces a new sequence of
    instructions.
    """

    def __init__(self, prog):
        self.prog = prog

    @abstractmethod
    def optimize(self):
        pass


class RegAllocator(Optimizer):
    """This file implements the register allocation pass."""

    def __init__(self, prog):
        super().__init__(prog)
        
        self.count = 0
        self.vars_to_pos = {}

        self.alloc_action = {
            "addi": addi_update,
            "add": add_update,
            "sub": sub_update,
            "div": div_update,
            "mul": mul_update, 
            "xor": xor_update,
            "slti": slit_update,
            "xori": xori_update,
            "sw": sw_update,
            "lw": lw_update,
            "slt": slt_update
        }

    def get_val(self, var):
        """
        Informs the value that is associated with the variable var within
        the program prog.
        """
        return self.prog.get_val(var)


    def optimize(self):
        """
        This function perform register allocation. It maps variables into
        memory, and changes instructions, so that they use one of the following
        registers:
        * x0: always the value zero. Can't change.
        * sp: the stack pointer. Starts with the memory size.
        * ra: the return address.
        * a0: function argument 0 (or return address)
        * a1: function argument 1
        * a2: function argument 2
        * a3: function argument 3

        Notice that next to each register we have suggested a usage. You can,
        of course, write on them and use them in other ways. But, at least x0
        and sp you should not overwrite. The first register you can't overwrite,
        actually. And sp is initialized with the number of memory addresses.
        It's good to use it to control the function stack.

        Examples:
        >>> insts = [Addi("a", "x0", 3)]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        3

        >>> insts = [Addi("a", "x0", 1), Slti("b", "a", 2)]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        1

        >>> insts = [Addi("a", "x0", 3), Slti("b", "a", 2), Xori("c", "b", 5)]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        5

        >>> insts = [Addi("sp", "sp", -1),Addi("a", "x0", 7),Sw("sp", 0, "a")]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_mem(p.get_val("sp"))
        7

        >>> insts = [Addi("sp", "sp", -1),Addi("a", "x0", 7),Sw("sp", 0, "a")]
        >>> insts += [Lw("sp", 0, "b"), Addi("c", "b", 6)]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        13

        >>> insts = [Addi("a", "x0", 3),Addi("b", "x0", 4),Add("c", "a", "b")]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        7

        >>> insts = [Addi("a", "x0", 28),Addi("b", "x0", 4),Div("c", "a", "b")]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        7

        >>> insts = [Addi("a", "x0", 3),Addi("b", "x0", 4),Mul("c", "a", "b")]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        12

        >>> insts = [Addi("a", "x0", 3),Addi("b", "x0", 4),Xor("c", "a", "b")]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        7

        >>> insts = [Addi("a", "x0", 3),Addi("b", "x0", 4),Slt("c", "a", "b")]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        1

        >>> insts = [Addi("a", "x0", 3),Addi("b", "x0", 4),Slt("c", "b", "a")]
        >>> p = Program(1000, env={}, insts=insts)
        >>> o = RegAllocator(p)
        >>> o.optimize()
        >>> p.eval()
        >>> p.get_val("a1")
        0
        
        # If you want, you can allocate Jal/Jalr/Beq instructions, but that's not
        # necessary for this exercise.

        # >>> insts = [Jal("a", 30)]
        # >>> p = Program(1000, env={}, insts=insts)
        # >>> o = RegAllocator(p)
        # >>> o.optimize()
        # >>> p.eval()
        # >>> (p.get_pc(), p.get_val("a1") > 0)
        # (30, True)

        # >>> insts = [Addi("a", "x0", 30), Jalr("b", "a")]
        # >>> p = Program(1000, env={}, insts=insts)
        # >>> o = RegAllocator(p)
        # >>> o.optimize()
        # >>> p.eval()
        # >>> (p.get_pc(), p.get_val("a1") > 0)
        # (30, True)

        # >>> insts = [Addi("a", "x0", 3), Addi("b", "a", 0), Beq("a", "b", 30)]
        # >>> p = Program(1000, env={}, insts=insts)
        # >>> o = RegAllocator(p)
        # >>> o.optimize()
        # >>> p.eval()
        # >>> p.get_pc()
        # 30
        """
 
        new_insts = []
        for inst in self.prog.get_insts():
            action = self.alloc_action[inst.get_opcode()]
            last_insts = action(inst, self)
            new_insts += last_insts
        self.prog.set_insts(new_insts)


def addi_update(inst, p: RegAllocator):
    insts = []

    if inst.rd not in p.vars_to_pos and inst.rd not in ["x0", "sp"]:
        p.vars_to_pos[inst.rd] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a0"))
        inst.rs1 = "a0"

    if inst.rd not in ["x0", "sp"]:
        insts.append(Addi("a1", inst.rs1, inst.imm))
        insts.append(Sw("x0", p.vars_to_pos[inst.rd], "a1"))
    else:
        insts.append(inst)

    return insts


def add_update(inst, p: RegAllocator):
    insts = []

    if inst.rd not in p.vars_to_pos and inst.rd not in ["x0", "sp"]:
        p.vars_to_pos[inst.rd] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a0"))
        inst.rs1 = "a0"

    if inst.rs2 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs2], "a2"))
        inst.rs2 = "a2"

    if inst.rd not in ["x0", "sp"]:
        insts.append(Add("a1", inst.rs1, inst.rs2))
        insts.append(Sw("x0", p.vars_to_pos[inst.rd], "a1"))
    else:
        insts.append(inst)

    return insts

def sub_update(inst, p: RegAllocator):
    insts = []

    if inst.rd not in p.vars_to_pos and inst.rd not in ["x0", "sp"]:
        p.vars_to_pos[inst.rd] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a0"))
        inst.rs1 = "a0"

    if inst.rs2 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs2], "a2"))
        inst.rs2 = "a2"

    if inst.rd not in ["x0", "sp"]:
        insts.append(Sub("a1", inst.rs1, inst.rs2))
        insts.append(Sw("x0", p.vars_to_pos[inst.rd], "a1"))
    else:
        insts.append(inst)

    return insts

def div_update(inst, p: RegAllocator):
    insts = []

    if inst.rd not in p.vars_to_pos and inst.rd not in ["x0", "sp"]:
        p.vars_to_pos[inst.rd] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a0"))
        inst.rs1 = "a0"

    if inst.rs2 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs2], "a2"))
        inst.rs2 = "a2"

    if inst.rd not in ["x0", "sp"]:
        insts.append(Div("a1", inst.rs1, inst.rs2))
        insts.append(Sw("x0", p.vars_to_pos[inst.rd], "a1"))
    else:
        insts.append(inst)

    return insts

def mul_update(inst, p: RegAllocator):
    insts = []

    if inst.rd not in p.vars_to_pos and inst.rd not in ["x0", "sp"]:
        p.vars_to_pos[inst.rd] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a0"))
        inst.rs1 = "a0"

    if inst.rs2 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs2], "a2"))
        inst.rs2 = "a2"

    if inst.rd not in ["x0", "sp"]:
        insts.append(Mul("a1", inst.rs1, inst.rs2))
        insts.append(Sw("x0", p.vars_to_pos[inst.rd], "a1"))
    else:
        insts.append(inst)

    return insts

def xor_update(inst, p: RegAllocator):
    insts = []

    if inst.rd not in p.vars_to_pos and inst.rd not in ["x0", "sp"]:
        p.vars_to_pos[inst.rd] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a0"))
        inst.rs1 = "a0"

    if inst.rs2 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs2], "a2"))
        inst.rs2 = "a2"

    if inst.rd not in ["x0", "sp"]:
        insts.append(Xor("a1", inst.rs1, inst.rs2))
        insts.append(Sw("x0", p.vars_to_pos[inst.rd], "a1"))
    else:
        insts.append(inst)

    return insts


def slt_update(inst, p: RegAllocator):
    insts = []

    if inst.rd not in p.vars_to_pos and inst.rd not in ["x0", "sp"]:
        p.vars_to_pos[inst.rd] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a0"))
        inst.rs1 = "a0"

    if inst.rs2 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs2], "a2"))
        inst.rs2 = "a2"

    if inst.rd not in ["x0", "sp"]:
        insts.append(Slt("a1", inst.rs1, inst.rs2))
        insts.append(Sw("x0", p.vars_to_pos[inst.rd], "a1"))
    else:
        insts.append(inst)

    return insts

def slit_update(inst, p: RegAllocator):
    insts = []

    if inst.rd not in p.vars_to_pos and inst.rd not in ["x0", "sp"]:
        p.vars_to_pos[inst.rd] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a0"))
        inst.rs1 = "a0"

    if inst.rd not in ["x0", "sp"]:
        insts.append(Slti("a1", inst.rs1, inst.imm))
        insts.append(Sw("x0", p.vars_to_pos[inst.rd], "a1"))
    else:
        insts.append(inst)

    return insts

def xori_update(inst, p: RegAllocator):
    insts = []

    if inst.rd not in p.vars_to_pos and inst.rd not in ["x0", "sp"]:
        p.vars_to_pos[inst.rd] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a0"))
        inst.rs1 = "a0"

    if inst.rd not in ["x0", "sp"]:
        insts.append(Xori("a1", inst.rs1, inst.imm))
        insts.append(Sw("x0", p.vars_to_pos[inst.rd], "a1"))
    else:
        insts.append(inst)

    return insts

def sw_update(inst, p: RegAllocator):
    insts = []

    if inst.reg not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.reg], "a0"))
        inst.reg = "a0"

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a2"))
        inst.rs1 = "a2"

    insts.append(inst)

    return insts


def lw_update(inst, p: RegAllocator):
    insts = []
    
    if inst.reg not in p.vars_to_pos and inst.reg not in ["x0", "sp"]:
        p.vars_to_pos[inst.reg] = p.count
        p.count += 1

    if inst.rs1 not in ["x0", "sp"]:
        insts.append(Lw("x0", p.vars_to_pos[inst.rs1], "a2"))
        inst.rs1 = "a2"

    insts.append(Lw(inst.rs1, inst.offset, "a0"))
    insts.append(Sw("x0", p.vars_to_pos[inst.reg], "a0"))

    return insts