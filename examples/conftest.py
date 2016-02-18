import sys
import os
import pytest


# @todo: need a better way to do this, the test for example 6 
# @todo: uses some of the framework from the implementation
# @todo: it wants to import some of the objects ...
sys.path.append('ex6_vgasys/myhdl')

@pytest.fixture(scope="session")
def expath():
    return os.curdir
