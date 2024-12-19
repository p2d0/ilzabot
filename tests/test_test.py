# import sys,os
# sys.path.append(os.getcwd())
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.kekes import kekes

def test_import():
    assert kekes() == 1
