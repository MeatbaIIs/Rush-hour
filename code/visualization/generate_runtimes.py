from code.algorithms.beam_search import BeamSearch as BS
from code.algorithms.breadth_first import BreadthFirst as BF
from code.algorithms.depth_first import DepthFirst as DF
from code.algorithms.random import Random
from code.helpers import loader, solution_to_csv, check_filename, ask_for_solution, load_solution
from copy import deepcopy
import matplotlib.pyplot as plt

import time



def generate_runtimes(input_filename, output_filename):
    solution_name = []
    runtimes = []
    grid = loader(input_filename)

    # try except to catch memory errors, name gets edited to failed
    try:
        start_time = time.perf_counter()
        algorithm = BF(deepcopy(grid))
        solution = algorithm.run()
        end_time = time.perf_counter()
        runtimes.append(end_time - start_time)
        solution_name.append("BreadthFirst")

    except MemoryError:
        runtimes.append(0)
        solution_name.append("BreadthFirst_failed")

    try:
        start_time = time.perf_counter()
        algorithm = BS(deepcopy(grid))
        solution = algorithm.run()
        end_time = time.perf_counter()
        runtimes.append(end_time - start_time)
        solution_name.append("BeamSearch")

    except MemoryError:
        runtimes.append(0)
        solution_name.append("BeamSearch_failed")

    try:
        start_time = time.perf_counter()
        algorithm = DF(deepcopy(grid))
        solution = algorithm.run("optimal")
        end_time = time.perf_counter()
        runtimes.append(end_time - start_time)
        solution_name.append("DepthFirst")

    except MemoryError:
        runtimes.append(0)
        solution_name.append("DepthFirst_failed")

    # try except to be consequent
    try:
        start_time = time.perf_counter()
        algorithm = Random(deepcopy(grid))
        solution = algorithm.run("random")
        end_time = time.perf_counter()
        runtimes.append(end_time - start_time)
        solution_name.append("Random")

    except MemoryError:
        runtimes.append(0)
        solution_name.append("Random_failed")


    fig, ax = plt.subplots()

    ax.bar(solution_name, runtimes)
    plt.savefig(output_filename)
    plt.show()

if __name__ == "__main__":
    generate_runtimes("data/Rushhour6x6_1.csv")
