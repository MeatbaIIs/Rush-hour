import copy
from .breadth_first import BreadthFirst
import queue
import random


class BreadthFirstIter(BreadthFirst):
    def __init__(self, grid, solution):
        self._grid = grid
        self._given_solution = solution
        self._car_indexes = {}
        for i, name in enumerate(self._grid.get_car_names()):
            self._car_indexes[name] = i

        self._solution_states = []
        self._solution_states.append(tuple([0 for i in self._car_indexes]))
        self._counter = 0

    def load_solution(self):

        for car, distance in self._given_solution:
            car_index = self._car_indexes[car]
            new_state = list(copy.deepcopy(self._solution_states[-1]))
            new_state[car_index] += distance
            self._solution_states.append(tuple(new_state))

        return

    def breadth_first_iteration(self, sequence_to_improve):
        start_state = sequence_to_improve[0]
        end_state = sequence_to_improve[-1]

        bf_queue = queue.Queue()
        bf_queue.put([start_state])
        visited = set()
        visited.add(start_state)

        while not bf_queue.empty():

            seq = bf_queue.get()
            # print(f'{bf_queue.qsize()}')

            if seq[-1] == end_state:
                # print('found optimization')
                self._counter += 1
                return seq

            if len(seq) >= len(sequence_to_improve):
                # print('didnt find it')
                return sequence_to_improve

            last_state = seq[-1]

            for new_state in self._grid.possible_next_lists(list(last_state)):
                new_state = tuple(new_state)
                if new_state in visited:
                    continue

                visited.add(new_state)
                child = copy.deepcopy(seq)
                child.append(new_state)
                bf_queue.put(child)

    def run(self):
        """  """
        self.load_solution()

        for index in range(len(self._solution_states)-7):
            print(index)
            # index = random.randrange(len(self._solution_states)-7)
            seq = self._solution_states[index:index+7]
            opt_seq = self.breadth_first_iteration(seq)
            self._solution_states = self._solution_states[:index] + \
                opt_seq + self._solution_states[index+7:]

        print(f'Found {self._counter} optimizations.')
        return self.solution_list_to_steps(self._solution_states)
