"""
Initialize a grid with the Rush Hour puzzle given as command line argument, solve the puzzle, and visualize the solution.
Usage: loader.py [PUZZLE_NAME.CSV]
"""

from grid import Grid
import argparse
import re


def main(input_file_name):
    # Get grid size from the input file name
    size = re.search("Rushhour.+x", input_file_name).group()
    size = re.search("\d", size).group()

    # Load grid
    grid = Grid(size)

    # Load cars in the grid
    with open(input_file_name) as f:
        # Skip over first line
        f.readline()
        while True:
            line = f.readline().strip().split(",")

            if line == [""]:
                break

            grid.add_car(line[0], line[1], line[2], line[3], line[4])


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
