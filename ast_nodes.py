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