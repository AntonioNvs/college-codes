import sys

from Visitor import ArrowType, TypeCheckVisitor
from Expression import *
from Lexer import Token, TokenType

"""
This file implements a parser for SML with anonymous functions and type
annotations. The grammar is as follows:

fn_exp  ::= fn <var>: types => fn_exp
          | if_exp
if_exp  ::= <if> if_exp <then> fn_exp <else> fn_exp
          | or_exp
or_exp  ::= and_exp (or and_exp)*
and_exp ::= eq_exp (and eq_exp)*
eq_exp  ::= cmp_exp (= cmp_exp)*
cmp_exp ::= add_exp ([<=|<] add_exp)*
add_exp ::= mul_exp ([+|-] mul_exp)*
mul_exp ::= unary_exp ([*|/] unary_exp)*
unary_exp ::= <not> unary_exp
             | ~ unary_exp
             | let_exp
let_exp ::= <let> <var>: types <- fn_exp <in> fn_exp <end>
          | val_exp
val_exp ::= val_tk (val_tk)*
val_tk ::= <var> | ( fn_exp ) | <num> | <true> | <false>

types ::= type -> types | type

type ::= int | bool | ( types )

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
        # You can (and probably should!) modify this method.

    def parse(self):
        """
        Returns the expression associated with the stream of tokens.

        Examples:
        >>> parser = Parser([Token('123', TokenType.NUM)])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'bool'>

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'bool'>

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.NUM)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('/', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> tk0 = Token('2', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('(', TokenType.LPR)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('4', TokenType.NUM)
        >>> tk6 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'bool'>

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'bool'>

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'bool'>

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('(', TokenType.LPR)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> tk3 = Token('<', TokenType.LTH)
        >>> tk4 = Token('4', TokenType.NUM)
        >>> tk5 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'bool'>

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('or', TokenType.ORX)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'bool'>

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('and', TokenType.AND)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'bool'>

        >>> t0 = Token('let', TokenType.LET)
        >>> t1 = Token('v', TokenType.VAR)
        >>> t2 = Token(':', TokenType.COL)
        >>> t3 = Token('int', TokenType.INT)
        >>> t4 = Token('<-', TokenType.ASN)
        >>> t5 = Token('42', TokenType.NUM)
        >>> t6 = Token('in', TokenType.INX)
        >>> t7 = Token('v', TokenType.VAR)
        >>> t8 = Token('end', TokenType.END)
        >>> parser = Parser([t0, t1, t2, t3, t4, t5, t6, t7, t8])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, {})
        <class 'int'>

        >>> t0 = Token('let', TokenType.LET)
        >>> t1 = Token('v', TokenType.VAR)
        >>> t2 = Token(':', TokenType.COL)
        >>> t3 = Token('int', TokenType.INT)
        >>> t4 = Token('<-', TokenType.ASN)
        >>> t5 = Token('21', TokenType.NUM)
        >>> t6 = Token('in', TokenType.INX)
        >>> t7 = Token('v', TokenType.VAR)
        >>> t8 = Token('+', TokenType.ADD)
        >>> t9 = Token('v', TokenType.VAR)
        >>> tA = Token('end', TokenType.END)
        >>> parser = Parser([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, tA])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, {})
        <class 'int'>

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
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> tk0 = Token('if', TokenType.IFX)
        >>> tk1 = Token('false', TokenType.FLS)
        >>> tk2 = Token('then', TokenType.THN)
        >>> tk3 = Token('1', TokenType.NUM)
        >>> tk4 = Token('else', TokenType.ELS)
        >>> tk5 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, None)
        <class 'int'>

        >>> tk0 = Token('fn', TokenType.FNX)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token(':', TokenType.COL)
        >>> tk3 = Token('int', TokenType.INT)
        >>> tk4 = Token('=>', TokenType.ARW)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('+', TokenType.ADD)
        >>> tk7 = Token('1', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> print(exp.accept(ev, {}))
        <class 'int'> -> <class 'int'>

        >>> t0 = Token('(', TokenType.LPR)
        >>> t1 = Token('fn', TokenType.FNX)
        >>> t2 = Token('v', TokenType.VAR)
        >>> t3 = Token(':', TokenType.COL)
        >>> t4 = Token('int', TokenType.INT)
        >>> t5 = Token('=>', TokenType.ARW)
        >>> t6 = Token('v', TokenType.VAR)
        >>> t7 = Token('+', TokenType.ADD)
        >>> t8 = Token('1', TokenType.NUM)
        >>> t9 = Token(')', TokenType.RPR)
        >>> tA = Token('2', TokenType.NUM)
        >>> parser = Parser([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, tA])
        >>> exp = parser.parse()
        >>> ev = TypeCheckVisitor()
        >>> exp.accept(ev, {})
        <class 'int'>
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
            self.eat(TokenType.COL)
            types = self.types()
            self.eat(TokenType.ARW)
            fn_body = self.fnx()            

            return Fn(var.text, types, fn_body)
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

        while self.cur_token_idx < len(self.tokens) and self.tokens[self.cur_token_idx].kind in [TokenType.MUL, TokenType.DIV]:
            if self.tokens[self.cur_token_idx].kind == TokenType.MUL:
                self.eat(TokenType.MUL)
                result = Mul(result, self.unary())
            elif self.tokens[self.cur_token_idx].kind == TokenType.DIV:
                self.eat(TokenType.DIV)
                result = Div(result, self.unary())
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
            var = self.tokens[self.cur_token_idx]
            self.eat(TokenType.VAR)
            self.eat(TokenType.COL)
            types = self.types()
            self.eat(TokenType.ASN)
            exp_def = self.fnx()
            self.eat(TokenType.INX)
            exp_body = self.fnx()
            self.eat(TokenType.END)
            return Let(var.text, types, exp_def, exp_body)
        
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


    def types(self):
        type_ = self.type_()
        if self.tokens[self.cur_token_idx].kind == TokenType.TPF:
            self.eat(TokenType.TPF)
            type_ = ArrowType(type_, self.types())
        
        return type_

    def type_(self):
        crr_token = self.tokens[self.cur_token_idx]

        if crr_token.kind == TokenType.INT:
            self.eat(TokenType.INT)
            return int
        elif crr_token.kind == TokenType.LGC:
            self.eat(TokenType.LGC)
            return bool
        elif crr_token.kind == TokenType.LPR:
            self.eat(TokenType.LPR)
            types = self.types()
            self.eat(TokenType.RPR)
            return types