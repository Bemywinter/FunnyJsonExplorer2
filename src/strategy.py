from abc import ABC, abstractmethod


class VisualizerStrategy(ABC):
    def __init__(self, icons):
        self.icons = icons
    @abstractmethod
    def visualize(self, node, level=0, is_last_child=False):
        pass

    @abstractmethod
    def beautify(self, result):
        pass


class TreeVisualizer(VisualizerStrategy):
    def visualize(self, node, level=0, is_last_child=False):
        result = ""
        prefix = "└─" if is_last_child else "├─"
        indent = "  " * (level - 1) if level > 0 else ""
        if node.is_leaf():
            if node.value is None:
                result += f"{indent}{prefix}{self.icons['leaf']}{node.name}\n"
            else:
                result += f"{indent}{prefix}{self.icons['leaf']}{node.name}: {node.value}\n"
        else:
            if node.name != "root":
                result += f"{indent}{prefix}{self.icons['composite']}{node.name}\n"
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
                result += f"{indent}{prefix}{self.icons['leaf']}{node.name}\n"
            else:
                result += f"{indent}{prefix}{self.icons['leaf']}{node.name}: {node.value}\n"
        else:
            if node.name != "root":
                result += f"{indent}{prefix}{self.icons['composite']}{node.name}\n"
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
            result += f"{indent}{self.icons['leaf']}{node.name}: {node.value}\n"
        else:
            result += f"{indent}{self.icons['composite']}{node.name}\n"
        return result

    def beautify(self, result):
        return result
