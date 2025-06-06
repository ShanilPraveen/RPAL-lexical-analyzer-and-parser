from abc import ABC, abstractmethod

class Node(ABC):
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
    
class STLambdaNode(Node):
    def __init__(self, Vb, Exp):
        super().__init__('E', 'lambda')
        self.Vb = Vb
        self.E = Exp
    
    def standardize(self):
        return self
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.Vb.print(indent + 1)
        self.E.print(indent + 1)


class IdentifierNode(Node):
    def __init__(self, name):
        super().__init__('Identifier', name)
    
    def standardize(self):
        return self  # Return the node itself, as IdentifierNode is already standardized
    
    def __str__(self):
        return f"Identifier({self.value})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}<ID:{self.value}>')


class LambdaNode(Node):
    def __init__(self, Vbs, Exp):
        super().__init__('E', 'lambda')
        self.Vb_list = Vbs
        self.E = Exp
    
    def standardize(self):
        stVbs = [vb.standardize() for vb in self.Vb_list]
        stE = self.E.standardize()
        for i in range(len(stVbs)-1, -1, -1):
            node = STLambdaNode(stVbs[i], stE)
            stE = node
        return stE  # Return the standardized lambda node
    
    def __str__(self):
        return f"Lambda({self.Vb_list}, {self.E})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        for vb in self.Vb_list:
            vb.print(indent + 1)
        self.E.print(indent + 1)


class GammaNode(Node):
    def __init__(self, N, E):
        super().__init__('gamma', 'gamma')
        self.N = N
        self.E = E
    
    def standardize(self):
        stN = self.N.standardize()
        stE = self.E.standardize()
        return GammaNode(stN, stE) 
    
    def __str__(self):
        return f"Gamma({self.N}, {self.E})"

    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.N.print(indent + 1)
        self.E.print(indent + 1)    


class RnNode(Node):
    def __init__(self, randType, rand):
        super().__init__(randType, rand)
    
    def standardize(self):
        return self # Return the node itself, as Rn is already standardized
    
    def __str__(self):
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

    
class LetNode(Node):
    def __init__(self, Def, Exp):
        super().__init__('E', 'let')
        self.D = Def
        self.E = Exp
    
    def standardize(self):
        stD = self.D.standardize()
        stE = self.E.standardize()
        if isinstance(stD, AssignmentNode):
            lambdaNode = STLambdaNode(stD.v1, stE)
            return GammaNode(lambdaNode, stD.e)
        else:
            raise ValueError("Invalid definition in LetNode")
        
    def __str__(self):
        return f"Let({self.D}, {self.E})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.D.print(indent + 1)
        self.E.print(indent + 1)


class CommaNode(Node):
    def __init__(self, params):
        super().__init__('comma', ',')
        self.params = params
    
    def standardize(self):
        stParams = [param.standardize() for param in self.params]
        return CommaNode(stParams)  # Return a new CommaNode with standardized parameters
    
    def __str__(self):
        return f"Comma({self.params})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        for param in self.params:
            param.print(indent + 1)


class AssignmentNode(Node):
    def __init__(self, v1, Exp):
        super().__init__('assignment', '=')
        self.v1 = v1
        self.e = Exp
    
    def standardize(self):
        stV1 = self.v1.standardize()
        stE = self.e.standardize()
        return AssignmentNode(stV1, stE)  # Return a new AssignmentNode with standardized components
    
    def __str__(self):
        return f"Assignment({self.v1}, {self.e})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.v1.print(indent + 1)
        self.e.print(indent + 1)


class FcnFormNode(Node):
    def __init__(self, name, Vbs, Exp):
        super().__init__('function_form', 'fcn_form')
        self.name = name
        self.Vbs = Vbs
        self.E = Exp
    
    def standardize(self):
        stVbs = [vb.standardize() for vb in self.Vbs]
        stE = self.E.standardize()
        for i in range(len(stVbs)-1, -1, -1):
            node = STLambdaNode(stVbs[i], stE)
            stE = node
        return AssignmentNode(self.name, stE)  # Return an AssignmentNode with the function name and standardized expression
    
    def __str__(self):
        return f"FcnForm({self.Vbs}, {self.E})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.name.print(indent + 1)
        for vb in self.Vbs:
            vb.print(indent + 1)
        self.E.print(indent + 1)


