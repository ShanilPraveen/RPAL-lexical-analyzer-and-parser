import sys
from Lexer import Lexer
from parser import Parser
from environment import Environment, BuiltInFunction

def read_file(filename):
    with open(filename,'r') as f:
        return f.read()


def main():
    # if len(sys.argv) < 2 :
    #     print("Usage: python myrpal.py <filename> [-ast]")
    #     return

    # filename = sys.argv[1]
    # show_ast_only = "-ast" in sys.argv

    code = """  let Is_perfect_Square N =
 Has_sqrt_ge (N,1)
 where
 rec Has_sqrt_ge (N,R) =
 R**2 gr N -> false
 | R**2 eq N -> true
 | Has_sqrt_ge (N,R+1)
 in Print (Is_perfect_Square 4,
 Is_perfect_Square 64,
 Is_perfect_Square 3)
"""

    lexer = Lexer(code)
    lexer.tokenize()
    # print("Tokens: "+str(lexer.tokens))

    parser = Parser(lexer.tokens)

    try:
        ast = parser.parse_E()
        # ast.print()
        st = ast.standardize()
        st.print()
        global_env = Environment()
        global_env.define("Print", BuiltInFunction("Print"))
        global_env.define("Y*", BuiltInFunction("Y*"))
        global_env.define("Order", BuiltInFunction("Order"))

        print("\n--- Program Output ---")
        final_result = st.interpret(global_env)
        print("--- End Program Output ---")
        print("\nFinal Program Result:", final_result)

    except (SyntaxError, NameError, TypeError, ZeroDivisionError, NotImplementedError, ValueError, RuntimeError, IndexError) as e:
        print(f"Error: {e}")
        e.print_exc()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        e.print_exc()

    # ast.print()

    # if show_ast_only:
    #     ast.print()

    # else:
    #     print("Output of the above program is:")
    #     # You’ll later replace this with CSE execution
    #     print("<placeholder>")


if __name__ == "__main__":
    main()
