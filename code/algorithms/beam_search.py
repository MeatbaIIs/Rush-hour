"""
Runs a beam search on a Rush hour puzzle. 
Heuristic: instead of saving all possible moves, it only saves one (of the) move(s) with the furthest distance.
           solutions might not be the best solution, but the algorithm works faster than the original breadth first.
How to use:
-   first load the grid with the initial state, using the loader function:
    grid = loader(input_file_name)
-   then use the algorithm to get a solution:
    beam_search = BeamSearch(grid)
    solution = beam_search.run()
Puzzle 1: around 0.0 minutes, solution of 21 steps
Puzzle 2: around 0.0 minutes, solution of 15 steps
Puzzle 3: around 0.02 minutes, solution of 33 steps
Puzzle 4: around 1 minutes, solution of 28 steps
Puzzle 5: stopped after more than 10 minutes
Puzzle 6: 
"""

from .breadth_first import BreadthFirst


class BeamSearch(BreadthFirst):
    def __init__(self, grid):
        print("Running Beam Search")
        super().__init__(grid)

    def get_next_lists(self, last_list):
        return self._grid.furthest_next_lists(last_list)
