import sys
from abc import ABC, abstractmethod
from Expression import *
import Asm as AsmModule


class Visitor(ABC):
    """
    The visitor pattern consists of two abstract classes: the Expression and the
    Visitor. The Expression class defines on method: 'accept(visitor, args)'.
    This method takes in an implementation of a visitor, and the arguments that
    are passed from expression to expression. The Visitor class defines one
    specific method for each subclass of Expression. Each instance of such a
    subclasse will invoke the right visiting method.
    """

    @abstractmethod
    def visit_var(self, exp, arg):
        pass

    @abstractmethod
    def visit_bln(self, exp, arg):
        pass

    @abstractmethod
    def visit_num(self, exp, arg):
        pass

    @abstractmethod
    def visit_eql(self, exp, arg):
        pass

    @abstractmethod
    def visit_add(self, exp, arg):
        pass

    @abstractmethod
    def visit_sub(self, exp, arg):
        pass

    @abstractmethod
    def visit_mul(self, exp, arg):
        pass

    @abstractmethod
    def visit_div(self, exp, arg):
        pass

    @abstractmethod
    def visit_leq(self, exp, arg):
        pass

    @abstractmethod
    def visit_lth(self, exp, arg):
        pass

    @abstractmethod
    def visit_neg(self, exp, arg):
        pass

    @abstractmethod
    def visit_not(self, exp, arg):
        pass

    @abstractmethod
    def visit_let(self, exp, arg):
        pass
    

class RenameVisitor(ABC):
    """
    This visitor traverses the AST of a program, renaming variables to ensure
    that they all have different names.

    Usage:
        >>> e0 = Let('x', Num(2), Add(Var('x'), Num(3)))
        >>> e1 = Let('x', e0, Mul(Var('x'), Num(10)))
        >>> e0.identifier == e1.identifier
        True

        >>> e0 = Let('x', Num(2), Add(Var('x'), Num(3)))
        >>> e1 = Let('x', e0, Mul(Var('x'), Num(10)))
        >>> r = RenameVisitor()
        >>> e1.accept(r, {})
        >>> e0.identifier == e1.identifier
        False

        >>> x0 = Var('x')
        >>> x1 = Var('x')
        >>> e0 = Let('x', Num(2), Add(x0, Num(3)))
        >>> e1 = Let('x', e0, Mul(x1, Num(10)))
        >>> x0.identifier == x1.identifier
        True

        >>> x0 = Var('x')
        >>> x1 = Var('x')
        >>> e0 = Let('x', Num(2), Add(x0, Num(3)))
        >>> e1 = Let('x', e0, Mul(x1, Num(10)))
        >>> r = RenameVisitor()
        >>> e1.accept(r, {})
        >>> x0.identifier == x1.identifier
        False
    """
    
    def visit_var(self, exp, arg):
        exp.identifier = arg[exp.identifier]

    def visit_bln(self, exp, arg):
        return

    def visit_num(self, exp, arg):
        return

    def visit_eql(self, exp, arg):
        exp.left.accept(self, arg)
        exp.right.accept(self, arg)

    def visit_add(self, exp, arg):
        exp.left.accept(self, arg)
        exp.right.accept(self, arg)

    def visit_sub(self, exp, arg):
        exp.left.accept(self, arg)
        exp.right.accept(self, arg)

    def visit_mul(self, exp, arg):
        exp.left.accept(self, arg)
        exp.right.accept(self, arg)

    def visit_div(self, exp, arg):
        exp.left.accept(self, arg)
        exp.right.accept(self, arg)

    def visit_leq(self, exp, arg):
        exp.left.accept(self, arg)
        exp.right.accept(self, arg)

    def visit_lth(self, exp, arg):
        exp.left.accept(self, arg)
        exp.right.accept(self, arg)

    def visit_neg(self, exp, arg):
        exp.exp.accept(self, arg)

    def visit_not(self, exp, arg):
        exp.exp.accept(self, arg)

    def visit_let(self, exp, arg):
        c = exp.identifier
        exp.exp_def.accept(self, arg)
        if exp.identifier in arg.keys():
            _, n = arg[exp.identifier].split("_")
            n = int(n)
            arg[exp.identifier] = f"{exp.identifier}_{str(n+1)}"

            exp.identifier = f"{exp.identifier}_{str(n+1)}"

            
            exp.exp_body.accept(self, arg)

            arg[c] = f"{c}_{str(n)}"
        else:
            arg[exp.identifier] = f"{exp.identifier}_0"
            exp.identifier = f"{exp.identifier}_0"

            exp.exp_body.accept(self, arg)

            arg.pop(c)


