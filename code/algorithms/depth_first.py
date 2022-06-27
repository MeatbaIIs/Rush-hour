from code.classes.grid import Grid
from copy import deepcopy, copy
from code.helpers import steps_to_total_movements_sequence, set_total_movements, total_movements_sequence_to_steps



class DepthFirst():
    def __init__(self, grid, best_solution=float('inf'), solution=[]):
        self._grid = grid
        amount_of_cars = len(self._grid.get_car_names())
        # self._stack = [[[0 for i in range(amount_of_cars)]]]
        self._empty_state = [[0 for i in range(amount_of_cars)]]
        self._visited = {tuple([0 for i in range(amount_of_cars)]):0}

        for i, state in enumerate(solution):
            self._visited[tuple(state)] =  i

        if solution:
            solution = steps_to_total_movements_sequence(grid, solution)
            self._solutions = [solution]

        else:
            self._solutions = []

        self._best_solution = best_solution

    def remove_long_visited(self, length):
        """removes the configurations in visited that are longer than the current best solution"""
        to_remove = []
        for key in self._visited:
            if self._visited[key] > length:
                to_remove.append(key)

        for key in to_remove:
            del self._visited[key]

    def check_for_better_solution(self, new_list, state):
        """
        Looks if the current configuration has been used in a state and
        replaces part of the steps if this is is a faster way to reach the solution
        """
        # als hij deze wel sneller doet kan het zijn dat die state al in een vorige oplossing is gevonden, als dit zo is is dit een snelleren oplossing
        for i, solution in enumerate(self._solutions):

            for j, config in enumerate(solution):

                # als de huidige staat sneller bereikt is dan in de huidige oplossing wordt dat stuk van de oplossing vervangen
                if new_list == config:
                    solution[:j] = state + [new_list]

                    # als dit beter is dan be beste oplossing wardt dat opgeslagen
                    if len(solution) < self._best_solution:
                        self._best_solution = len(solution) - 1
                        print(f'found solution of {len(solution) - 2} steps')
                        self.remove_long_visited(self._best_solution)
                        print(total_movements_sequence_to_steps(self._grid, solution))


    def pick_best_solution(self):
        """pick the beste solution out of al solutions found"""
        best_solution_len = float('inf')
        best_solution_steps = []
        for solution in self._solutions:
            if len(solution) < best_solution_len:
                best_solution_steps = total_movements_sequence_to_steps(self._grid, solution)
        return best_solution_steps

    def get_next_state(self, new_list, state):
        """add a new configuration to the stack"""
        self._new_state = True
        self._visited[tuple(new_list)] = len(state) - 1
        state.append(new_list)
        #self._stack.append(state)
        return state

    def check_for_new_state(self, state):
        """check whether a new configuration can be reached, otherwise take a step back"""
        if not self._new_state and len(state) > 0:
            state.pop()
        return state
            # self._stack.append(state)

    def check_for_solution(self, state):
        """checks whether a solution is reached"""
        if self._grid.win():
            print('found a solution of ' + str(len(state) - 1) + ' steps.')
            self._solutions.append(copy(state))
            self._best_solution = len(state) - 1
            self.remove_long_visited(self._best_solution)
            print(total_movements_sequence_to_steps(self._grid, state))

    def run(self):
        """
        Runs the depth-first algorithm with as little memory use as possible
        """
        state = copy(self._empty_state)
        while state:
            # get the top configuration of the stack
            # state = self._stack.pop()

            # get the last configuaration of the current state
            last_list = state[-1]
            set_total_movements(self._grid, last_list)

            self._new_state = False



            current_steps = len(state) - 1

            # check for every car what moves are available and try them
            for i, car in enumerate(self._grid.get_car_names()):

                moves = self._grid.possible_moves(car)
                # make sure to stop searching deeper when the length of the best solution is reached
                if len(state) < self._best_solution:
                    longest_moves = set()

                    if moves and max(moves) > 0:
                        longest_moves.add(max(moves))

                    if moves and min(moves) < 0:
                        longest_moves.add(min(moves))

                    for move in longest_moves:

                        # make a copy of the last list to add a move
                        new_list = copy(state[-1])
                        new_list[i] += move

                        # if the configuration has been reached before and has now been reached faster, check for a better solution
                        if tuple(new_list) in self._visited and self._visited[tuple(new_list)] > current_steps:
                            self.check_for_better_solution(new_list, state)
                            state = self.get_next_state(new_list, state)
                            set_total_movements(self._grid, new_list)
                            break

                        # if the configuration has never been reached, try it out
                        elif tuple(new_list) not in self._visited:
                            state = self.get_next_state(new_list, state)
                            set_total_movements(self._grid, new_list)
                            self.check_for_solution(state)
                            break

                    # if (tuple(new_list) in self._visited and self._visited[tuple(new_list)] > current_steps) or tuple(new_list) not in self._visited:
                    #     break

            # check whether the algorithm reached a new state, otherwise take a step back
            state = self.check_for_new_state(state)


        return self.pick_best_solution()
