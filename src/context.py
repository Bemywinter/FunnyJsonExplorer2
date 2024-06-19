from iterator import TreeIterator
from strategy import VisualizerStrategy

class VisualizerContext:
    def __init__(self, strategy: VisualizerStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: VisualizerStrategy):
        self._strategy = strategy

    def visualize(self, node):
        iterator = TreeIterator(node)
        result = ""
        for node, level, is_last_child in iterator:
            result += self._strategy.visualize(node, level, is_last_child)
        return self._strategy.beautify(result)
