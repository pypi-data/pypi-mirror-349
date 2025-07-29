import unittest

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

class TestFibonacci(unittest.TestCase):

    def test_fibonacci_functions(self):

        n_and_fib = [
            [4, 3],
            [7, 13],
            [10, 55],
            [14, 377]
            ]
        
        for function in fibonacci_functions:
            for element in n_and_fib:
                for input, expected in n_and_fib:
                    self.assertEqual(function(input), expected)


    def test_fibonacci_negative(self):
        with self.assertRaises(ValueError):
            fib_iterative(-1) 



if __name__ == "__main__":
    unittest.main()