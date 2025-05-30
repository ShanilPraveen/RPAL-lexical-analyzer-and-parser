class TreeNode:
    def __init__(self,value,children=None):
        self.value = value
        self.children = children or []

    def __str__(self,level=0):
        ret = '.' * level + self.value + '\n'
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return self.__str__()



def build_tree(value,children=None):
    return TreeNode(value,children or [])