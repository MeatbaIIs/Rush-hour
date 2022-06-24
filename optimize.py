"""
Optimize a rush hour puzzle solution that was saved as csv.
Usage: optimize.py [SOLUTION_FILE.CSV]
"""

import csv
from code.algorithms.take_out_loops import TakeOutLoops
from code.algorithms.breadth_first_iter import BreadthFirstIter
from code.helpers import loader, solution_to_csv
from code.algorithms.improving_algorithm import Improving_algorithm
import argparse
import pandas as pd
from csv import reader
import re


def main(input_file_name):

    solution = []
    # Load solution in list of lists
    with open(input_file_name, 'r') as f:
        file_reader = reader(f)
        next(file_reader)
        for line in file_reader:
            solution.append([line[0], int(line[1])])

    puzzle_name = re.search(
        "data/Rushhour\d+x\d+_\d+", input_file_name).group() + ".csv"
    print(puzzle_name)
    grid = loader(puzzle_name)

    print(f'Optimizing a solution of {len(solution)} steps.')

    print('Taking out loops.')
    TOL = TakeOutLoops(grid, solution)
    solution = TOL.run()
    print(f'After taking out loops the solution is {len(solution)} steps.')

    print('Seeing if any useless steps can be left out.')
    IA = Improving_algorithm(grid, solution)
    solution = IA.run()
    print(
        f'After deleting useless steps the solution is {len(solution)} steps.')

    print('Iterating with Breadth First')
    BFI = BreadthFirstIter(grid, solution)
    solution = BFI.run()
    print(
        f'After iterating with breadth first the solution {len(solution)} steps.')

    print('Writing optimized solution to a csv file')
    filename = input_file_name.rstrip(".csv") + "_optimized.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['car', 'move'])

        for step in solution:
            # Write step to csv
            csvwriter.writerow(step)


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(
        description="Optimize a Rush hour puzzle solution")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
