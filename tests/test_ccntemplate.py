import pytest
from ccn_template import hello_world

def test_1():
  print("Hello CCN")

def test_2():
  hello_world.hello_world_func("CCN")
