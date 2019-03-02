import sys
sys.path.insert(0, '../')
import ruleset

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

def test_e():
    assert ruleset.dummy_input != None