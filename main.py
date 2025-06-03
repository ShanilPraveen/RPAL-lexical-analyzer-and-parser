import sys
from .Lexer import Lexer
from .parser import Parser

def read_file(filename):
    with open(filename,'r') as f:
        return f.read()


def main():
    # if len(sys.argv) < 2 :
    #     print("Usage: python myrpal.py <filename> [-ast]")
    #     return

    # filename = sys.argv[1]
    # show_ast_only = "-ast" in sys.argv

    code = """let rec f(a)= a eq 1 -> 1 
		      | a le 0 -> 0
		      | f(a-1) + f(a-2) in Print( f(2))
"""

    lexer = Lexer(code)
    lexer.tokenize()
    print("Tokens: "+str(lexer.tokens))

    parser = Parser(lexer.tokens)
    ast = parser.parse_E()
    ast.standardize().print()

    # if show_ast_only:
    #     ast.print()

    # else:
    #     print("Output of the above program is:")
    #     # You’ll later replace this with CSE execution
    #     print("<placeholder>")


if __name__ == "__main__":
    main()
