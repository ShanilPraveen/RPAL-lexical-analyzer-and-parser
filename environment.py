from data_types import Tuple, TruthValue, Nil

class Environment:

    builtInFunctions = [
        ("Print", 1),
        ("Isinteger", 1),
        ("Istruthvalue", 1),
        ("Isstring", 1),
        ("Istuple", 1),
        ("Isfunction", 1),
        ("Isdummy", 1),
        ("Stem", 1),
        ("Stern", 1),
        ("Conc", 2),
        ("Order", 1),
        ("Null", 1),
        ("Y*", 1)
    ]

    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def define(self, name, value):
        """Define a new variable in the current environment."""
        self.bindings[name] = value

    def defineBuiltInFunctions(self):
        """Define all built-in functions in the current environment."""
        for name, arity in self.builtInFunctions:
            self.define(name, BuiltInFunction(name, arity))

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
    def __init__(self, name, arity=1, args_received=None):
        self.name = name
        self.arity = arity
        self.args_received = args_received if args_received is not None else []

    def execute(self, arg_value):
        # Implement the logic for each built-in function here
        current_args = self.args_received + [arg_value]
        if len(current_args) < self.arity:
            return BuiltInFunction(self.name, self.arity, current_args)
        else:
            if self.name == "Print":
                # print("Executing Print built-in function with argument:")
                print(current_args[0])
                return "dummy"
            
            elif self.name == "Isinteger":
                if type(current_args[0]) == int:
                    return TruthValue(True)
                else:
                    return TruthValue(False)
                
            elif self.name == "Istruthvalue":
                if isinstance(current_args[0], TruthValue):
                    return TruthValue(True)
                else:
                    return TruthValue(False)
                
            elif self.name == "Isstring":
                if type(current_args[0]) == str:
                    return TruthValue(True)
                else:
                    return TruthValue(False)
                
            elif self.name == "Istuple":
                if isinstance(current_args[0], Tuple):
                    return TruthValue(True)
                else:
                    return TruthValue(False)
            
            elif self.name == "Isfunction":
                if isinstance(current_args[0], BuiltInFunction) or isinstance(current_args[0], Closure):
                    return TruthValue(True)
                else:
                    return TruthValue(False)
                
            elif self.name == "Isdummy":
                if current_args[0] == "dummy":
                    return TruthValue(True)
                else:
                    return TruthValue(False)
                
            elif self.name == "Stem":
                if type(current_args[0]) == str:
                    if len(current_args[0]) == 0:
                        raise ValueError("Stem built-in function expects a non-empty string argument.")
                    return current_args[0][0]
                else:
                    raise TypeError("Stem built-in function expects a string argument.")
            
            elif self.name == "Stern":
                if type(current_args[0]) == str:
                    if len(current_args[0]) == 0:
                        raise ValueError("Stern built-in function expects a non-empty string argument.")
                    return current_args[0][1:]
                else:
                    raise TypeError("Stern built-in function expects a string argument.")
                
            elif self.name == "Conc":
                if len(current_args) != 2:
                    raise TypeError("Conc function expects exactly two string arguments.")
                
                str1 = current_args[0]
                str2 = current_args[1]
                
                if not isinstance(str1, str) or not isinstance(str2, str):
                    raise TypeError("Conc function expects two string arguments.")
                
                return str1 + str2
            
            elif self.name == "Order":
                if isinstance(current_args[0],Tuple):
                    return len(current_args[0])
                else:
                    raise TypeError("Order built-in function expects a tuple argument.")
                
            elif self.name == "Null":
                if isinstance(current_args[0],tuple) and len(current_args[0]) == 0:
                    return TruthValue(True)
                else:   
                    return TruthValue(False)

            elif self.name == 'Y*':
                from nodes import IdentifierNode # Local import to resolve circular dependency
                if len(current_args) != 1:
                    raise TypeError("Y* combinator expects exactly one argument.")
                
                if not isinstance(current_args[0], Closure):
                    raise TypeError("Y* combinator expects a function (closure) as its argument.")
                
                rec_lambda_node = current_args[0].lambdaNode 
                
                if not isinstance(rec_lambda_node.Vb, IdentifierNode):
                    raise TypeError("Recursive function name for Y* must be a single identifier.")
                
                func_name = rec_lambda_node.Vb.value
                actual_function_body_node = rec_lambda_node.E

                rec_def_env = current_args[0].env

                recursive_call_env = Environment(parent=rec_def_env)
                recursive_call_env.define(func_name, None)
                
                actual_recursive_closure = Closure(actual_function_body_node, recursive_call_env)
                recursive_call_env.define(func_name, actual_recursive_closure)
                return actual_recursive_closure
            
            else:
                raise NotImplementedError(f"Built-in function '{self.name}' not yet implemented.")


    def __call__(self, *args):
        """Call the built-in function with the provided arguments."""
        return self.func(*args)

    def __str__(self):
        return f"BuiltInFunction(name={self.name})"

    def __repr__(self):
        return self.__str__()
     
