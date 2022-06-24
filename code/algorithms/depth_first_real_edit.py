from code.classes.grid import Grid
from copy import deepcopy
from copy import copy
#import stack


# misschien overerven van breadth first
class Depth_first():
    def __init__(self, grid, best_solution = float('inf'), solutions = []):
        self._initial_grid = deepcopy(grid)
        self._grid = deepcopy(grid)
        self._empty_grid = []
        self._stack = []
        for _ in range(grid.get_size()):
            self._empty_grid.append(grid.get_size() * ['*'])#deepcopy(grid.get_grid())

        self._grid = grid
        self._cars = grid.get_car_names()
        self._initial_x = {}
        self._initial_y = {}
        self._orientation = {}
        self._lengths = {}
        self._visited = {}
        self._empty_state = {}
        self._last_car = ""
        # Make dictionaries with info about all cars on the given grid
        for name in self._cars:
            self._empty_state[name] = 0
            self._initial_x[name] = grid.get_car_x(name)
            self._initial_y[name] = grid.get_car_y(name)
            self._orientation[name] = grid.get_car_orientation(name)
            self._lengths[name] = grid.get_car_length(name)


        #self._queue.put([[0 for i in range(len(self._cars))]])
        self._stack.append([[0 for i in range(len(self._cars))]])
        self._visited[tuple([0 for i in range(len(self._cars))])] = 0
        self._len_visited = [0]
        for solution in solutions:
            for i, state in enumerate(solution):
                self._visited[tuple(state)] =  i
        self._solutions = solutions
        self._best_solution = best_solution

    def possible_next_lists(self, current_list):
        """ Gives the possible lists after one move on the grid that can be made with the given list """

        # Write the list to a grid and set this as current grid.

        grid = self.list_to_grid(current_list)
        self._grid.set_grid(grid)
        next_lists = []

        # For each car see what moves are possible
        for i, car in enumerate(self._cars):


            moves = self._grid.possible_moves(car)

            if moves and max(moves) > 0:
                distance = max(moves)
                next_list = copy(current_list)
                next_list[i] += distance
                next_lists.append(next_list)

            if moves and min(moves) < 0:
                distance = min(moves)
                next_list = copy(current_list)
                next_list[i] += distance
                next_lists.append(next_list)


        return next_lists


    def route_to_state(self, route):
        state = copy(self._empty_state)
        for move in route:
            car = move[0]
            distance = move[1]
            state[car] = distance

        return state

    def list_to_grid(self, current_list):
        """ Given a list with the total moved distance from the start position for each car, draws a list of lists that represents the grid """
        grid = deepcopy(self._empty_grid)

        # Add cars
        # Add cars
        for i, car  in enumerate(self._cars):
            x = self._initial_x[car]
            y = self._initial_y[car]
            length = self._lengths[car]

            if self._orientation[car] == 'H':
                x += current_list[i]
                for j in range(length):
                    grid[y][x + j] = car
            else:
                y += current_list[i]
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

    def remove_long_visited(self, visited_keys, length):
        for key in visisted_keys:
            if self._visited[key] > length:



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
        """
        TO DO:
        Check of de stack goed aangevuld wordt
        Misschien alleen code van breadth_first gebruiken (hooguit 6 stappen)
        zorg dat de oplossingen opgeslagen worden
        Zorg dat vorige states opgeslagen worden
        """

        current_list = deepcopy(self._empty_state)
        current_route = []
        runs = 0

        while self._stack:
            # self._new_state = False
            #print(len(self._stack))
            state = self._stack.pop()
            #print(self._stack)
            if self.is_solution(state):
                print('found a solution of ' + str(len(state)) + ' steps.')
                solution = self.solution_list_to_steps(state)
                self._solutions.append(state)
                self._best_solution = len(state)
                # print(self._stack)

            if self._grid.win():
                print("won")


            # pak de laatste configuratie van
            last_list = state[-1]
            # werkt niet
            self._new_state = False

            if len(state) < self._best_solution - 1:

                # ga elke mogelijke volgende stap af
                # for new_list in self.possible_next_lists(last_list):

                visited_keys = set(self._visited.keys())

                current_steps = len(state)

                for i, car in enumerate(self._cars):
                    for move in self._grid.possible_moves():

                        # make a copy of the last list to add a move
                        new_list = copy(last_list)

                        # get the maximum move
                        if move == max(move) and move > 0:
                            new_list[i] += move

                        elif move = min(move) and move < 0:
                            new_list[i] += move

                        if tuple(new_list) in visited_keys and self._visited[tuple(new_list)] < current_steps:
                            continue

                        # # als deze configuratie  al een keer bereikt is en hij deze keer niet sneller is dan de vorige keer slaan we hem over
                        if tuple(new_list) in visisted_keys and self._visited[tuple(new_list)] > current_steps:

                            # als hij deze wel sneller doet kan het zijn dat die state al in een vorige oplossing is gevonden, als dit zo is is dit een snelleren oplossing
                            for i, solution in enumerate(self._solutions):
                                for j, config in enumerate(solution):
                                    if new_list == config:
                                        solution[:j] = state + [new_list]
                                        if len(solution) < self._best_solution:
                                            self._best_solution = len(solution)
                                            print(f'found solution of {len(solution)} steps')
                                            solution = self.solution_list_to_steps(solution)

                        self._new_state = True
                        self._visited[tuple(new_list)] = len(state) - 1#.append(new_list)
                        child = deepcopy(state)
                        child.append(new_list)
                        self._stack.append(child)

                        #werkt niet
                        break

            #werkt niet
            if not self._new_state and len(state) > 1:
                state.pop()
                self._stack.append(state)


        return solution
