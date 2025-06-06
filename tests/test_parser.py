from Lexer import Lexer
from parser import Parser

def test_parser_constructs_ast():
    code = "let x = 3 in x + 1"
    lexer = Lexer(code)
    lexer.tokenize()

    parser = Parser(lexer.tokens)
    ast = parser.parse_E()

    assert ast is not None
    assert hasattr(ast, "standardize")
