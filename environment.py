class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def define(self, name, value):
        """Define a new variable in the current environment."""
        self.bindings[name] = value

    def lookup(self, name):
        """Look up a variable in the current environment or its parent."""
        if name in self.bindings:
            return self.bindings[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Identifier '{name}' is not defined.")
    
    def __str__(self):
        """String representation of the environment for debugging."""
        return f"Environment(bindings={self.bindings}, parent={self.parent})"
    
    def __repr__(self):
        return self.__str__()
    

class Closure:
    def __init__(self, lambdaNode, env):
        self.lambdaNode = lambdaNode
        self.env = env

    def __str__(self):
        param_str = self.lambdaNode.Vb.value if hasattr(self.lambdaNode.Vb, 'value') else str(self.lambdaNode.Vb)
        return f"Closure(param='{param_str}', body_node={self.lambdaNode.E}, defined_env={len(self.env.bindings)})"

    def __repr__(self):
        return self.__str__()
    
class BuiltInFunction:
    def __init__(self, name):
        self.name = name

    def execute(self, arg_value):
        # Implement the logic for each built-in function here
        if self.name == "Print":
            # print("Executing Print built-in function with argument:")
            print(arg_value)
            return "dummy"
        
        elif self.name == "Isinteger":
            if type(arg_value) == int:
                return True
            else:
                return False
            
        elif self.name == "Istruthvalue":
            if arg_value == True:
                return True
            
        elif self.name == "Isstring":
            if type(arg_value) == str:
                return True
            else:
                return False
            
        elif self.name == "Istuple":
            if isinstance(arg_value, tuple):
                return True
            else:
                return False
        
        elif self.name == "Isfunction":
            if isinstance(arg_value, BuiltInFunction) or isinstance(arg_value, Closure):
                return True
            else:
                return False
            
        elif self.name == "Isdummy":
            if arg_value == "dummy":
                return True
            else:
                return False
            
        elif self.name == 'Y*':
            raise NotImplementedError("Direct call to Y* built-in is not supported. It's used for recursion standardization.")
        
        raise NotImplementedError(f"Built-in function '{self.name}' not yet implemented.")

    def __call__(self, *args):
        """Call the built-in function with the provided arguments."""
        return self.func(*args)

    def __str__(self):
        return f"BuiltInFunction(name={self.name})"

    def __repr__(self):
        return self.__str__()
    
