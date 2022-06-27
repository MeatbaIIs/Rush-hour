import copy
import queue
import numpy as np


class BreadthFirst():
    """ Runs a breadth first algorithm on a Rush hour puzzle. """

    def __init__(self, grid):
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
        """ Get the next total_movements after all possible steps. """
        return self._grid.possible_next_lists(last_list)

    def run(self):
        """ Runs a breadth first algorithm """
        while not self._queue.empty():

            # Get total_movement_sequence from the queue
            state = self._queue.get()

            if self.is_solution(state):
                solution = self.solution_list_to_steps(state)
                break

            # Get last total_movements
            last_list = state[-1]

            # Look for possible new total_movements after taking one step
            for new_list in self.get_next_lists(last_list):
                new_tuple = tuple(new_list)

                # Skip if total_movements encountered before
                if new_tuple in self._visited:
                    continue

                # If not, put it in the queue
                self._visited.add(new_tuple)
                child = copy.deepcopy(state)
                child.append(new_list)
                self._queue.put(child)

        return solution
