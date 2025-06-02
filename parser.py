from .tree import build_tree
from .Lexer import Token
from .ast_nodes import (LetNode, LambdaNode, RnNode, 
GammaNode, CommaNode, VbNode)

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
    
    def prevToken(self):
        if self.position > 0:
            return self.tokens[self.position - 1]
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
    
    def parse_Rn(self):
        token =self.peek()
        if token:
            if token.type == 'identifier':
                self.match('identifier')
                return RnNode('identifier', token.value)
            elif token.type == 'integer':
                self.match('integer')
                return RnNode('integer', token.value) #can pass int
            elif token.type == 'srting':
                self.match('srting')
                return RnNode('srting', token.value)
            elif token.type == 'true':
                self.match('true')
                return RnNode('true', token.value) #can pass True
            elif token.type == 'false':
                self.match('false')
                return RnNode('false', token.value) #can pass False 
            elif token.type == 'nil':
                self.match('nil')
                return RnNode('nil', token.value) #can pass None
            elif (token.type == 'delimiter' and token.value == '('):
                self.match('delimiter')
                e = self.parse_E()
                self.expect('delimiter')
                return e
            else:
                raise SyntaxError(f"Unexpected token: {token}")
        else:
            raise SyntaxError("Unexpected end of input while parsing RnNode")
        
    def parse_R(self):
        operands = []
        while True:
            try:
                Rn = self.parse_Rn()
                operands.append(Rn)
            except SyntaxError:
                # If we can't parse another Rn, break the loop
                break
        if not operands:
            raise SyntaxError("Expected at least one operand")
        elif len(operands) == 1:
            return operands[0]
        else:
            for i in range(len(operands)-1, -1, -1):
                Rn = operands[i]
                # Create a GammaNode for each operand
                node = GammaNode(node, Rn)
            return node
    
    def parse_V1(self):
        params = []
        token = self.peek()
        nextExpected = 'identifier'
        while (token and token.type==nextExpected):
            if(nextExpected == 'identifier'):
                params.append(self.match('identifier'))
                nextExpected = 'delimiter'
            elif(nextExpected == 'delimiter' and token.value == ','):
                self.match('delimiter')
                nextExpected = 'identifier'
            else:
                break
        
        if len(params)<2:
            raise SyntaxError("Expected at least two identifiers separated by commas")
        else:
            return CommaNode(params)

    def parse_Vb(self):
        token = self.peek()
        if token:
            if token.type == 'identifier':
                identifier = self.match('identifier')
                return VbNode(identifier.value)
            elif token.type == 'delimiter' and token.value == '(':
                self.match('delimiter')
                vb_list = self.parse_V1()
                self.expect('delimiter')
                return vb_list
            else:
                raise SyntaxError(f"Unexpected token: {token}")
            

    def parse_D(self):
        token = self.peek()
        return None
    
    # def parse_Db(self):
    #     token = self.peek()
    #     if token:
    #         if token.type == 'identifier':
    #             identifier = self.match('identifier')
    #             if
    #         elif token.type == 'delimiter' and token.value == '(':
    #             self.match('delimiter')
    #             vb_list = self.parse_V1()
    #             self.expect('delimiter')
    #             return vb_list
    #         else:
    #             raise SyntaxError(f"Unexpected token: {token}")
        