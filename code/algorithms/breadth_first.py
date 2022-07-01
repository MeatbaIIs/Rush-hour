import copy
import queue
import numpy as np
from ..helpers import is_solution, total_movements_sequence_to_steps, next_total_movements


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
        print("Running Breadth-first algorithm")

    def get_next_total_movements(self, total_movements):
        """ Get the next total_movements after all possible steps. """
        return next_total_movements(self._grid, total_movements, furthest=False)

    def run(self):
        """ Runs a breadth first algorithm """
        while not self._queue.empty():

            # Get total_movement_sequence from the queue
            total_movements_sequence = self._queue.get()

            if is_solution(self._grid, total_movements_sequence):
                solution = total_movements_sequence_to_steps(
                    self._grid, total_movements_sequence)
                break

            # Get last total_movements
            last_total_movements = total_movements_sequence[-1]

            # Look for possible new total_movements after taking one step
            for total_movements in self.get_next_total_movements(last_total_movements):
                new_tuple = tuple(total_movements)

                # Skip if total_movements encountered before
                if new_tuple in self._visited:
                    continue

                # If not, put it in the queue
                self._visited.add(new_tuple)
                child = copy.deepcopy(total_movements_sequence)
                child.append(total_movements)
                self._queue.put(child)

        return solution
