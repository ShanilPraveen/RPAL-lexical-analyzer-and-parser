from .tree import build_tree
from .Lexer import Token
from .ast_nodes import (LetNode, LambdaNode, RnNode, FcnFormNode, RecNode,
GammaNode, CommaNode, VbNode, AssignmentNode, AndNode, WithinNode, WhereNode,
TauNode, AugNode, ArrowNode, NotNode, BAndOrNode, ConditionNode, ArithmeticNode,
NegNode, AtNode)


class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def match(self, expected):
        token = self.peek()
        if token and (token.type == expected or token.value == expected):
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

    def expect(self, expected):
        token = self.match(expected)
        if token is None:
            raise SyntaxError(f"Expected {expected} but found {self.peek()}")
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
                next_token = self.peek()
                if next_token and next_token.value == '.':
                    break
                if not next_token:
                    raise SyntaxError("Expected '.' after fn arguments")

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
            return WhereNode(t,dr)

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


    def parse_T(self):
        ta_list = [self.parse_Ta()]

        while True:
            token = self.peek()
            if token and token.value == ",":
                self.match(',')
                ta = self.parse_Ta()
                ta_list.append(ta)

            else:
                break

        if len(ta_list) == 1:
            return ta_list[0]
        else:
            return TauNode(ta_list)

    def parse_Ta(self):
        node = self.parse_Tc()

        while True:
            token = self.peek()
            if token and token.value == 'aug':
                self.match('aug')
                right = self.parse_Tc()
                node = AugNode(node, right)
            else:
                break

        return node

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
        params.append(self.match('identifier')) 
        while self.peek() and self.peek().type == 'delimiter' and self.peek().value == ',':
            self.expect('delimiter')
            params.append(self.match('identifier'))
        
        if len(params)==0:
            raise SyntaxError("Expected at least one identifier in paranthesis")
        elif len(params) == 1:
            return VbNode(params[0].value)
        else:
            return CommaNode(params)

    def parse_Tc(self):
        b = self.parse_B()
        token = self.peek()
        if token and token.value == '->':
            self.match('->')
            tc1 = self.parse_Tc()
            self.expect('|')
            tc2 = self.parse_Tc()
            return ArrowNode(b, tc1, tc2)

        return b

    def parse_B(self):
        node = self.parse_Bt()
        while True :
            if self.peek() and self.peek().value == 'or':
                self.match('or')
                next_bt = self.parse_Bt()
                node = BAndOrNode(node,next_bt, 'or')
            else:
                break


        return node

    def parse_Bt(self):
        node = self.parse_Bs()
        while True:
            if self.peek() and self.peek().value == '&':
                self.match('&')
                next_bs = self.parse_Bs()
                node = BAndOrNode(node, next_bs, '&')
            else:
                break
        return node
            
    
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
                        self.expect('=')
                        e = self.parse_E()
                        return FcnFormNode(identifier.value, Vbs, e)
                else:
                    raise SyntaxError("Unexpected end of input while parsing DbNode")
            elif token.type == 'delimiter' and token.value == '(':
                self.match('(')
                d = self.parse_D()
                self.expect(')')
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


    def parse_Bs(self):
        token = self.peek()
        if token and token.value == 'not':
            self.match('not')
            bp = self.parse_Bp()
            return NotNode(bp)

        return self.parse_Bp()

    def parse_Bp(self):
        a1 = self.parse_A()
        token = self.peek()

        if token and token.value in ('gr', '>'):
            self.match(token.value)
            a2 = self.parse_A()
            return ConditionNode(a1, a2, '>')

        elif token and token.value in ('ge', '>='):
            self.match(token.value)
            a2 = self.parse_A()
            return ConditionNode(a1, a2, '>=')

        elif token and token.value in ('ls', '<'):
            self.match(token.value)
            a2 = self.parse_A()
            return ConditionNode(a1, a2, '<')

        elif token and token.value in ('le', '<='):
            self.match(token.value)
            a2 = self.parse_A()
            return ConditionNode(a1, a2, '<=')

        elif token and token.value == 'eq':
            self.match('eq')
            a2 = self.parse_A()
            return ConditionNode(a1, a2, 'eq')

        elif token and token.value == 'ne':
            self.match('ne')
            a2 = self.parse_A()
            return ConditionNode(a1, a2, 'ne')

        return a1

    def parse_A(self):
        token = self.peek()

        if token and token.value == '+':
            self.match('+')
            at = self.parse_At()
            return ArithmeticNode('+', 0 , at)

        elif token and token.value == '-':
            self.match('-')
            at = self.parse_At()
            return NegNode(at)

        node = self.parse_At()
        while True:
            token = self.peek()
            if token and token.value == '+':
                self.match('+')
                right = self.parse_At()
                node = ArithmeticNode('+', node, right)
            elif token and token.value == '-':
                self.match('-')
                right = self.parse_At()
                node = ArithmeticNode('-', node, right)
            else:
                break
        return node

    def parse_At(self):
        node = self.parse_Af()
        while True:
            token = self.peek()
            if token and token.value == '*':
                self.match('*')
                right = self.parse_Af()
                node = ArithmeticNode('*', node, right)
            elif token and token.value == '/':
                self.match('/')
                right = self.parse_Af()
                node = ArithmeticNode('/', node, right)
            else:
                break
        return node

    def parse_Af(self):
        node = self.parse_Ap()
        while True:
            token = self.peek()
            if token and token.value == '**':
                self.match('**')
                right = self.parse_Ap()
                node = ArithmeticNode('**', node, right)
            else:
                break
        return node

    def parse_Ap(self):
        node = self.parse_R()

        while True:
            token = self.peek()
            if token and token.value == '@':
                self.match('@')

                id_token = self.match('identifier')
                if not id_token:
                    raise SyntaxError("Expected identifier after '@'")

                r = self.parse_R()

                node = AtNode(node, id_token.value, r)

            else:
                break

        return node
