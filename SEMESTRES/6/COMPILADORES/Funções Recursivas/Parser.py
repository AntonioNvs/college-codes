import sys

from Expression import *
from Visitor import *
from Lexer import Token, TokenType

"""
This file implements a parser for SML with anonymous functions. The grammar is
as follows:

fn_exp  ::= fn <var> => fn_exp
          | if_exp
if_exp  ::= <if> if_exp <then> fn_exp <else> fn_exp
          | or_exp
or_exp  ::= and_exp (or and_exp)*
and_exp ::= eq_exp (and eq_exp)*
eq_exp  ::= cmp_exp (= cmp_exp)*
cmp_exp ::= add_exp ([<=|<] add_exp)*
add_exp ::= mul_exp ([+|-] mul_exp)*
mul_exp ::= uny_exp ([*|div|mod] uny_exp)*
uny_exp ::= <not> uny_exp
          | ~ uny_exp
          | let_exp
let_exp ::= <let> decl <in> fn_exp <end>
          | val_exp
val_exp ::= val_tk (val_tk)*
val_tk  ::= <var> | ( fn_exp ) | <num> | <true> | <false>

decl    ::= val <var> = fn_exp
          | fun <var> <var> = fn_exp

References:
    see https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm#classic
"""

class Parser:
    def __init__(self, tokens):
        """
        Initializes the parser. The parser keeps track of the list of tokens
        and the current token. For instance:
        """
        self.tokens = list(tokens)
        self.cur_token_idx = 0 # This is just a suggestion!
        # TODO: you might want to implement more stuff in the initializer :)

    def parse(self):
        """
        Returns the expression associated with the stream of tokens.

        Examples:
        >>> parser = Parser([Token('123', TokenType.NUM)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        123

        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.NUM)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -123

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        12

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -12

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('div', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        26

        >>> tk0 = Token('2', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('(', TokenType.LPR)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('4', TokenType.NUM)
        >>> tk6 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        14

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('(', TokenType.LPR)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> tk3 = Token('<', TokenType.LTH)
        >>> tk4 = Token('4', TokenType.NUM)
        >>> tk5 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('or', TokenType.ORX)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('and', TokenType.AND)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('val', TokenType.VAL)
        >>> tk2 = Token('v', TokenType.VAR)
        >>> tk3 = Token('=', TokenType.EQL)
        >>> tk4 = Token('42', TokenType.NUM)
        >>> tk5 = Token('in', TokenType.INX)
        >>> tk6 = Token('v', TokenType.VAR)
        >>> tk7 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('val', TokenType.VAL)
        >>> tk2 = Token('v', TokenType.VAR)
        >>> tk3 = Token('=', TokenType.EQL)
        >>> tk4 = Token('21', TokenType.NUM)
        >>> tk5 = Token('in', TokenType.INX)
        >>> tk6 = Token('v', TokenType.VAR)
        >>> tk7 = Token('+', TokenType.ADD)
        >>> tk8 = Token('v', TokenType.VAR)
        >>> tk9 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7, tk8, tk9])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('if', TokenType.IFX)
        >>> tk1 = Token('2', TokenType.NUM)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('then', TokenType.THN)
        >>> tk5 = Token('1', TokenType.NUM)
        >>> tk6 = Token('else', TokenType.ELS)
        >>> tk7 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        1

        >>> tk0 = Token('if', TokenType.IFX)
        >>> tk1 = Token('false', TokenType.FLS)
        >>> tk2 = Token('then', TokenType.THN)
        >>> tk3 = Token('1', TokenType.NUM)
        >>> tk4 = Token('else', TokenType.ELS)
        >>> tk5 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        2

        >>> tk0 = Token('fn', TokenType.FNX)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('=>', TokenType.ARW)
        >>> tk3 = Token('v', TokenType.VAR)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('1', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> print(exp.accept(ev, None))
        Fn(v)

        >>> tk0 = Token('(', TokenType.LPR)
        >>> tk1 = Token('fn', TokenType.FNX)
        >>> tk2 = Token('v', TokenType.VAR)
        >>> tk3 = Token('=>', TokenType.ARW)
        >>> tk4 = Token('v', TokenType.VAR)
        >>> tk5 = Token('+', TokenType.ADD)
        >>> tk6 = Token('1', TokenType.NUM)
        >>> tk7 = Token(')', TokenType.RPR)
        >>> tk8 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7, tk8])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        3

        >>> t0 = Token('let', TokenType.LET)
        >>> t1 = Token('fun', TokenType.FUN)
        >>> t2 = Token('f', TokenType.VAR)
        >>> t3 = Token('v', TokenType.VAR)
        >>> t4 = Token('=', TokenType.EQL)
        >>> t5 = Token('v', TokenType.VAR)
        >>> t6 = Token('+', TokenType.ADD)
        >>> t7 = Token('v', TokenType.VAR)
        >>> t8 = Token('in', TokenType.INX)
        >>> t9 = Token('f', TokenType.VAR)
        >>> tA = Token('2', TokenType.NUM)
        >>> tB = Token('end', TokenType.END)
        >>> parser = Parser([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, tA, tB])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        4
        """
        return self.fnx()
    
    def eat(self, token_type):
        if self.tokens[self.cur_token_idx].kind == token_type:
            self.cur_token_idx += 1
        else:
            raise ValueError(f"Unexpected token: {self.tokens[self.cur_token_idx].kind} - {self.tokens[self.cur_token_idx].text}")

    def fnx(self):
        if self.tokens[self.cur_token_idx].kind == TokenType.FNX:
            self.eat(TokenType.FNX)
            var = self.tokens[self.cur_token_idx]
            self.eat(TokenType.VAR)
            self.eat(TokenType.ARW)
            fn_body = self.fnx()            

            return Fn(var.text, fn_body)
        return self.if_then_elses()
    
    def if_then_elses(self):
        if self.tokens[self.cur_token_idx].kind == TokenType.IFX:
            self.eat(TokenType.IFX)
            cond = self.if_then_elses()
            self.eat(TokenType.THN)
            e0 = self.if_then_elses()
            self.eat(TokenType.ELS)
            e1 = self.if_then_elses()
            return IfThenElse(cond, e0, e1)
        
        return self.orx()

    def orx(self):
        result = self.and_()

        if self.cur_token_idx < len(self.tokens) and self.tokens[self.cur_token_idx].kind == TokenType.ORX:
            self.eat(TokenType.ORX)
            result = Or(result, self.and_())
        
        return result

    def and_(self):
        result = self.eq()

        if self.cur_token_idx < len(self.tokens) and self.tokens[self.cur_token_idx].kind == TokenType.AND:
            self.eat(TokenType.AND)
            result = And(result, self.eq())
        
        return result

    def eq(self):
        result = self.comp()

        if self.cur_token_idx < len(self.tokens) and self.tokens[self.cur_token_idx].kind == TokenType.EQL:
            self.eat(TokenType.EQL)
            result = Eql(result, self.comp())
        
        return result

    def comp(self):
        result = self.expr()

        while self.cur_token_idx < len(self.tokens) and self.tokens[self.cur_token_idx].kind in [TokenType.LEQ, TokenType.LTH]:
            if self.tokens[self.cur_token_idx].kind == TokenType.LEQ:
                self.eat(TokenType.LEQ)
                result = Leq(result, self.expr())
            elif self.tokens[self.cur_token_idx].kind == TokenType.LTH:
                self.eat(TokenType.LTH)
                result = Lth(result, self.expr())

        return result

    def expr(self):
        result = self.term()

        while self.cur_token_idx < len(self.tokens) and self.tokens[self.cur_token_idx].kind in [TokenType.ADD, TokenType.SUB]:
            if self.tokens[self.cur_token_idx].kind == TokenType.ADD:
                self.eat(TokenType.ADD)
                result = Add(result, self.term())
            elif self.tokens[self.cur_token_idx].kind == TokenType.SUB:
                self.eat(TokenType.SUB)
                result = Sub(result, self.term())
        return result
    
    def term(self):
        result = self.unary()

        while self.cur_token_idx < len(self.tokens) and self.tokens[self.cur_token_idx].kind in [TokenType.MUL, TokenType.DIV, TokenType.MOD]:
            if self.tokens[self.cur_token_idx].kind == TokenType.MUL:
                self.eat(TokenType.MUL)
                result = Mul(result, self.unary())
            elif self.tokens[self.cur_token_idx].kind == TokenType.DIV:
                self.eat(TokenType.DIV)
                result = Div(result, self.unary())
            elif self.tokens[self.cur_token_idx].kind == TokenType.MOD:
                self.eat(TokenType.MOD)
                result = Mod(result, self.unary())
        return result
    
    def unary(self):
        crr_token = self.tokens[self.cur_token_idx]

        if crr_token.kind == TokenType.NEG:
            self.eat(TokenType.NEG)
            result = self.unary()
            return Neg(result)
        elif crr_token.kind == TokenType.NOT:
            self.eat(TokenType.NOT)
            return Not(self.unary())
        
        return self.let_exp()    

    def let_exp(self):
        if self.tokens[self.cur_token_idx].kind == TokenType.LET:
            self.eat(TokenType.LET)
            var_name, var_def = self.decl()
            self.eat(TokenType.INX)
            exp_body = self.fnx()
            self.eat(TokenType.END)

            return Let(var_name, var_def, exp_body)
        
        return self.val_exp()

    def val_exp(self):
        result = self.val_tkn()

        while self.cur_token_idx < len(self.tokens) and \
            self.tokens[self.cur_token_idx].kind in [TokenType.NUM, TokenType.VAR, TokenType.TRU, TokenType.FLS, TokenType.LPR]:
            result = App(result, self.val_tkn())
        return result

    def val_tkn(self):
        crr_token = self.tokens[self.cur_token_idx]

        if crr_token.kind == TokenType.NUM:
            self.eat(TokenType.NUM)
            return Num(crr_token.text)
        elif crr_token.kind == TokenType.VAR:
            self.eat(TokenType.VAR)
            return Var(crr_token.text)
        elif crr_token.kind == TokenType.TRU:
            self.eat(TokenType.TRU)
            return Bln("True")
        elif crr_token.kind == TokenType.FLS:
            self.eat(TokenType.FLS)
            return Bln("False")
        elif crr_token.kind == TokenType.LPR:
            self.eat(TokenType.LPR)
            result = self.fnx()
            self.eat(TokenType.RPR)
            return result
        else:
            sys.exit("Parse error")

    def decl(self):
        crr_token = self.tokens[self.cur_token_idx]

        if crr_token.kind == TokenType.VAL:
            self.eat(TokenType.VAL)
            var = self.tokens[self.cur_token_idx]
            self.eat(TokenType.VAR)
            self.eat(TokenType.EQL)
            exp_def = self.fnx()

            return var.text, exp_def
        elif crr_token.kind == TokenType.FUN:
            self.eat(TokenType.FUN)
            fun_var = self.tokens[self.cur_token_idx]
            self.eat(TokenType.VAR)
            fun_param = self.tokens[self.cur_token_idx]
            self.eat(TokenType.VAR)
            self.eat(TokenType.EQL)
            fun_body = self.fnx()

            return fun_var.text, Fun(fun_var.text, fun_param.text, fun_body)
        else:
            sys.exit("Parse error")