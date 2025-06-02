from .tree import build_tree
from .Lexer import Token
from .ast_nodes import (LetNode, LambdaNode)

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def match(self,expected_type):
        token = self.peek()
        if token and token.type == expected_type:
            self.position += 1
            return token
        return None


    def expect(self,expected_type):
        token = self.match(expected_type)
        if token is None:
            raise SyntaxError(f"Expected {expected_type} but found {self.peek()}")
        return token


    def parse_E(self):
        token = self.peek()

        if token and token.type == 'let':
            self.match('let')
            d = self.parse_D()
            self.expect('in')
            e = self.parse_E()
            return LetNode(d,e)

        elif token and token.type == 'fn':
            self.match('fn')
            vb_list = []

            while True:
                vb = self.parse_Vb()
                vb_list.append(vb)

                if self.peek() and self.peek().value == '.':
                    break

            self.expect('.')
            e = self.parse_E()

            for i in range(len(vb_list)-1, -1, -1):
                vb = vb_list[i]
                # Create a LambdaNode for each variable binding
                e = LambdaNode(vb, e)
            return e


        else:
            return self.parse_Ew()


    def parse_Ew(self):
        t = self.parse_T()

        token = self.peek()
        if token and token.type == "where":
            self.match("where")
            dr = self.parse_Dr()
            return build_tree("where",[t,dr])

        return t









