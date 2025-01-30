import sys

from Expression import *
from Lexer import Token, TokenType

"""
This file implements the parser of arithmetic expressions.

References:
    see https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm
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
        >>> exp.eval(None)
        123

        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        True

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        False

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.NUM)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        -123

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        12

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        -12

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('/', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        7

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        7

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval(None)
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
        >>> exp.eval(None)
        14

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        False

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('4', TokenType.NUM)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> exp.eval(None)
        True

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.ASN)
        >>> tk3 = Token('42', TokenType.NUM)
        >>> tk4 = Token('in', TokenType.INX)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> exp.eval({})
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
        >>> exp.eval({})
        42
        """
        return self.no()
    
    def eat(self, token_type):
        if self.tokens[self.cur_token_idx].kind == token_type:
            self.cur_token_idx += 1
        else:
            raise ValueError(f"Unexpected token: {self.tokens[self.cur_token_idx].text}")

    def no(self):
        if self.tokens[self.cur_token_idx].kind == TokenType.NOT:
            self.eat(TokenType.NOT)
            return Not(self.eq())
        return self.eq()

    def eq(self):
        result = self.expr()

        while self.cur_token_idx < len(self.tokens) and self.tokens[self.cur_token_idx].kind in [TokenType.EQL, TokenType.LEQ, TokenType.LTH]:
            if self.tokens[self.cur_token_idx].kind == TokenType.EQL:
                self.eat(TokenType.EQL)
                result = Eql(result, self.expr())
            elif self.tokens[self.cur_token_idx].kind == TokenType.LEQ:
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
            result = self.expr()
            return Neg(result)
        elif crr_token.kind == TokenType.TRU:
            self.eat(TokenType.TRU)
            return Bln("True")
        elif crr_token.kind == TokenType.FLS:
            self.eat("False")
            return Bln(crr_token.text)
        elif crr_token.kind == TokenType.LPR:
            self.eat(TokenType.LPR)
            result = self.no()
            self.eat(TokenType.RPR)
            return result
        elif crr_token.kind == TokenType.LET:
            self.eat(TokenType.LET)
            var = self.tokens[self.cur_token_idx]
            self.eat(TokenType.VAR)
            self.eat(TokenType.ASN)
            exp_def = self.no()
            self.eat(TokenType.INX)
            exp_body = self.no()
            self.eat(TokenType.END)

            return Let(var.text, exp_def, exp_body)

        else:
            print(crr_token.kind)
            raise ValueError()