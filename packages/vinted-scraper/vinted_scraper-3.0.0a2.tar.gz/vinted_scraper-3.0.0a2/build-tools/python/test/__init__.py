"""Workaround founf on https://stackoverflow.com/a/59732673"""

import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, "src")
sys.path.append(SOURCE_PATH)
