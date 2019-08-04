class Node:
    def __init__(self, node, p_node):
        self.node = node
        self.parent = p_node
        self.leaves = []


class Tree:
    def __init__(self, root, p_node):
        self.__root = Node(root, p_node)
        self.__car_node = self.__root

    def append_node(self, node):
        t_car = Node(node, self.__car_node)
        self.__car_node.leaves.append(t_car)
        self.__car_node = t_car

    def set_parent(self):
        self.__car_node = self.__car_node.parent

    def print_tree(self):
        if self.__root:
            self._print_tree(self.__root, 0)

    def _print_tree(self, root, h):
        depth = "     ¦" * (h-1)
        if h != 0:
            depth += "     └─── "
        if isinstance(root.node, str):
            print("%s%s" % (depth, root.node))
        else:
            print("%s%s" % (depth, root.node[0]))
        for leaf in root.leaves:
            self._print_tree(leaf, h+1)

    def get_root(self):
        return self.__root