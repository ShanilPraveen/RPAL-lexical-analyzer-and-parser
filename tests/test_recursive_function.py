from Lexer import Lexer
from parser import Parser
from environment import Environment

def test_recursive_sum():
    code = """
    let Sum(A) = Psum(A, Order A)
    where rec Psum(T,N) = N eq 0 -> 0 | Psum(T, N-1) + T N
    in Sum(1,2,3)
    """
    lexer = Lexer(code)
    lexer.tokenize()
    parser = Parser(lexer.tokens)
    ast = parser.parse_E()

    st = ast.standardize()
    env = Environment()
    env.defineBuiltInFunctions()

    result = st.interpret(env)
    assert result == 6  # 1 + 2 + 3 = 6
