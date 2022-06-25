"""
Runs a breadth first algorithm on a Rush hour puzzle.
How to use:
-   first load the grid with the initial state, using the loader function:
    grid = loader(input_file_name)
-   then use the algorithm to get a solution:
    breadth_first = BreadthFirst(grid)
    solution = breadth_first.run()
Puzzle 1: around 0.0 minutes, solution of 21 steps
Puzzle 2: around 0.01 minutes, solution of 15 steps
Puzzle 3: around 0.03 minutes, solution of 33 steps
Puzzle 4: around 2,5 minutes, solution of 27 steps
Puzzle 5: killed
Puzzle 6: killed
"""

import copy
import queue
import numpy as np


class BreadthFirst():
    def __init__(self, grid):
        print("Running Breadth First algorithm")
        self._grid = grid
        initial_list = [0 for i in range(len(self._grid.get_car_names()))]

        # Queue is a queue of lists of lists
        self._queue = queue.Queue()
        self._queue.put([initial_list])

        # Visited is a set of tuples
        self._visited = set()
        self._visited.add(tuple(initial_list))

    def is_solution(self, state):
        """ Checks whether the given state is a solution """
        self._grid.set_configuration_from_list(state[-1])
        if self._grid.win():
            return True
        return False

    def solution_list_to_steps(self, solution):
        """ 
        Given a list of lists of total moved distances for each car, e.g. [-2, 0, 5, 1]
        rewrite this as steps, e.g. [X, 2]
        """
        steps = []
        previous_state = solution[0]

        for next_state in solution[1:]:

            for i in range(len(previous_state)):

                if not next_state[i] == previous_state[i]:
                    car = self._grid.get_car_names()[i]
                    distance = next_state[i] - previous_state[i]

            steps.append([car, distance])
            previous_state = next_state

        return steps

    def get_next_lists(self, last_list):
        return self._grid.possible_next_lists(last_list)

    def run(self):
        """ Runs a breadth first algorithm """

        # print('looking for a solution')

        while not self._queue.empty():

            state = self._queue.get()

            if self.is_solution(state):
                # print('found a solution of ' + str(len(state)-1) + ' steps.')
                solution = self.solution_list_to_steps(state)
                break

            # Get list representation of the grid after the last step
            last_list = state[-1]

            # Look for possible new grid representations and add them to queue if not encountered before.
            for new_list in self.get_next_lists(last_list):
                new_tuple = tuple(new_list)
                if new_tuple in self._visited:
                    continue

                self._visited.add(new_tuple)
                child = copy.deepcopy(state)
                child.append(new_list)
                self._queue.put(child)

        return solution
