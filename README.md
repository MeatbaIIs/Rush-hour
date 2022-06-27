# Rush-hour
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

"""
Runs a breadth first algorithm on a Rush hour puzzle.
How to use:
-   first load the grid with the initial state, using the loader function:
    grid = loader(input_file_name)
-   then use the algorithm to get a solution:
    breadth_first = BreadthFirst(grid)
    solution = breadth_first.run()
Puzzle 1: around 0.0 minutes, solution of 21 steps
Puzzle 2: around 0.01 minutes, solution of 15 steps
Puzzle 3: around 0.03 minutes, solution of 33 steps
Puzzle 4: around 2,5 minutes, solution of 27 steps
Puzzle 5: killed
Puzzle 6: killed
"""