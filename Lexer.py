import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f'{self.type} "{self.value}"'

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.keywords = {
            'let', 'in', 'where', 'within', 'and', 'nil', 'aug',
            'rec', 'fn', 'lambda', 'true', 'false', 'dummy',
        }

        self.token_specification = [
            ('KEYWORD',   r'\b(?:' + '|'.join(self.keywords) + r')\b'),
            ('COMMENT',    r'//.*'),
            ('STRING',     r"'([^'\\]|\\.)*'"),
            ('INTEGER',    r'\d+'),
            ('OPERATOR',   r'eq|ne|gr|ge|ls|le|<=|>=|->|\*\*|=>|[+\-*/=<>&|@]'),
            ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]*'),
            ('PUNCTION',  r'[()\[\]{},;.]'),
            ('WHITESPACE', r'\s+'),
            ('UNKNOWN',    r'.'),
        ]

        self.regex = re.compile(
            '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification),
            re.DOTALL
        )

    def tokenize(self):
        for match in self.regex.finditer(self.code):
            kind = match.lastgroup
            value = match.group()

            if kind == 'WHITESPACE' or kind == 'COMMENT':
                continue

            if kind == 'KEYWORD':
                self.tokens.append(Token(value, value))
            elif kind == 'UNKNOWN':
                print(f"Unknown token: {value}")
            else:
                self.tokens.append(Token(kind.lower(), value))



