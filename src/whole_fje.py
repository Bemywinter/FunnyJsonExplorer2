import argparse
import json
from abc import ABC, abstractmethod

# JSON file loading
class FjeExplorer:
    @staticmethod
    def load_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def load_icons(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Funny JSON Explorer (FJE)")
        parser.add_argument("-f", "--file", required=True, help="Path to the JSON file")
        parser.add_argument("-s", "--style", required=True, help="Visualization style")
        parser.add_argument("-i", "--icons", required=True, help="Icon family")
        return parser.parse_args()


# Iterator for tree traversal
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


# Strategy for visualization
class VisualizerStrategy(ABC):
    @abstractmethod
    def visualize(self, node, level=0, is_last_child=False):
        pass

    @abstractmethod
    def beautify(self, result):
        pass


# Concrete Strategies
class TreeVisualizer(VisualizerStrategy):
    def visualize(self, node, level=0, is_last_child=False):
        result = ""
        prefix = "└─" if is_last_child else "├─"
        indent = "  " * (level - 1) if level > 0 else ""
        if node.is_leaf():
            if node.value is None:
                result += f"{indent}{prefix}{icons['leaf']}{node.name}\n"
            else:
                result += f"{indent}{prefix}{icons['leaf']}{node.name}: {node.value}\n"
        else:
            if node.name != "root":
                result += f"{indent}{prefix}{icons['composite']}{node.name}\n"
        return result

    def beautify(self, result):
        lines = result.split('\n')
        last_root_index = 0
        for i in range(len(lines) - 1):
            last_non_whitespace_index = len(lines[i]) - len(lines[i].lstrip())
            if last_non_whitespace_index > 0:
                lines[i] = '│' + lines[i][1:]
            if lines[i][0] == '└':
                last_root_index = i
        for i in range(last_root_index + 1, len(lines) - 1):
            lines[i] = ' ' + lines[i][1:]
        return '\n'.join(lines)


class RectangleVisualizer(VisualizerStrategy):
    def visualize(self, node, level=0, is_last_child=False):
        result = ""
        prefix = "├─"
        indent = "│ " * (level - 1) if level > 0 else ""
        if node.is_leaf():
            if node.value is None:
                result += f"{indent}{prefix}{icons['leaf']}{node.name}\n"
            else:
                result += f"{indent}{prefix}{icons['leaf']}{node.name}: {node.value}\n"
        else:
            if node.name != "root":
                result += f"{indent}{prefix}{icons['composite']}{node.name}\n"
        return result

    def beautify(self, result):
        lines = result.split('\n')
        max_length = max(len(line) for line in lines)  # 获取最长的一行的长度
        for i in range(len(lines)):
            lines[i] = lines[i].ljust(max_length + 7, '─')  # 使用横线填充每行
        for i in range(len(lines)):
            lines[i] = '│' + lines[i][1:-1] + '┤'
        lines[0] = '┌' + lines[0][1:-1] + '┐'
        lines[-2] = lines[-2][:-1] + '┘'
        lines[-2] = lines[-2].replace("│", "└")
        lines[-2] = lines[-2].replace(" ", "─", lines[-2].count("└"))
        lines[-2] = lines[-2].replace("├", "─")

        lines[-1] = ''
        return '\n'.join(lines)


class NewVisualizer(VisualizerStrategy):
    def visualize(self, node, level=0, is_last_child=False):
        result = "This is new style!"
        indent = " " * level * 2
        if node.is_leaf():
            result += f"{indent}{icons['leaf']}{node.name}: {node.value}\n"
        else:
            result += f"{indent}{icons['composite']}{node.name}\n"
        return result

    def beautify(self, result):
        return result


# Context to use the strategy
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


# Builder Pattern
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


# Product of Builder
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


# Building tree
class TreeDirector:
    def __init__(self, builder):
        self._builder = builder

    def build_tree(self, data, name='root'):
        return self._builder.build(data, name)


args = FjeExplorer.parse_arguments()
json_data = FjeExplorer.load_json(args.file)
icons = FjeExplorer.load_icons("icons.json")[args.icons]

builder = CompositeNodeBuilder()
director = TreeDirector(builder)
json_tree = director.build_tree(json_data)

# Creating context with the chosen strategy
if args.style == "tree":
    strategy = TreeVisualizer()
elif args.style == "rectangle":
    strategy = RectangleVisualizer()
elif args.style == "new":
    strategy = NewVisualizer()
else:
    raise ValueError(f"Unknown style: {args.style}")

context = VisualizerContext(strategy)

# Visualization output
output = context.visualize(json_tree)
print(output)
