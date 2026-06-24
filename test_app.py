import pytest
from app import add_numbers, subtract_numbers

def test_addition():
    assert add_numbers(5, 5) == 10
    assert add_numbers(-1, 1) == 0

def test_subtraction():
    assert subtract_numbers(10, 5) == 5
