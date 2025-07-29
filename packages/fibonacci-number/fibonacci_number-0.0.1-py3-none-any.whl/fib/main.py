import argparse
import textwrap
import logging
import typer
from fib.parser import parallel_choices, parallel_args, parallel_functions

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('nth', type=int, help='n-th fibonacci number')
    parser.add_argument('-f', '--func', choices=parallel_choices, help=textwrap.dedent('''\
        the fibonacci function to choose:
          i   - iterative
          m   - matrix exponentiation
          r   - recursive
          rm  - recursive with memoization
          rc  - recursive with cache
        '''), default='r', metavar='FUNC')
    parser.add_argument('-p','--parallel', help='use the function with parallelization', action="store_true")
    parser.add_argument('-d','--depth', type = int, help='how many cores to use in parallelization', default=2)

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    args = parser.parse_args()

    for p in parallel_choices:
        if args.func == p:
            logging.info(f"Calculating fibonacci number {args.nth} using {p} function...")
            
            if args.parallel:
                logging.info(f"Using parallelization with depth {args.depth}...")
                if args.depth < 1 or args.depth > 8:
                    logging.warning(f"Depth can not be {args.depth}. It must be greater than 1 or less than 8. Using default value of 2.")
                    args.depth = 2

            fib_function = parallel_functions[parallel_choices.index(p)]
            result = parallel_args(fib_function, args.nth, args.parallel, args.depth)

    print(result)

if __name__ == "__main__":
    typer.run(main)