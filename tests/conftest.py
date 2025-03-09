# tests/conftest.py
import os
import sys

# Vertel Python waar je projectmap staat
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)