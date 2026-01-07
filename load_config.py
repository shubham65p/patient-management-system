import yaml

import sys
import os

# def resource_path(relative_path):
#     if hasattr(sys, "_MEIPASS"):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# title = config["title"]
