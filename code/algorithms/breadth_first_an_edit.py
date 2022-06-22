"""
Example usage:
python3 main_an.py data/Rushhour6x6_2.csv
python3 code/visualization/visualization.py data/Rushhour6x6_2_solution.csv
"""

import copy
import queue
import numpy as np


class BreadthFirst():
    def __init__(self, grid):
        self._depth = 100
        self._queue = queue.Queue()
        self._empty_grid = []
        for _ in range(grid.get_size()):
            self._empty_grid.append(grid.get_size() * ['*'])#copy.deepcopy(grid.get_grid())

        self._grid = grid
        self._cars = grid.get_car_names()
        self._initial_x = {}
        self._initial_y = {}
        self._orientation = {}
        self._lengths = {}
        self._visited = []

        # Make dictionaries with info about all cars on the given grid
        for name in self._cars:
            self._initial_x[name] = grid.get_car_x(name)
            self._initial_y[name] = grid.get_car_y(name)
            self._orientation[name] = grid.get_car_orientation(name)
            self._lengths[name] = grid.get_car_length(name)

        self._queue.put([[0 for i in range(len(self._cars))]])
        self._visited.append([[0 for i in range(len(self._cars))]])

    def possible_next_lists(self, current_list):
        """ Gives the possible lists after one move on the grid that can be made with the given list """

        # Write the list to a grid and set this as current grid.
        grid = self.list_to_grid(current_list)
        self._grid.set_grid(grid)
        next_lists = []

        # For each car see what moves are possible
        for car, i in enumerate(self._cars):

            moves = self._grid.possible_moves(car)

            if moves and max(moves) > 0:
                distance = max(moves)
                next_list = copy.deepcopy(current_list)
                next_list[i] += distance
                next_lists.append(next_list)

            if moves and min(moves) < 0:
                distance = min(moves)
                next_list = copy.deepcopy(current_list)
                next_list[i] += distance
                next_lists.append(next_list)


            # for distance in moves:
            #
            #     # Write each move as a new list and collect all possible new lists
            #     next_list = copy.deepcopy(current_list)
            #     next_list[i] += distance
            #     next_lists.append(next_list)

        return next_lists

    def list_to_grid(self, list):
        """ Given a list with the total moved distance from the start position for each car, draws a list of lists that represents the grid """
        grid = copy.deepcopy(self._empty_grid)

        # Construct the grid
        # for i in range(self._grid.get_size()):
        #     grid.append(self._grid.get_size() * ['*'])

        # Add cars
        for i, car  in enumerate(self._cars):
            x = self._initial_x[car]
            y = self._initial_y[car]
            length = self._lengths[car]

            if self._orientation[car] == 'H':
                x += list[i]
                for j in range(length):
                    grid[y][x + j] = car
            else:
                y += list[i]
                for j in range(length):
                    grid[y + j][x] = car

            # Update coordinates in each Car object
            self._grid.set_car_x(car, x)
            self._grid.set_car_y(car, y)

        return grid

    def is_solution(self, state):
        """ Checks whether the given state is a solution """

        if state[-1][-1] + self._initial_x['X'] == self._grid.get_size() - 2:
            return True

        return False

    def solution_list_to_steps(self, state):
        """
        Given a list of lists of total moved distances for each car, e.g. [-2, 0, 5, 1]
        rewrite this as steps, e.g. [X, 2]
        """
        steps = []
        previous_state = state[0]

        for next_state in state[1:]:

            for i in range(len(previous_state)):

                if not next_state[i] == previous_state[i]:
                    car = self._cars[i]
                    distance = next_state[i] - previous_state[i]

            steps.append([car, distance])
            previous_state = next_state

        return steps

    def run(self):
        """ Runs a breadth first algorithm """

        print('looking for a solution of max ' + str(self._depth) + ' steps')

        while not self._queue.empty():

            state = self._queue.get()


            if self.is_solution(state):
                print('found a solution of ' + str(len(state)) + ' steps.')
                solution = self.solution_list_to_steps(state)
                break

            # Get list representation of the grid after the last step
            last_list = state[-1]

            if len(state) < self._depth:

                # Look for possible new grid representations and add them to queue if not encountered before.
                for new_list in self.possible_next_lists(last_list):

                    if new_list in self._visited:
                        continue

                    self._visited.append(new_list)
                    child = copy.deepcopy(state)
                    child.append(new_list)
                    self._queue.put(child)

        return solution
