import copy
from ..helpers import steps_to_total_movements_sequence, total_movements_sequence_to_steps


class TakeOutLoops():
    def __init__(self, grid, solution):
        self._grid = grid
        self._given_solution = solution

        self._total_movements_sequence = []
        self._optimized_sequence = []

    def run(self):
        """ For a given solution, check if the same state is visited multiple times and take out the steps in between """
        print("Running Take-Out-Loops algorithm")
        self._total_movements_sequence = steps_to_total_movements_sequence(
            self._grid, self._given_solution)
        counter = 0

        for total_movements in self._total_movements_sequence:

            if not total_movements in self._optimized_sequence:
                self._optimized_sequence.append(total_movements)
                continue

            counter += 1
            loop_start = self._optimized_sequence.index(total_movements)
            self._optimized_sequence = self._optimized_sequence[:loop_start]
            self._optimized_sequence.append(total_movements)

        print(f'Found and took out {counter} loops.')

        return total_movements_sequence_to_steps(self._grid, self._optimized_sequence)