class RecNode(Node):
    def __init__(self, Db):
        super().__init__('rec', 'rec')
        self.Db = Db
    
    def standardize(self):
        stDb = self.Db.standardize()
        if isinstance(stDb, AssignmentNode):
            lambdaNode = STLambdaNode(stDb.v1, stDb.e)
            gammaNode = GammaNode(IdentifierNode('Y*'), lambdaNode)
            return AssignmentNode(stDb.v1, gammaNode)  # Return an AssignmentNode for the recursive definition
        else:
            raise ValueError("Invalid definition in RecNode")
    
    def __str__(self):
        return f"Rec({self.Db})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.Db.print(indent + 1)


class AndNode(Node):
    def __init__(self, Drs):
        super().__init__('and', 'and')
        self.Drs = Drs

    def standardize(self):
        stDrs = [dr.standardize() for dr in self.Drs]
        params = []
        elements = []

        for dr in stDrs:
            if not isinstance(dr, AssignmentNode):
                raise ValueError("Invalid Node in AndNode. Expected an AssignmentNode.")
            params.append(dr.v1)
            elements.append(dr.e)
        
        comma = CommaNode(params)
        tuple = TauNode(elements)
        return AssignmentNode(comma, tuple)  # Return an AssignmentNode with a CommaNode and TauNode
    
    def __str__(self):
        return f"And({self.Drs})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        for dr in self.Drs:
            dr.print(indent + 1)


class WithinNode(Node):
    def __init__(self, Da, D):
        super().__init__('within', 'within')
        self.Da = Da
        self.D = D

    def standardize(self):
        stDa = self.Da.standardize()
        stD = self.D.standardize()
        if not isinstance(stDa, AssignmentNode) or not isinstance(stD, AssignmentNode):
            raise ValueError("Invalid Node in WithinNode. Expected AssignmentNodes.")
        
        lambdaNode = STLambdaNode(stDa.v1, stD.e)
        gammaNode = GammaNode(lambdaNode, stDa.e)
        return AssignmentNode(stD.v1, gammaNode)  # Return an AssignmentNode for the within definition

    def __str__(self):
        return f"Within({self.Da}, {self.D})"

    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.Da.print(indent + 1)
        self.D.print(indent + 1)   


class WhereNode(Node):
    def __init__(self, T, Dr):
        super().__init__('Ew', 'where')
        self.T = T
        self.Dr = Dr
    
    def standardize(self):
        stT = self.T.standardize()
        stDr = self.Dr.standardize()
        if not isinstance(stDr, AssignmentNode):
            raise ValueError("Invalid Node in WhereNode. Expected an AssignmentNode.")
        
        lambdaNode = STLambdaNode(stDr.v1, stT)
        return GammaNode(lambdaNode, stDr.e)  # Return a GammaNode with the standardized lambda and expression
    
    def __str__(self):
        return f"Where({self.T}, {self.Dr})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.T.print(indent + 1)
        self.Dr.print(indent + 1)


class TauNode(Node):
    def __init__(self, elements):
        super().__init__('tau', 'tau')
        self.elements = elements

    def standardize(self):
        stElements = [element.standardize() for element in self.elements]
        return TauNode(stElements)  # Return a new TauNode with standardized elements
    
    def __str__(self):
        return f"Tau({self.elements})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        for element in self.elements:
            element.print(indent + 1)


class AugNode(Node):
    def __init__(self, Ta, Tc):
        super().__init__('aug', 'aug')
        self.Ta = Ta
        self.Tc = Tc
    
    def standardize(self):
        stTa = self.Ta.standardize()
        stTc = self.Tc.standardize()
        return AugNode(stTa, stTc)  # Return a new AugNode with standardized Ta and Tc

    def __str__(self):
        return f"Aug({self.Ta}, {self.Tc})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.Ta.print(indent + 1)
        self.Tc.print(indent + 1)


