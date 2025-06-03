from abc import ABC, abstractmethod

__all__ = [
    'ASTNode', 
    'LambdaNode', 
    'LetNode',
    ]

class ASTNode(ABC):
    def __init__(self, type_, value):
        super().__init__()
        self.type = type_
        self.value = value

    @abstractmethod
    def standardize(self):
        # This method should be implemented by subclasses to standardize the node
        pass
        
    def __str__(self):
        return f"{self.type} Node with value: {self.value}"

    def __repr__(self):
        return self.__str__()

    
class LambdaNode(ASTNode):
    def __init__(self, Vb, Exp):
        super().__init__('E', 'lambda')
        self.Vb = Vb
        self.E = Exp
    
    def standardize(self):
        # Standardize logic goes here
        return f"Lambda({self.Vb}, {self.E})"
    
class GammaNode(ASTNode):
    def __init__(self, N, E):
        super().__init__('gamma', 'gamma')
        self.N = N
        self.E = E
    
    def standardize(self):
        # Standardize logic goes here
        return f"Gamma({self.N}, {self.E})"

class RnNode(ASTNode):
    def __init__(self, randType, rand):
        super().__init__(randType, rand)
    
    def standardize(self):
        # Standardize logic goes here
        return f"Rn({self.type}, {self.value})"
    
class LetNode(ASTNode):
    def __init__(self, Def, Exp):
        super().__init__('E', 'let')
        self.D = Def
        self.E = Exp
    
    def standardize(self):
        # Standardize logic goes here
        return f"Let({self.D}, {self.E})"
    
class CommaNode(ASTNode):
    def __init__(self, params):
        super().__init__('comma', ',')
        self.params = params
    
    def standardize(self):
        # Standardize logic goes here
        return f"Comma({self.params})"
    
class VbNode(ASTNode):
    def __init__(self, name):
        super().__init__('Vb', name)
    
    def standardize(self):
        # Standardize logic goes here
        return f"Vb({self.value})"
    
class AssignmentNode(ASTNode):
    def __init__(self, v1, Exp):
        super().__init__('assignment', '=')
        self.v1 = v1
        self.e = Exp
    
    def standardize(self):
        # Standardize logic goes here
        return f"Assignment({self.v1}, {self.e})"
    
class FcnFormNode(ASTNode):
    def __init__(self, name, Vbs, Exp):
        super().__init__('fcn_form', 'function')
        self.name = name
        self.Vbs = Vbs
        self.E = Exp
    
    def standardize(self):
        # Standardize logic goes here
        return f"FcnForm({self.Vbs}, {self.E})"
    
class RecNode(ASTNode):
    def __init__(self, Db):
        super().__init__('rec', 'rec')
        self.Db = Db
    
    def standardize(self):
        # Standardize logic goes here
        return f"Rec({self.Db})"
    
class AndNode(ASTNode):
    def __init__(self, Drs):
        super().__init__('and', 'and')
        self.Drs = Drs

    def standardize(self):
        # Standardize logic goes here
        return f"And({self.Drs})"

class WithinNode(ASTNode):
    def __init__(self, Db, D):
        super().__init__('within', 'within')
        self.Db = Db
        self.D = D

    def standardize(self):
        # Standardize logic goes here
        return f"Within({self.Db}, {self.D})"    
    
class WhereNode(ASTNode):
    def __init__(self, T, Dr):
        super().__init__('Ew', 'where')
        self.T = T
        self.Dr = Dr
    
    def standardize(self):
        # Standardize logic goes here
        return f"Where({self.T}, {self.Dr})"
    
class TauNode(ASTNode):
    def __init__(self, elements):
        super().__init__('tau', 'tau')
        self.elements = elements

    def standardize(self):
        # Standardize logic goes here
        return f"Tau({self.elements})"
    
class AugNode(ASTNode):
    def __init__(self, Ta, Tc):
        super().__init__('aug', 'aug')
        self.Ta = Ta
        self.Tc = Tc
    
    def standardize(self):
        # Standardize logic goes here
        return f"Aug({self.Ta}, {self.Tc})"
    
class ArrowNode(ASTNode):
    def __init__(self, condition, ifCase, elseCase):
        super().__init__('arrow', '->')
        self.condition = condition
        self.ifCase = ifCase
        self.elseCase = elseCase

    def standardize(self):
        # Standardize logic goes here
        return f"Arrow({self.condition}, {self.ifCase}, {self.elseCase})"
    
class NotNode(ASTNode):
    def __init__(self, Bp):
        super().__init__('not', 'not')
        self.Bp = Bp
    
    def standardize(self):
        # Standardize logic goes here
        return f"Not({self.Bp})"
    
class BAndOrNode(ASTNode):
    def __init__(self, B1, B2, operator):
        super().__init__('Boolean', operator)
        self.B1 = B1
        self.B2 = B2
    
    def standardize(self):
        # Standardize logic goes here
        return f"{self.value}({self.B1}, {self.B2})"
    
class ConditionNode(ASTNode):
    def __init__(self, a1, a2, condition):
        super().__init__('condition', condition)
        self.a1 = a1
        self.a2 = a2

    def standardize(self):
        # Standardize logic goes here
        return f"{self.value}({self.a1}, {self.a2})"
    
class ArithmeticNode(ASTNode):
    def __init__(self, operator, a1, a2):
        super().__init__('arithmetic', operator)
        self.a1 = a1
        self.a2 = a2

    def standardize(self):
        # Standardize logic goes here
        return f"{self.value}({self.a1}, {self.a2})"
    
class NegNode(ASTNode):
    def __init__(self, a):
        super().__init__('neg', 'neg')
        self.a = a
    
    def standardize(self):
        # Standardize logic goes here
        return f"Neg({self.a})"
    
class AtNode(ASTNode):
    def __init__(self, a1, Id, a2):
        super().__init__('at', '@')
        self.a1 = a1
        self.Id = Id
        self.a2 = a2
    
    def standardize(self):
        # Standardize logic goes here
        return f"@({self.a1}, {self.Id}, {self.a2})"