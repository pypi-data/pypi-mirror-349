from multiprocessing import Process, Queue
from typing import Callable
import numpy as np
from numpy.linalg import matrix_power

def fib_worker(func :Callable, n :int, q: Queue, depth :int):
    q.put(func(n, depth))


def parallel_computing_recursive(func :Callable, n: int, depth :int):
    q1 = Queue()
    q2 = Queue()

    p1 = Process(target=fib_worker, args=(func, n - 1, q1, depth-1))
    p2 = Process(target=fib_worker, args=(func, n - 2, q2, depth-1))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    result1 = q1.get()
    result2 = q2.get()

    return result1 + result2


def parallel_computing_matrix(func :Callable, n: int, depth :int):
    q1 = Queue()
    q2 = Queue()

    p1 = Process(target=fib_worker, args=(func, n - 1, q1, depth-1))
    p2 = Process(target=fib_worker, args=(func, n - 2, q2, depth-1))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    result1 = q1.get()
    result2 = q2.get()

    return result1**2 + result2**2


def fib_odd(n: int, parallel :bool = False, depth :int = 0):
    n = int((n+1)/2)+1
    if parallel and depth:
        return parallel_computing_matrix(fibmat, n, depth)
    Fn = fibmat(n-1) 
    Fn1 = fibmat(n-2)
    return Fn1**2 + Fn**2

def fib_even(n: int, parallel :bool = False, depth :int = 0):
    n = int(n/2)+1
    if parallel and depth:
        return parallel_computing_matrix(fibmat, n, depth)
    Fn = fibmat(n-1) 
    Fn1 = fibmat(n-2)
    return Fn * (2*Fn1 + Fn)

def fibmat(n: int):
    i = np.array([[0, 1], [1, 1]])
    return np.matmul(matrix_power(i, n), np.array([1, 0]))[1]