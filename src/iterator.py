from node import CompositeNode

class TreeIterator:
    def __init__(self, root):
        self.stack = [(root, 0, False)]  # Node, level, is_last_child

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration

        node, level, is_last_child = self.stack.pop()
        if isinstance(node, CompositeNode):
            for i, child in enumerate(reversed(node.children)):
                self.stack.append((child, level + 1, i == 0))

        return node, level, is_last_child
