class Tuple:
    def __init__(self, elements=None):
        if elements is None:
            elements = []
        elif not isinstance(elements, list):
            raise TypeError("Elements passed to must be a list.")
        
        self.elements = elements

    def __str__(self):
        return f"({', '.join(str(e) for e in self.elements)})"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __iter__(self):
        return iter(self.elements)
    
    def add(self, other):
        if isinstance(other, (int, str, bool, Tuple, Nil, TruthValue)):
            return Tuple(self.elements + [other])
        else:
            raise TypeError(f"Cannot add {type(other).__name__} to Tuple.")
        
    def isEmpty(self):
        return len(self.elements) == 0
    

class TruthValue:
    def __init__(self, value):
        if not isinstance(value, bool):
            raise TypeError("TruthValue must be a boolean.")
        self.value = value

    def __str__(self):
        return "true" if self.value else "false"

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return self.value
    
class Nil:
    def __str__(self):
        return "nil"

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return False

    def isEmpty(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Nil)