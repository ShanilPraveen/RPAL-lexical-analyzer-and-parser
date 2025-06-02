from .tree import build_tree
from .Lexer import Token
from .ast_nodes import (LetNode, LambdaNode, RnNode, FcnFormNode, RecNode,
GammaNode, CommaNode, VbNode, AssignmentNode, AndNode, WithinNode)

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
    
    def reversePos(self):
        if self.position > 0:
            self.position -= 1
        else:
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
            elif token.type == 'string':
                self.match('string')
                return RnNode('string', token.value)
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
        params.append(self.expect('identifier')) 
        while self.peek() and self.peek().type == 'delimiter' and self.peek().value == ',':
            self.match('delimiter')
            params.append(self.expect('identifier'))
        
        if len(params)==0:
            raise SyntaxError("Expected at least one identifier in paranthesis")
        elif len(params) == 1:
            return VbNode(params[0].value)
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
            
    
    def parse_Db(self):
        token = self.peek()
        if token:
            if token.type == 'identifier':
                identifier = self.match('identifier')
                next_token = self.peek()
                if next_token:
                    if(next_token.type == 'delimeter' and next_token.value == ','):
                        self.reversePos()
                        v1 = self.parse_V1()
                        self.expect('operator')
                        e = self.parse_E()
                        return AssignmentNode(v1, e)
                    else:
                        Vbs = []
                        while True:
                            vb = self.parse_Vb()
                            Vbs.append(vb)
                            if self.peek() and self.peek().value == '=':
                                break
                        if len(Vbs) == 0:
                            raise SyntaxError("Expected at least one variable binding")
                        self.expect('operator')
                        e = self.parse_E()
                        return FcnFormNode(identifier.value, Vbs, e)
                else:
                    raise SyntaxError("Unexpected end of input while parsing DbNode")
            elif token.type == 'delimiter' and token.value == '(':
                self.match('delimiter')
                d = self.parse_D()
                self.expect('delimiter')
                return d
            else:
                raise SyntaxError(f"Unexpected token: {token}")
        else:
            raise SyntaxError("Unexpected end of input while parsing DbNode")
        
    def parse_Dr(self):
        token = self.peek()
        if token:
            if token.type == 'rec':
                self.expect('rec')
                Db = self.parse_Db()
                return RecNode(Db)
            else:
                return self.parse_Db()
        else:
            raise SyntaxError("Unexpected end of input while parsing DrNode")
        
    def parse_Da(self):
        token = self.peek()
        if token:
            Drs = []
            while True:
                Dr = self.parse_Dr()
                Drs.append(Dr)
                if self.peek() and self.peek().value == 'and':
                    self.expect('and')
                else:
                    break
            if len(Drs) == 0:
                raise SyntaxError("Expected at least one declaration")
            elif len(Drs) == 1:
                return Drs[0]
            else:
                return AndNode(Drs)
        else:
            raise SyntaxError("Unexpected end of input while parsing DaNode")
        
    def parse_D(self):
        token = self.peek()
        if token:
            Da = self.parse_Da()
            if self.peek() and self.peek().value == 'within':
                self.expect('within')
                D = self.parse_D()
                return WithinNode(Da, D)
            else:
                return Da
        else:
            raise SyntaxError("Unexpected end of input while parsing DNode")