import sys
import re
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
    VAR = 7   # An identifier
    LET = 8   # The 'let' of the let expression
    INX = 9   # The 'in' of the let expression
    END = 10  # The 'end' of the let expression
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
    ASN = 212 # The assignment '<-' operator


class Lexer:
    
    def __init__(self, source):
        """
        The constructor of the lexer. It receives the string that shall be
        scanned.
        TODO: You will need to implement this method.
        """
        self.source = source
        self.var_expected = False

    def tokens(self):
        """
        This method is a token generator: it converts the string encapsulated
        into this object into a sequence of Tokens. Examples:

        >>> l = Lexer("1 + 3")
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.ADD: 202>, <TokenType.NUM: 3>]

        >>> l = Lexer('1 * 2 -- 3\\n')
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.MUL: 204>, <TokenType.NUM: 3>]

        >>> l = Lexer("1 + var")
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.ADD: 202>, <TokenType.VAR: 7>]

        >>> l = Lexer("let v <- 2 in v end")
        >>> [tk.kind.name for tk in l.tokens()]
        ['LET', 'VAR', 'ASN', 'NUM', 'INX', 'VAR', 'END']
        """
        token = self.getToken()
        while token.kind != TokenType.EOF:
            if token.kind != TokenType.WSP and token.kind != TokenType.COM:
                yield token
            token = self.getToken()

    def getToken(self):
        if len(self.source.strip()) == 0:
            return Token("", TokenType.EOF)

        self.source = self.source.lstrip()

        if self.source[:2] == "--":
            idx = self.source.find("\n")
            if idx != -1:
                self.source = self.source[idx+1:]
            else:
                self.source = str()
            return Token("", TokenType.COM)
        
        if self.source[:2] == "(*":
            idx = self.source.find("*)")
            if idx == -1:
                raise Exception("Comment was not finished.")
            else:
                self.source = self.source[idx+2:]
                return Token("", TokenType.COM)

        number_pattern = r"^\d+"
        identifier_pattern = r"^[a-zA-Z_]\w*"
        operator_pattern = r"^(\+|\-|\*|\/|<-|<=|<|=|~|\(|\))"
        keyword_patterns = {
            "let": TokenType.LET,
            "in": TokenType.INX,
            "end": TokenType.END,
            "not": TokenType.NOT,
            "true": TokenType.TRU,
            "false": TokenType.FLS
        }

        if self.var_expected:
            match = re.match(identifier_pattern, self.source)
            if match:
                var_name = match.group(0)
                self.source = self.source[len(var_name):]
                self.var_expected = False
                return Token(var_name, TokenType.VAR)

        # Check for numbers
        match = re.match(number_pattern, self.source)
        if match:
            number = match.group(0)
            self.source = self.source[len(number):]
            return Token(int(number), TokenType.NUM)

        match = re.match(identifier_pattern, self.source)
        if match:
            identifier = match.group(0)
            self.source = self.source[len(identifier):]

            if identifier in keyword_patterns:
                token_type = keyword_patterns[identifier]
                if token_type == TokenType.LET:
                    self.var_expected = True 
                return Token(identifier, token_type)
            else:
                return Token(identifier, TokenType.VAR)

        match = re.match(operator_pattern, self.source)
        if match:
            operator = match.group(0)
            self.source = self.source[len(operator):]
            token_map = {
                "+": TokenType.ADD,
                "-": TokenType.SUB,
                "*": TokenType.MUL,
                "/": TokenType.DIV,
                "<=": TokenType.LEQ,
                "<": TokenType.LTH,
                "=": TokenType.EQL,
                "~": TokenType.NEG,
                "(": TokenType.LPR,
                ")": TokenType.RPR,
                "<-": TokenType.ASN
            }
            return Token(operator, token_map.get(operator, TokenType.EOF))

        raise Exception("Unrecognized semantic.")