class ArrowNode(Node):
    def __init__(self, condition, ifCase, elseCase):
        super().__init__('arrow', '->')
        self.condition = condition
        self.ifCase = ifCase
        self.elseCase = elseCase

    def standardize(self):
        stCondition = self.condition.standardize()
        stIfCase = self.ifCase.standardize()
        stElseCase = self.elseCase.standardize()
        return ArrowNode(stCondition, stIfCase, stElseCase)  # Return a new ArrowNode with standardized components
    
    def __str__(self):
        return f"Arrow({self.condition}, {self.ifCase}, {self.elseCase})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.condition.print(indent + 1)
        self.ifCase.print(indent + 1)
        self.elseCase.print(indent + 1)


class NotNode(Node):
    def __init__(self, Bp):
        super().__init__('not', 'not')
        self.Bp = Bp
    
    def standardize(self):
        stBp = self.Bp.standardize()
        return NotNode(stBp)  # Return a new NotNode with standardized Bp

    def __str__(self):
        return f"Not({self.Bp})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.Bp.print(indent + 1)
    

class BAndOrNode(Node):
    def __init__(self, B1, B2, operator):
        super().__init__('Boolean', operator)
        self.B1 = B1
        self.B2 = B2
    
    def standardize(self):
        stB1 = self.B1.standardize()
        stB2 = self.B2.standardize()
        return BAndOrNode(stB1, stB2, self.value)  # Return a new BAndOrNode with standardized B1 and B2
    
    def __str__(self):
        return f"{self.value}({self.B1}, {self.B2})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.B1.print(indent + 1)
        self.B2.print(indent + 1)


class ConditionNode(Node):
    def __init__(self, a1, a2, condition):
        super().__init__('condition', condition)
        self.a1 = a1
        self.a2 = a2

    def standardize(self):
        stA1 = self.a1.standardize()
        stA2 = self.a2.standardize()
        return ConditionNode(stA1, stA2, self.value)
    
    def __str__(self):
        return f"{self.value}({self.a1}, {self.a2})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.a1.print(indent + 1)
        self.a2.print(indent + 1)


class ArithmeticNode(Node):
    def __init__(self, operator, a1, a2):
        super().__init__('arithmetic', operator)
        self.a1 = a1
        self.a2 = a2

    def standardize(self):
        stA1 = self.a1.standardize()
        stA2 = self.a2.standardize()
        return ArithmeticNode(self.value, stA1, stA2)  # Return a new ArithmeticNode with standardized a1 and a2
        
    def __str__(self):
        return f"{self.value}({self.a1}, {self.a2})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.a1.print(indent + 1)
        self.a2.print(indent + 1)


class NegNode(Node):
    def __init__(self, a):
        super().__init__('neg', 'neg')
        self.a = a
    
    def standardize(self):
        stA = self.a.standardize()
        return NegNode(stA)  # Return a new NegNode with standardized a
    
    def __str__(self):
        return f"Neg({self.a})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.a.print(indent + 1)


class AtNode(Node):
    def __init__(self, a1, Id, a2):
        super().__init__('at', '@')
        self.a1 = a1
        self.Id = IdentifierNode(Id)
        self.a2 = a2
    
    def standardize(self):
        stA1 = self.a1.standardize()
        stA2 = self.a2.standardize()
        tempGamma = GammaNode(self.Id, stA1)
        return GammaNode(tempGamma, stA2)
    
    def __str__(self):
        return f"@({self.a1}, {self.Id}, {self.a2})"
    
    def print(self, indent=0):
        print(f'{self.indentationSymbol * indent}{self.value}')
        self.a1.print(indent + 1)
        self.Id.print(indent + 1)
        self.a2.print(indent + 1)