from abc import ABC, abstractmethod
from node import CompositeNode, LeafNode


class NodeBuilder(ABC):
    @abstractmethod
    def build(self, data, name="root"):
        pass


class CompositeNodeBuilder(NodeBuilder):
    def build(self, data, name="root"):
        if isinstance(data, dict):
            node = CompositeNode(name)
            for key, value in data.items():
                child = self.build(value, key)
                node.add(child)
            return node
        else:
            return LeafNode(name, data)


class TreeDirector:
    def __init__(self, builder):
        self._builder = builder

    def build_tree(self, data, name='root'):
        return self._builder.build(data, name)
