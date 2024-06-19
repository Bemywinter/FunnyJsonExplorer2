from builder import CompositeNodeBuilder
from builder import TreeDirector
from context import VisualizerContext
from strategy import *
import argparse
import json

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

args = FjeExplorer.parse_arguments()
json_data = FjeExplorer.load_json(args.file)
icons = FjeExplorer.load_icons("icons.json")[args.icons]

builder = CompositeNodeBuilder()
director = TreeDirector(builder)
json_tree = director.build_tree(json_data)

# Creating context with the chosen strategy
if args.style == "tree":
    strategy = TreeVisualizer(icons)
elif args.style == "rectangle":
    strategy = RectangleVisualizer(icons)
elif args.style == "new":
    strategy = NewVisualizer(icons)
else:
    raise ValueError(f"Unknown style: {args.style}")

context = VisualizerContext(strategy)

# Visualization output
output = context.visualize(json_tree)
print(output)
