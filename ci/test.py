import pytest
from app import add_numbers, subtract_numbers

# Test case 1: Checks if addition works
def test_addition():
    assert add_numbers(5, 5) == 10
    assert add_numbers(-1, 1) == 0

# Test case 2: Checks if subtraction works
def test_subtraction():
    assert subtract_numbers(10, 5) == 5
