import sys
from Lexer import Lexer
from parser import Parser
from environment import Environment, BuiltInFunction

def read_file(filename):
    with open(filename,'r') as f:
        return f.read()


def main():
    if len(sys.argv) < 2 :
        print("Usage: python myrpal.py [-ast] <filename>")
        return


    filename = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
    code = read_file(filename)
    flags = sys.argv
    


    lexer = Lexer(code)
    lexer.tokenize()
    # print("Tokens: "+str(lexer.tokens))

    parser = Parser(lexer.tokens)

    try:
        ast = parser.parse_E()

        if "-ast" in flags:
            ast.print()

        st = ast.standardize()

        if "-st" in flags:
            st.print()
        
        global_env = Environment()
        global_env.defineBuiltInFunctions()
            
        print("Output of the above program is:")
        final_result = st.interpret(global_env)
        print()
        #print("\nFinal Program Result:", final_result)


    except (SyntaxError, NameError, TypeError, ZeroDivisionError, NotImplementedError, ValueError, RuntimeError, IndexError) as e:
        print(f"Error: {e}")
        #e.print_exc()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        e.print_exc()


if __name__ == "__main__":
    main()
