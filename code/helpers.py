"""
This file contains helper functions for the rest of the files in this project
"""
import csv
from typing import Dict
from .classes.grid import Grid
import re
from typing import List, Dict
import copy
from csv import reader


def loader(input_file_name):
    """
    Initialize a grid with the Rush Hour puzzle given as argument
    """
    size = re.search(
        "Rushhour.+x", input_file_name).group().lstrip("Rushhour").rstrip("x")

    grid = Grid(int(size))

    # Load cars in the grid
    with open(input_file_name) as f:

        f.readline()
        car_num = 0

        while True:
            line = f.readline().strip().split(",")

            if line == [""]:
                break

            grid.add_car(line[0], line[1], int(line[2]) - 1,
                         int(line[3]) - 1, int(line[4]), car_num)

            car_num += 1

    return grid


def check_filename(filename):
    """Adds the right folder and extension to a filename"""
    if not ".csv" in filename:
        filename = filename + ".csv"

    if not "data/" in filename:
        filename = "data/" + filename

    return filename


def ask_for_solution():
    """Ask for a filename of a solution and adds the right folder and extension if necessary"""
    solution_name = input("What is the file name of the solution? ")
    solution_name = check_filename(solution_name)
    return solution_name


def solution_to_csv(solution, filename):
    """ takes a solution formatted as a list of steps and outputs this to a csv file """

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['car', 'move'])

        for step in solution:

            # Write step to csv
            csvwriter.writerow(step)


def load_solution(filename):
    """ Loads solution from csv file and returns it """
    solution = []

    # Load solution in list of lists
    with open(filename, 'r') as f:
        file_reader = csv.reader(f)
        next(file_reader)

        for line in file_reader:
            solution.append([line[0], int(line[1])])

    return solution


def is_solution(grid, total_movements_sequence):
    """ Checks whether the given total_movements_sequence is a solution for a given Grid object"""
    set_total_movements(grid, total_movements_sequence[-1])
    if grid.win():
        return True
    return False


def check_solution(grid, solution):
    """ Returns True if a solution is a valid solution. """
    gridcopy = copy.deepcopy(grid)

    # Run through all moves in the solution
    for move in solution:
        car = move[0]
        distance = move[1]

        # Check if the move is possible
        if not distance in gridcopy.possible_moves(car):
            return False
        gridcopy.move(car, distance)

    # Check if Rush hour puzzle is solved after carrying out all moves
    if gridcopy.win():
        return True
    return False


def total_movements_sequence_to_steps(grid, solution):
    """
    Given a sequence of total_movements, e.g. [-2, 0, 5, 1]
    rewrite this as steps, e.g. [X, 2]
    """
    steps = []
    previous_total_movements = solution[0]

    for next_total_movements in solution[1:]:

        for i in range(len(previous_total_movements)):

            if not next_total_movements[i] == previous_total_movements[i]:
                car = grid.get_car_names()[i]
                distance = next_total_movements[i] - \
                    previous_total_movements[i]
                break

        steps.append([car, distance])
        previous_total_movements = next_total_movements

    return steps


def steps_to_total_movements_sequence(grid, steps):
    """
    Given steps and a grid, rewrite these as a sequence of states, which are represented as total_movements.
    """
    total_movements = grid.get_initial_total_movements()
    total_movements_sequence = [copy.copy(total_movements)]
    for move in steps:
        for i, car in enumerate(grid.get_car_names()):
            if car == move[0]:
                distance = move[1]
                total_movements[i] += distance
                total_movements_sequence.append(copy.copy(total_movements))

    return total_movements_sequence


def set_total_movements(grid, total_movements):
    """ Sets grid object to a state with the given total_movements """
    new_grid = copy.deepcopy(grid.get_empty_grid())

    for i, name in enumerate(grid.get_car_names()):
        x = grid.get_car_initial_x(name)
        y = grid.get_car_initial_y(name)
        length = grid.get_car_length(name)

        if grid.get_car_orientation(name) == 'H':
            x += total_movements[i]
            for j in range(length):
                new_grid[y][x + j] = name
        else:
            y += total_movements[i]
            for j in range(length):
                new_grid[y+j][x] = name

        # Update coordinates in each Car object
        grid.set_car_x(name, x)
        grid.set_car_y(name, y)
        grid.set_grid(new_grid)

    return


def next_total_movements(grid, total_movements, furthest):
    """ Gives the possible total_movements after one move on the grid that can be made with the given total_movements """

    set_total_movements(grid, total_movements)
    next_total_movements = []

    # For each car see what moves are possible
    for i, name in enumerate(grid.get_car_names()):

        if furthest:
            moves = grid.furthest_possible_moves(name)
        else:
            moves = grid.possible_moves(name)

        for distance in moves:

            # Write each move as a new total_movements and append
            next_total_movement = copy.deepcopy(total_movements)
            next_total_movement[i] += distance
            next_total_movements.append(next_total_movement)

    return next_total_movements


class MethodInputError(Exception):
    """Raised when a method input is wrong"""
    pass
