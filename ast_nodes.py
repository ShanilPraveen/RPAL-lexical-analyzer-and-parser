from abc import ABC, abstractmethod

__all__ = [
    'ASTNode', 
    'LambdaNode', 
    'LetNode',
    ]

class ASTNode(ABC):
    indentationSymbol = '.'

    def __init__(self, type_, value):
        super().__init__()
        self.type = type_
        self.value = value

    @abstractmethod
    def standardize(self):
        # This method should be implemented by subclasses to standardize the node
        pass

    @abstractmethod
    def print(self, indent=0):
        # This method should be implemented by subclasses to print the node
        pass
        
    def __str__(self):
        return f"{self.type} Node with value: {self.value}"

    def __repr__(self):
        return self.__str__()

    
class LambdaNode(ASTNode):
    def __init__(self, Vbs, Exp):
        super().__init__('E', 'lambda')
        self.Vb_list = Vbs
        self.E = Exp
    
    def standardize(self):
        # Standardize logic goes here
        return f"Lambda({self.Vb_list}, {self.E})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        for vb in self.Vb_list:
            vb.print(indent + 1)
        self.E.print(indent + 1)
    
class GammaNode(ASTNode):
    def __init__(self, N, E):
        super().__init__('gamma', 'gamma')
        self.N = N
        self.E = E
    
    def standardize(self):
        # Standardize logic goes here
        return f"Gamma({self.N}, {self.E})"

    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.N.print(indent + 1)
        self.E.print(indent + 1)    


class RnNode(ASTNode):
    def __init__(self, randType, rand):
        super().__init__(randType, rand)
    
    def standardize(self):
        # Standardize logic goes here
        return f"Rn({self.type}, {self.value})"
    
    def print(self, indent=0):
        tag = ""
        match self.type:
            case 'integer':
                tag = f"<INT:{self.value}>"
            case 'string':
                tag = f"<STR:{self.value}>"
            case 'identifier':
                tag = f"<ID:{self.value}>"
            case _:
                tag = f"<{self.value}>"
        print(f'{self.indentationSymbol * indent}{tag}')

    
class LetNode(ASTNode):
    def __init__(self, Def, Exp):
        super().__init__('E', 'let')
        self.D = Def
        self.E = Exp
    
    def standardize(self):
        # Standardize logic goes here
        return f"Let({self.D}, {self.E})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.D.print(indent + 1)
        self.E.print(indent + 1)
    
class CommaNode(ASTNode):
    def __init__(self, params):
        super().__init__('comma', ',')
        self.params = params
    
    def standardize(self):
        # Standardize logic goes here
        return f"Comma({self.params})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        for param in self.params:
            param.print(indent + 1)
    
class VbNode(ASTNode):
    def __init__(self, name):
        super().__init__('Vb', name)
    
    def standardize(self):
        # Standardize logic goes here
        return f"Vb({self.value})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}<ID:{self.value}>')
    
class AssignmentNode(ASTNode):
    def __init__(self, v1, Exp):
        super().__init__('assignment', '=')
        self.v1 = v1
        self.e = Exp
    
    def standardize(self):
        # Standardize logic goes here
        return f"Assignment({self.v1}, {self.e})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.v1.print(indent + 1)
        self.e.print(indent + 1)
    
class FcnFormNode(ASTNode):
    def __init__(self, name, Vbs, Exp):
        super().__init__('fcn_form', 'function')
        self.name = name
        self.Vbs = Vbs
        self.E = Exp
    
    def standardize(self):
        # Standardize logic goes here
        return f"FcnForm({self.Vbs}, {self.E})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        print(f'{self.indentationSymbol * (indent+1)}<ID:{self.name}>')
        for vb in self.Vbs:
            vb.print(indent + 1)
        self.E.print(indent + 1)
    
class RecNode(ASTNode):
    def __init__(self, Db):
        super().__init__('rec', 'rec')
        self.Db = Db
    
    def standardize(self):
        # Standardize logic goes here
        return f"Rec({self.Db})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.Db.print(indent + 1)
    
