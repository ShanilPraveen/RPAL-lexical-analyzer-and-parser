# import pytest
# from Lexer import Lexer
# from parser import Parser
# from environment import Environment
# from io import StringIO

# def evaluate_rpal_code(code: str):
#     lexer = Lexer(code)
#     lexer.tokenize()
#     parser = Parser(lexer.tokens)
#     ast = parser.parse_E()
#     st = ast.standardize()
#     env = Environment()
#     env.defineBuiltInFunctions()
#     return st.interpret(env)

# def test_builtin_functions():
#     cases = [
#         # Print returns dummy (side effect)
#         ("Print('hello')", "dummy"),

#         # Order returns length of tuple
#         ("Order(1,2,3)", 3),

#         # Stem returns first character
#         ("Stem('abc')", "a"),

#         # Stern returns rest of string
#         ("Stern('abc')", "bc"),

#         # Concatenation
#         ("Conc('ab','cd')", "abcd"),

#         # Isinteger tests
#         ("Isinteger(123)", "true"),
#         ("Isinteger('abc')", "false"),

#         # Isstring tests
#         ("Isstring('abc')", "true"),
#         ("Isstring(123)", "false"),

#         # Istuple
#         ("Istuple((1,2))", "true"),
#         ("Istuple(123)", "false"),

#         # Isdummy
#         ("Isdummy(dummy)", "true"),
#         ("Isdummy(1)", "false"),

#         # Istruthvalue
#         ("Istruthvalue(true)", "true"),
#         ("Istruthvalue('abc')", "false"),

#         # Itos
#         ("Itos(123)", "123"),

#         # Null
#         ("Null(nil)", "true"),
#         ("Null((1,2))", "false"),
#     ]

#     for code, expected in cases:
#         program = f"in {code}"  # Wrap expression to make it a valid RPAL 'E'
#         result = evaluate_rpal_code(program)

#         if hasattr(result, "value"):  # In case of dummy, boolean etc.
#             result = result.value
#         elif isinstance(result, str):
#             pass  # already string
#         elif isinstance(result, int):
#             result = str(result)
#         elif result is None:
#             result = "dummy"

#         assert str(result) == str(expected), f"Failed on: {code}, got {result}"
