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

    
class LetNode(ASTNode):
    def __init__(self, Def, Exp):
        super().__init__('E', 'let')
        self.D = Def
        self.E = Exp
    
    def standardize(self):
        # Standardixe logic goes here
        return f"Let({self.D}, {self.E})"