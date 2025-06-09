from Lexer import Lexer
from parser import Parser
from environment import Environment

def test_print_builtin():
    code = "Print(1)"
    lexer = Lexer(code)
    lexer.tokenize()
    parser = Parser(lexer.tokens)
    ast = parser.parse_E()

    st = ast.standardize()
    env = Environment()
    env.defineBuiltInFunctions()

    result = st.interpret(env)
    assert result == "dummy"  # Print should return the value in your implementation

def test_order_builtin():
    code = "Order(1,2,3)"
    lexer = Lexer(code)
    lexer.tokenize()
    parser = Parser(lexer.tokens)
    ast = parser.parse_E()

    st = ast.standardize()
    env = Environment()
    env.defineBuiltInFunctions()

    result = st.interpret(env)
    assert result == 3 # Order should return the number of arguments

def test_stem_builtin():
    code = "Stem('abc')"
    lexer = Lexer(code)
    lexer.tokenize()
    parser = Parser(lexer.tokens)
    ast = parser.parse_E()

    st = ast.standardize()
    env = Environment()
    env.defineBuiltInFunctions()

    result = st.interpret(env)
    assert result == "a" # Stem should return the first character of the string

def test_itos_builtin():
    code = "ItoS(123)"
    lexer = Lexer(code)
    lexer.tokenize()
    parser = Parser(lexer.tokens)
    ast = parser.parse_E()

    st = ast.standardize()
    env = Environment()
    env.defineBuiltInFunctions()

    result = st.interpret(env)
    assert result == "123" # ItoS should convert integer to string
