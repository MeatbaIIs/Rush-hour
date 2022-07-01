import copy
from .breadth_first import BreadthFirst
import queue
from ..helpers import set_total_movements, total_movements_sequence_to_steps
import random


class BreadthFirstIter(BreadthFirst):
    def __init__(self, grid, solution):
        super().__init__(grid)
        self._start = []
        self._end = []
        self._given_solution = solution
        self._car_indexes = {}
        for i, name in enumerate(self._grid.get_car_names()):
            self._car_indexes[name] = i

        self._total_movements_sequence = []
        self._total_movements_sequence.append(
            tuple([0 for i in self._grid.get_car_names()]))
        self._counter = 0

    def init_iteration(self, index):
        self._start = self._total_movements_sequence[index]
        self._end = self._total_movements_sequence[index+7]
        self._visited = set()
        self._visited.add(tuple(self._start))
        self._queue = queue.Queue()
        self._queue.put([self._start])
        set_total_movements(self._grid, self._start)

    def is_solution(self, total_movements_sequence):
        if total_movements_sequence[-1] == self._end:
            return True
        return False

    def load_solution(self):
        for car, distance in self._given_solution:
            car_index = self._car_indexes[car]
            new_total_movements = list(copy.deepcopy(
                self._total_movements_sequence[-1]))
            new_total_movements[car_index] += distance
            self._total_movements_sequence.append(tuple(new_total_movements))

    def run(self):
        """ Runs a breadth first algorithm """
        while not self._queue.empty():

            # Get total_movement_sequence from the queue
            total_movements_sequence = self._queue.get()

            if self.is_solution(total_movements_sequence):
                solution = total_movements_sequence_to_steps(
                    self._grid, total_movements_sequence)
                break

            # Get last total_movements
            last_total_movements = list(total_movements_sequence[-1])

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

    def run_iterations(self):
        self.load_solution()

        for i in range(len(self._given_solution)-7):
            # Run iteration
            self.init_iteration(i)
            optimized_sequence = self.run()

            # Check if an improved sequence was found
            if len(optimized_sequence) < 7:
                self._counter += 1
                self._solution_states = self._solution_states[:i] + \
                    optimized_sequence + self._solution_states[i+7:]

        print(f'Found {self._counter} optimizations.')
        return self.solution_list_to_steps(self._solution_states)
