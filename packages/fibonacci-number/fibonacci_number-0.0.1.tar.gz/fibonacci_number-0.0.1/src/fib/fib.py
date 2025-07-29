import functools

from fib.parallelization import parallel_computing_recursive, fib_even, fib_odd

def fib_iterative(n: int) -> int:
    if n < 0:
        raise ValueError("n must be grater than 0")
    if n < 2:
        return n
    
    n0 = 0
    n1 = 1
    for _ in range(n):
        nth = n0 + n1
        n0 = n1
        n1 = nth
    return n0


def fib_matrix(n: int, parallel :bool = False, depth :int = 0):
    if n%2 == 0:
        return fib_even(n, parallel, depth)
    return fib_odd(n, parallel, depth)


def fib_recursive(n: int, parallel :bool = False, depth :int = 0) -> int:
    if n < 0:
        raise ValueError("n must be grater than 0")
    if n < 2:
        return n
    if parallel and depth:
        return parallel_computing_recursive(fib_recursive, n, depth)
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)


cache = {}

def fib_recursive_memoization(n: int, parallel :bool = False, depth :int = 0) -> int:
    if n < 0:
        raise ValueError("n must be grater or equal to zero.")
    if n < 2:
        return n
    if n in cache:
        return cache[n]
    if parallel and depth:
        return parallel_computing_recursive(fib_recursive_memoization, n, depth)
    
    nth = fib_recursive_memoization(n - 1) + fib_recursive_memoization(n - 2)

    cache[n] = nth

    return nth


@functools.cache
def fib_recursive_cache(n: int, parallel :bool = False, depth :int = 0) -> int:
    if n < 0:
        raise ValueError("n must be grater or equal to zero.")
    if n < 2:
        return n
    if parallel and depth:
        return parallel_computing_recursive(fib_recursive_cache, n, depth)
    return fib_recursive_cache(n - 1) + fib_recursive_cache(n - 2)