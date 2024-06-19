from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def is_leaf(self):
        pass

class CompositeNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add(self, node):
        self.children.append(node)

    def is_leaf(self):
        return False

class LeafNode(Node):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    def is_leaf(self):
        return True
