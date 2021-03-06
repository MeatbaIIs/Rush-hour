import copy
from ..helpers import check_solution


class RemoveUseless():
    def __init__(self, grid, solution):
        """ For a solution to a Rush hour puzzle, check for each step if it can be left out. """
        self._grid = grid
        self._solution = solution
        self._test_solution = []

    def correct_later_moves(self, car, distance, step):
        """
        Correct the next move of car 'car' after step 'step' for the given distance.
        If the next move of car is the same disance in the opposite direction, remove the next move as well.
        Otherwise, add the given distance to the next move.
        """
        for i in range(step, len(self._test_solution)):
            if self._test_solution[i][0] == car:
                if self._test_solution[i][1] == -distance:
                    removing = self._test_solution.pop(i)
                    return
                else:
                    self._test_solution[i][1] += distance
                    return

    def step(self, i):
        """ Attempt to make a solution where the i-th move is left out. """

        # Remove move at index i from solution
        self._test_solution = copy.deepcopy(self._solution)
        deleted_step = self._test_solution.pop(i)
        car = deleted_step[0]
        distance = deleted_step[1]

        # Correct the next move
        self.correct_later_moves(car, distance, i)

        # Modify solution if new solution is valid
        if check_solution(self._grid, self._test_solution):
            self._solution = copy.deepcopy(self._test_solution)
            return True
        return False

    def run(self):
        """
        Check for every move if it can be removed from the solution.
        Runs as long as new optimizations have been found
        Returns the optimized solution
        """
        print("Running Remove Useless algorithm")
        found_optimization = True

        while found_optimization:
            found_optimization = False
            for i in range(len(self._solution)):
                if self.step(i):
                    found_optimization = True
                    break

        return self._solution
