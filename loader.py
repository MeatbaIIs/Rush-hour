"""
Initialize a grid with the Rush Hour puzzle given as command line argument, solve the puzzle, and visualize the solution.
Usage: loader.py [PUZZLE_NAME.CSV]
"""

from grid import Grid
import argparse
import re


def main(input_file_name):
    # Get grid size from the input file name
    size = re.search(
        "Rushhour.+x", input_file_name).group().lstrip("Rushhour").rstrip("x")

    # Load grid
    grid = Grid(int(size))

    # Load cars in the grid
    with open(input_file_name) as f:

        # Skip over first line
        f.readline()

        while True:
            line = f.readline().strip().split(",")

            if line == [""]:
                break

            grid.add_car(line[0], line[1], int(line[2]) - 1,
                         int(line[3]) - 1, int(line[4]))

    return grid


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    grid = main(args.input)

    grid.print_grid()
    grid.give_empties()
    print("doing all possible moves")
    grid.give_all_possible_moves()



    grid.neighbours(1, 1)
    grid.possible_cars(3, 4)
    grid.random_algorythm()
