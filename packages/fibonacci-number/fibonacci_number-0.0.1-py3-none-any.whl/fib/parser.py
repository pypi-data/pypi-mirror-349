from typing import Callable

from fib.fib import (
    fib_iterative,
    fib_matrix,
    fib_recursive,
    fib_recursive_memoization,
    fib_recursive_cache,
)

parallel_choices = [
    'i',
    'm',
    'r',
    'rm',
    'rc',
    ]

parallel_functions = [
    fib_iterative,
    fib_matrix,
    fib_recursive,
    fib_recursive_memoization,
    fib_recursive_cache,
    ]

def parallel_args(func: Callable, n: int, parallel: bool = False, depth: int = 0):
    if parallel:
        return func(n, parallel, depth)
    else:
        return func(n)