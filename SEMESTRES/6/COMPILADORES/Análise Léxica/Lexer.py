import sys
import enum


class Token:
    """
    This class contains the definition of Tokens. A token has two fields: its
    text and its kind. The "kind" of a token is a constant that identifies it
    uniquely. See the TokenType to know the possible identifiers (if you want).
    You don't need to change this class.
    """
    def __init__(self, tokenText, tokenKind):
        # The token's actual text. Used for identifiers, strings, and numbers.
        self.text = tokenText
        # The TokenType that this token is classified as.
        self.kind = tokenKind


class TokenType(enum.Enum):
    """
    These are the possible tokens. You don't need to change this class at all.
    """
    EOF = -1  # End of file
    NLN = 0   # New line
    WSP = 1   # White Space
    COM = 2   # Comment
    NUM = 3   # Number (integers)
    STR = 4   # Strings
    TRU = 5   # The constant true
    FLS = 6   # The constant false
    EQL = 201
    ADD = 202
    SUB = 203
    MUL = 204
    DIV = 205
    LEQ = 206
    LTH = 207
    NEG = 208
    NOT = 209
    LPR = 210
    RPR = 211


class Lexer:
    
    def __init__(self, source):
        """
        The constructor of the lexer. It receives the string that shall be
        scanned.
        TODO: You will need to implement this method.
        """
        self.source = source

    def tokens(self):
        """
        This method is a token generator: it converts the string encapsulated
        into this object into a sequence of Tokens. Examples:

        >>> l = Lexer('1 * 2 - 3')
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.ADD: 202>, <TokenType.NUM: 3>]

        >>> l = Lexer('1 * 2 -- 3\\n')
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.MUL: 204>, <TokenType.NUM: 3>]
        """
        token = self.getToken()
        while token.kind != TokenType.EOF:
            if token.kind != TokenType.WSP and token.kind != TokenType.COM:
                yield token
            token = self.getToken()

    def getToken(self):
        """
        Return the next token.
        TODO: Implement this method!
        """
        if len(self.source) == 0:
            return Token("", TokenType.EOF)
        
        text = ""
        while len(self.source) != 0 and self.source[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            text += self.source[0]
            self.source = self.source[1:]

        if text == "": 
            text = self.source[0]
            self.source = self.source[1:]

            if text == "<" and len(self.source) > 0 and self.source[0] == "=":
                text = "<="
                self.source = self.source[1:]

            if text == "-" and len(self.source) > 0 and self.source[0] == "-":
                i = 1
                while len(self.source)-i and self.source[i] != '\n': 
                    i += 1
        
                self.source = self.source[i+1:]
                return Token("", TokenType.WSP)
            
            if text == "(" and len(self.source) > 0 and self.source[0] == "*":
                i = 1
                while len(self.source)-i and self.source[i:i+2] != "*)":
                    i += 1
                
                self.source = self.source[i+2:]
                return Token("", TokenType.WSP)
            
            if text == "n" and self.source[0:2] == "ot":
                text = "not"
                self.source = self.source[2:]
            
            if text == "t" and self.source[0:3] == "rue":
                text = "true"
                self.source = self.source[3:]

            if text == "f" and self.source[0:4] == "alse":
                text = "false"
                self.source = self.source[4:]

        if text == "+":
            token = Token("+", TokenType.ADD)
        elif text == "-":
            token = Token("-", TokenType.SUB)
        elif text == "*":
            token = Token("*", TokenType.MUL)
        elif text == "/":
            token = Token("/", TokenType.DIV)
        elif text == " ":
            token = Token("WSP", TokenType.WSP)
        elif text == "<=":
            token = Token("<=", TokenType.LEQ)
        elif text == "<":
            token = Token("<", TokenType.LTH)
        elif text == "=":
            token = Token("=", TokenType.EQL)
        elif text == "~":
            token = Token("~", TokenType.NEG)
        elif text == "(":
            token = Token("(", TokenType.LPR)
        elif text == ")":
            token = Token(")", TokenType.RPR)
        elif text == "\n":
            token = Token("", TokenType.NLN)
        elif text == "not":
            token = Token("not", TokenType.NOT)
        elif text == "true":
            token = Token("true", TokenType.TRU)
        elif text == "false":
            token = Token("false", TokenType.FLS)
        else:
            token = Token(int(text), TokenType.NUM)

        return token