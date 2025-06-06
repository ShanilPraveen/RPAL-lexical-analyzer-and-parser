from Lexer import Lexer
from parser import Parser
from environment import Environment

def test_ast_standardize_and_interpret():
    code = "let x = 3 in x + 2"
    lexer = Lexer(code)
    lexer.tokenize()
    parser = Parser(lexer.tokens)
    ast = parser.parse_E()

    st = ast.standardize()

    # Global environment
    env = Environment()
    env.defineBuiltInFunctions()

    result = st.interpret(env)
    assert result == 5  # 3 + 2 = 5
