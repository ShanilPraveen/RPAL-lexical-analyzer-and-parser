from tree import TreeNode, build_tree

def test_single_node():
    node = build_tree("root")
    assert node.value == "root"
    assert node.children == []

def test_nested_tree():
    node = build_tree("add", [
        build_tree("x"),
        build_tree("5")
    ])
    assert node.value == "add"
    assert len(node.children) == 2
    assert node.children[0].value == "x"
    assert node.children[1].value == "5"
