import os
import sys

def load_resource(path):
    """
    Helper to get resource paths, works for normal run & PyInstaller bundle.
    Also handles if the path is already absolute.
    """
    if os.path.isabs(path): # If path is already absolute, return it directly
        return path
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundles stuff here
        base_path = sys._MEIPASS
    else:
        # Normal execution path, resolves relative to this utils.py file
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, path)