import pytest

from fib import (
    fib_iterative,
    fib_recursive,
    fib_recursive_cache,
    fib_recursive_memoization,
    fib_matrix,
)

fibonacci_functions = [
    fib_iterative,
    fib_recursive,
    fib_recursive_cache,
    fib_recursive_memoization,
    fib_matrix,
]

def test_fib_9_is_34():
    for function in fibonacci_functions:
        assert function(9) == 34


def test_fib_negative_raise_error():
    with pytest.raises(ValueError):
        fib_iterative(-1)


def test_fib_34_is_5702887():
    for function in fibonacci_functions:
        assert function(34) == 5702887


def test_fib_0_is_0():
    for function in fibonacci_functions:
        assert function(0) == 0


def test_fib_1_is_1():
    for function in fibonacci_functions:
        assert function(1) == 1


def test_fib_2_is_1():
    for function in fibonacci_functions:
        assert function(2) == 1


def test_fib_large_number():
    for function in fibonacci_functions:
        assert function(50) == 12586269025


def test_fib_non_integer_input():
    with pytest.raises(TypeError):
        fib_iterative(3.5)
    with pytest.raises(TypeError):
        fib_iterative("string")


def test_fib_large_negative_raises_error():
    with pytest.raises(ValueError):
        fib_iterative(-100)