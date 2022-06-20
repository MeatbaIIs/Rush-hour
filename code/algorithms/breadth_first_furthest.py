"""
Runs a breadth first algorithm with an added heuristic on a Rush hour puzzle. 
Heuristic: instead of saving all possible moves, it only saves one (of the) move(s) with the furthest distance.
           solutions might not be the best solution, but the algorithm works faster than the original breadth first.

How to use:
-   first load the grid with the initial state, using the loader function:
    grid = loader(input_file_name)
-   then use the algorithm to get a solution:
    breadth_first = BreadthFirstFurthest(grid)
    solution = breadth_first.run()

Puzzle 1: around 0.0 minutes, solution of 21 steps
Puzzle 2: around 0.0 minutes, solution of 15 steps
Puzzle 3: around 0.02 minutes, solution of 33 steps
Puzzle 4: around 1 minutes, solution of 28 steps
Puzzle 5: stopped after more than 10 minutes
Puzzle 6: 
"""

import copy
import queue
import numpy as np
import time
import random


class BreadthFirstFurthest():
    def __init__(self, grid):
        # Queue is a queue of lists of lists
        self._queue = queue.Queue()
        self._empty_grid = []
        for _ in range(grid.get_size()):
            self._empty_grid.append(grid.get_size() * ['*'])

        self._grid = grid
        self._cars = grid.get_car_names()
        self._initial_x = {}
        self._initial_y = {}
        self._orientation = {}
        self._lengths = {}

        # Visited is a set of tuples
        self._visited = set()
        self._visited.add(tuple([0 for i in range(len(self._cars))]))

        # Make dictionaries with info about all cars on the given grid
        for name in self._cars:
            self._initial_x[name] = grid.get_car_x(name)
            self._initial_y[name] = grid.get_car_y(name)
            self._orientation[name] = grid.get_car_orientation(name)
            self._lengths[name] = grid.get_car_length(name)

        self._queue.put([[0 for i in range(len(self._cars))]])

    def possible_next_lists(self, current_list):
        """ Gives the possible lists after one move on the grid that can be made with the given list """

        # Write the list to a grid and set this as current grid.
        grid = self.list_to_grid(current_list)
        self._grid.set_grid(grid)
        next_lists = []

        # For each car see what moves are possible
        for i in range(len(self._cars)):

            moves = self._grid.possible_moves(self._cars[i])

            if not moves:
                continue

            # Select (one of the) move(s) with furthest distance
            if abs(moves[0]) > abs(moves[-1]):
                distance = moves[0]
            elif abs(moves[-1]) > abs(moves[0]):
                distance = moves[-1]
            else:
                distance = random.choice([moves[0], moves[-1]])

            next_list = copy.deepcopy(current_list)
            next_list[i] += distance
            next_lists.append(next_list)

        return next_lists

    def list_to_grid(self, list):
        """ Given a list with the total moved distance from the start position for each car, draws a list of lists that represents the grid """
        grid = copy.deepcopy(self._empty_grid)

        # Add cars
        for i in range(len(self._cars)):
            car = self._cars[i]
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
        st = time.time()
        while not self._queue.empty():

            state = self._queue.get()

            if self.is_solution(state):
                print('found a solution of ' + str(len(state)-1) + ' steps.')
                solution = self.solution_list_to_steps(state)
                et = time.time()
                break

            # Get list representation of the grid after the last step
            last_list = state[-1]

            # Look for possible new grid representations and add them to queue if not encountered before.
            for new_list in self.possible_next_lists(last_list):
                new_tuple = tuple(new_list)
                if new_tuple in self._visited:
                    continue

                self._visited.add(new_tuple)
                child = copy.deepcopy(state)
                child.append(new_list)
                self._queue.put(child)

        time_taken = et - st
        return solution, time_taken
