"""
Takes Rush hour puzzle in the command line and solves it.
Usage: main.py [PUZZLE_NAME.CSV]
"""

import csv
from code.algorithms.breadth_first_an import BreadthFirst as BF
from code.algorithms.breadth_first_furthest import BreadthFirstFurthest as BFF
from code.algorithms.depth_first import Depth_first as DF
from code.algorithms.random import Random 
from code.classes.car import Car
from code.helpers import loader, batchrunner
from code.classes.grid import Grid
from code.visualization.histogram import histogram_and_plot
import argparse


def main(input_file_name):
    # make a histogram and a plot for the input_file for every known method after 1000 steps (batchrunned)
    histogram_and_plot(input_file_name, 100)
    
if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
