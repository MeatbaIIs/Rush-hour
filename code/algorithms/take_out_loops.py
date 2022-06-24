import copy


class TakeOutLoops():
    def __init__(self, grid, solution):
        self._grid = grid
        self._given_solution = solution
        self._car_indexes = {}
        for i, name in enumerate(self._grid.get_car_names()):
            self._car_indexes[name] = i

        self._solution_states = []
        self._solution_states.append(tuple([0 for i in self._car_indexes]))
        self._optimized_states = []

        self._optimized_solution = copy.deepcopy(self._given_solution)

    def load_solution(self):

        for car, distance in self._given_solution:
            car_index = self._car_indexes[car]
            new_state = list(copy.deepcopy(self._solution_states[-1]))
            new_state[car_index] += distance
            self._solution_states.append(tuple(new_state))

        return

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

    def run(self):
        """ For a given solution, check if the same state is visited multiple times and take out the steps in between """
        self.load_solution()
        counter = 0

        for state in self._solution_states:

            if not state in self._optimized_states:
                self._optimized_states.append(state)
                continue

            counter += 1
            loop_start = self._optimized_states.index(state)
            self._optimized_states = self._optimized_states[:loop_start]
            self._optimized_states.append(state)

        print(f'Found and took out {counter} loops.')

        return self.solution_list_to_steps(self._optimized_states)