class GenVisitor(Visitor):
    """
    The GenVisitor class compiles arithmetic expressions into a low-level
    language.
    """

    def __init__(self):
        self.next_var_counter = 0

    def next_var_name(self):
        self.next_var_counter += 1
        return f"v{self.next_var_counter}"

    def visit_var(self, exp, prog):
        """
        Usage:
            >>> e = Var('x')
            >>> p = AsmModule.Program({"x":1}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            1
        """
        return exp.identifier

    def visit_bln(self, exp, prog):
        """
        Usage:
            >>> e = Bln(True)
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            1

            >>> e = Bln(False)
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            0
        """
        if exp.bln == True or exp.bln == "True":
            var_name = self.next_var_name()
            prog.add_inst(AsmModule.Addi(var_name, "x0", 1))
            return var_name
        else:
            return "x0"

    def visit_num(self, exp, prog):
        """
        Usage:
            >>> e = Num(13)
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            13
        """
        var_name = self.next_var_name()
        prog.add_inst(AsmModule.Addi(var_name, "x0", exp.num))
        return var_name

    def visit_eql(self, exp, prog):
        """
        >>> e = Eql(Num(13), Num(13))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Eql(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Eql(Num(-1), Num(1))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0
        """
        l_name = exp.left.accept(self, prog)
        r_name = exp.right.accept(self, prog) 

        vsub1_name = self.next_var_name()
        vsub2_name = self.next_var_name()
        vslt1_name = self.next_var_name()
        vslt2_name = self.next_var_name()
        vxor_name = self.next_var_name()
        var_name = self.next_var_name()

        prog.add_inst(AsmModule.Sub(vsub1_name, l_name, r_name))
        prog.add_inst(AsmModule.Sub(vsub2_name, r_name, l_name))
        prog.add_inst(AsmModule.Slt(vslt1_name, vsub1_name, "x0"))
        prog.add_inst(AsmModule.Slt(vslt2_name, vsub2_name, "x0"))

        prog.add_inst(AsmModule.Xor(vxor_name, vslt1_name, vslt2_name))
        prog.add_inst(AsmModule.Xori(var_name, vxor_name, 1))

        return var_name

    def visit_add(self, exp, prog):
        """
        >>> e = Add(Num(13), Num(-13))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0
        >>> e = Add(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        23
        """
        l_name = exp.left.accept(self, prog)
        r_name = exp.right.accept(self, prog) 

        var_name = self.next_var_name()

        prog.add_inst(AsmModule.Add(var_name, l_name, r_name))
        return var_name

    def visit_sub(self, exp, prog):
        """
        >>> e = Sub(Num(13), Num(-13))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        26

        >>> e = Sub(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        3
        """
        l_name = exp.left.accept(self, prog)
        r_name = exp.right.accept(self, prog) 

        var_name = self.next_var_name()

        prog.add_inst(AsmModule.Sub(var_name, l_name, r_name))
        return var_name

    def visit_mul(self, exp, prog):
        """
        >>> e = Mul(Num(13), Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        26

        >>> e = Mul(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        130
        """
        l_name = exp.left.accept(self, prog)
        r_name = exp.right.accept(self, prog) 

        var_name = self.next_var_name()

        prog.add_inst(AsmModule.Mul(var_name, l_name, r_name))
        return var_name

    def visit_div(self, exp, prog):
        """
        >>> e = Div(Num(13), Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        6

        >>> e = Div(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1
        """
        l_name = exp.left.accept(self, prog)
        r_name = exp.right.accept(self, prog) 

        var_name = self.next_var_name()

        prog.add_inst(AsmModule.Div(var_name, l_name, r_name))
        return var_name

    def visit_leq(self, exp, prog):
        """
        >>> e = Leq(Num(3), Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Leq(Num(3), Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Leq(Num(2), Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Leq(Num(-3), Num(-2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Leq(Num(-3), Num(-3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Leq(Num(-2), Num(-3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0
        """
        l_name = exp.left.accept(self, prog)
        r_name = exp.right.accept(self, prog) 

        varthan_name = self.next_var_name()

        prog.add_inst(AsmModule.Slt(varthan_name, l_name, r_name))

        vsub1_name = self.next_var_name()
        vsub2_name = self.next_var_name()
        vslt1_name = self.next_var_name()
        vslt2_name = self.next_var_name()
        vxor_name = self.next_var_name()
        varequal_name = self.next_var_name()

        prog.add_inst(AsmModule.Sub(vsub1_name, l_name, r_name))
        prog.add_inst(AsmModule.Sub(vsub2_name, r_name, l_name))
        prog.add_inst(AsmModule.Slt(vslt1_name, vsub1_name, "x0"))
        prog.add_inst(AsmModule.Slt(vslt2_name, vsub2_name, "x0"))

        prog.add_inst(AsmModule.Xor(vxor_name, vslt1_name, vslt2_name))
        prog.add_inst(AsmModule.Xori(varequal_name, vxor_name, 1))

        vsum_name = self.next_var_name()
        var_name = self.next_var_name()

        prog.add_inst(AsmModule.Add(vsum_name, varequal_name, varthan_name))
        prog.add_inst(AsmModule.Slt(var_name, "x0", vsum_name))

        return var_name


    def visit_lth(self, exp, prog):
        """
        >>> e = Lth(Num(3), Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Lth(Num(3), Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Lth(Num(2), Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1
        """
        l_name = exp.left.accept(self, prog)
        r_name = exp.right.accept(self, prog) 

        var_name = self.next_var_name()

        prog.add_inst(AsmModule.Slt(var_name, l_name, r_name))

        return var_name
        

    def visit_neg(self, exp, prog):
        """
        >>> e = Neg(Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        -3

        >>> e = Neg(Num(0))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Neg(Num(-3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        3
        """
        value_name = exp.exp.accept(self, prog)
        vone_name = self.next_var_name()
        var_name = self.next_var_name()

        prog.add_inst(AsmModule.Addi(vone_name, "x0", 1))
        prog.add_inst(AsmModule.Sub(vone_name, "x0", vone_name))
        prog.add_inst(AsmModule.Mul(var_name, value_name, vone_name))

        return var_name


    def visit_not(self, exp, prog):
        """
        >>> e = Not(Bln(True))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Not(Bln(False))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Not(Num(0))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Not(Num(-2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Not(Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0
        """
        value_name = exp.exp.accept(self, prog)
        var_name = self.next_var_name()

        vt1 = self.next_var_name()
        vt2 = self.next_var_name()

        prog.add_inst(AsmModule.Slt(vt1, value_name, "x0"))
        prog.add_inst(AsmModule.Slt(vt2, "x0", value_name))

        prog.add_inst(AsmModule.Add(vt1, vt1, vt2))
        prog.add_inst(AsmModule.Slt(vt2, "x0", vt1))

        prog.add_inst(AsmModule.Xori(var_name, vt2, 1))

        return var_name

    def visit_let(self, exp, prog):
        """
        Usage:
            >>> e = Let('v', Not(Bln(False)), Var('v'))
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            1

            >>> e = Let('v', Num(2), Add(Var('v'), Num(3)))
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            5

            >>> e0 = Let('x', Num(2), Add(Var('x'), Num(3)))
            >>> e1 = Let('y', e0, Mul(Var('y'), Num(10)))
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e1.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            50
        """
        unique_name = exp.identifier

        d_name = exp.exp_def.accept(self, prog)
        prog.add_inst(AsmModule.Addi(unique_name, d_name, 0))

        var_name = exp.exp_body.accept(self, prog)
        return var_name
    

if __name__ == "__main__":
    e0 = Let('x', Num(2), Add(Var('x'), Num(3)))
    e1 = Let('x', e0, Mul(Var('x'), Num(10)))
    r = RenameVisitor()
    e1.accept(r, {})
    print(e0.identifier, e1.identifier)