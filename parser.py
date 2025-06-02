from ast_nodes import LetNode, LambdaNode, WhereNode
from .tree import build_tree
from .Lexer import Token

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
            return LambdaNode(vb_list,e)


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
                node = OrNode(node,next_bt)
            else:
                break

        return node

    def parse_Bt(self):
        node = self.parse_Bs()
        while True:
            if self.peek() and self.peek().value == '&':
                self.match('&')
                next_bs = self.parse_Bs()
                node = AndNode(node, next_bs)
            else:
                break

        return node

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
            return GreaterThanNode(a1, a2)

        elif token and token.value in ('ge', '>='):
            self.match(token.value)
            a2 = self.parse_A()
            return GreaterThanOrEqualNode(a1, a2)

        elif token and token.value in ('ls', '<'):
            self.match(token.value)
            a2 = self.parse_A()
            return LessThanNode(a1, a2)

        elif token and token.value in ('le', '<='):
            self.match(token.value)
            a2 = self.parse_A()
            return LessThanOrEqualNode(a1, a2)

        elif token and token.value == 'eq':
            self.match('eq')
            a2 = self.parse_A()
            return EqualNode(a1, a2)

        elif token and token.value == 'ne':
            self.match('ne')
            a2 = self.parse_A()
            return NotEqualNode(a1, a2)

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
            return ArithmeticNode('neg', None, at)

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
                id_node = IDNode(id_token.value)

                node = ArithmeticNode('@', node, [id_node, r])

            else:
                break

        return node