class AndNode(ASTNode):
    def __init__(self, Drs):
        super().__init__('and', 'and')
        self.Drs = Drs

    def standardize(self):
        # Standardize logic goes here
        return f"And({self.Drs})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        for dr in self.Drs:
            dr.print(indent + 1)

class WithinNode(ASTNode):
    def __init__(self, Da, D):
        super().__init__('within', 'within')
        self.Da = Da
        self.D = D

    def standardize(self):
        # Standardize logic goes here
        return f"Within({self.Da}, {self.D})"

    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.Da.print(indent + 1)
        self.D.print(indent + 1)   
    
class WhereNode(ASTNode):
    def __init__(self, T, Dr):
        super().__init__('Ew', 'where')
        self.T = T
        self.Dr = Dr
    
    def standardize(self):
        # Standardize logic goes here
        return f"Where({self.T}, {self.Dr})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.T.print(indent + 1)
        self.Dr.print(indent + 1)
    
class TauNode(ASTNode):
    def __init__(self, elements):
        super().__init__('tau', 'tau')
        self.elements = elements

    def standardize(self):
        # Standardize logic goes here
        return f"Tau({self.elements})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        for element in self.elements:
            element.print(indent + 1)
    
class AugNode(ASTNode):
    def __init__(self, Ta, Tc):
        super().__init__('aug', 'aug')
        self.Ta = Ta
        self.Tc = Tc
    
    def standardize(self):
        # Standardize logic goes here
        return f"Aug({self.Ta}, {self.Tc})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.Ta.print(indent + 1)
        self.Tc.print(indent + 1)
    
class ArrowNode(ASTNode):
    def __init__(self, condition, ifCase, elseCase):
        super().__init__('arrow', '->')
        self.condition = condition
        self.ifCase = ifCase
        self.elseCase = elseCase

    def standardize(self):
        # Standardize logic goes here
        return f"Arrow({self.condition}, {self.ifCase}, {self.elseCase})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.condition.print(indent + 1)
        self.ifCase.print(indent + 1)
        self.elseCase.print(indent + 1)
    
class NotNode(ASTNode):
    def __init__(self, Bp):
        super().__init__('not', 'not')
        self.Bp = Bp
    
    def standardize(self):
        # Standardize logic goes here
        return f"Not({self.Bp})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.Bp.print(indent + 1)
    
class BAndOrNode(ASTNode):
    def __init__(self, B1, B2, operator):
        super().__init__('Boolean', operator)
        self.B1 = B1
        self.B2 = B2
    
    def standardize(self):
        # Standardize logic goes here
        return f"{self.value}({self.B1}, {self.B2})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.B1.print(indent + 1)
        self.B2.print(indent + 1)
    
class ConditionNode(ASTNode):
    def __init__(self, a1, a2, condition):
        super().__init__('condition', condition)
        self.a1 = a1
        self.a2 = a2

    def standardize(self):
        # Standardize logic goes here
        return f"{self.value}({self.a1}, {self.a2})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.a1.print(indent + 1)
        self.a2.print(indent + 1)
    
class ArithmeticNode(ASTNode):
    def __init__(self, operator, a1, a2):
        super().__init__('arithmetic', operator)
        self.a1 = a1
        self.a2 = a2

    def standardize(self):
        # Standardize logic goes here
        return f"{self.value}({self.a1}, {self.a2})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.a1.print(indent + 1)
        self.a2.print(indent + 1)
    
class NegNode(ASTNode):
    def __init__(self, a):
        super().__init__('neg', 'neg')
        self.a = a
    
    def standardize(self):
        # Standardize logic goes here
        return f"Neg({self.a})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.a.print(indent + 1)
    
class AtNode(ASTNode):
    def __init__(self, a1, Id, a2):
        super().__init__('at', '@')
        self.a1 = a1
        self.Id = Id
        self.a2 = a2
    
    def standardize(self):
        # Standardize logic goes here
        return f"@({self.a1}, {self.Id}, {self.a2})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.a1.print(indent + 1)
        print(f'{self.indentationSymbol * (indent + 1)}<ID:{self.Id}>')
        self.a2.print(indent + 1)