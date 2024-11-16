import sys

from Expression import *
from Lexer import Token, TokenType

"""
This file implements the parser of logic and arithmetic expressions.

Precedence table:
    1: not ~ ()
    2: *   /
    3: +   -
    4: <   <=   >=   >
    5: =
    6: and
    7: or
    8: if-then-else

Notice that not 2 < 3 must be a type error, as we are trying to apply a boolean
operation (not) onto a number.

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
        >>> tk1 = Token('/', TokenType.DIV)
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
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.ASN)
        >>> tk3 = Token('42', TokenType.NUM)
        >>> tk4 = Token('in', TokenType.INX)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.ASN)
        >>> tk3 = Token('21', TokenType.NUM)
        >>> tk4 = Token('in', TokenType.INX)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('+', TokenType.ADD)
        >>> tk7 = Token('v', TokenType.VAR)
        >>> tk8 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7, tk8])
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
        """
        return self.if_then_elses()
    
    def eat(self, token_type):
        if self.tokens[self.cur_token_idx].kind == token_type:
            self.cur_token_idx += 1
        else:
            raise ValueError(f"Unexpected token: {self.tokens[self.cur_token_idx].kind} - {self.tokens[self.cur_token_idx].text}")

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
        result = self.factor()

        while self.cur_token_idx < len(self.tokens) and self.tokens[self.cur_token_idx].kind in [TokenType.MUL, TokenType.DIV]:
            if self.tokens[self.cur_token_idx].kind == TokenType.MUL:
                self.eat(TokenType.MUL)
                result = Mul(result, self.factor())
            elif self.tokens[self.cur_token_idx].kind == TokenType.DIV:
                self.eat(TokenType.DIV)
                result = Div(result, self.factor())
        return result
    
    def factor(self):
        crr_token = self.tokens[self.cur_token_idx]

        if crr_token.kind == TokenType.NUM:
            self.eat(TokenType.NUM)
            return Num(crr_token.text)
        elif crr_token.kind == TokenType.VAR:
            self.eat(TokenType.VAR)
            return Var(crr_token.text)
        elif crr_token.kind == TokenType.NEG:
            self.eat(TokenType.NEG)
            result = self.factor()
            return Neg(result)
        elif crr_token.kind == TokenType.NOT:
            self.eat(TokenType.NOT)
            return Not(self.factor())
        elif crr_token.kind == TokenType.TRU:
            self.eat(TokenType.TRU)
            return Bln("True")
        elif crr_token.kind == TokenType.FLS:
            self.eat(TokenType.FLS)
            return Bln("False")
        elif crr_token.kind == TokenType.LPR:
            self.eat(TokenType.LPR)
            result = self.if_then_elses()
            self.eat(TokenType.RPR)
            return result
        elif crr_token.kind == TokenType.LET:
            self.eat(TokenType.LET)
            var = self.tokens[self.cur_token_idx]
            self.eat(TokenType.VAR)
            self.eat(TokenType.ASN)
            exp_def = self.if_then_elses()
            self.eat(TokenType.INX)
            exp_body = self.if_then_elses()
            self.eat(TokenType.END)

            return Let(var.text, exp_def, exp_body)
        else:
            sys.exit("Parse error")