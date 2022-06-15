"""
Code to make histograms from codes and alogrithms to dertemine what a feasable upper bound for the number of steps is

"""

from code.helpers import loader
from matplotlib import pyplot as plt
from code.algorithms.random import Random
import copy

def histogram(file_name):
    #file_name = "data/Rushhour6x6_1.csv"
    grid = loader(file_name)
    grid.print_grid()

    N = 1000
    print(f"going to solve previous grid {N} times")

    counts = []
    # counts_2 = []

    for i in range(N):
        # grid = loader(file_name)
        gridcopy = copy.deepcopy(grid)
        algorithm = Random(gridcopy)

        tries = algorithm.random_algorithm()
        # grid = loader(file_name)
        # algorithm = Random(grid)
        # tries_2 = algorithm.other_random_algorithm()
        counts.append(tries)
        # counts_2.append(tries_2)
        if i % 10== 0:
            print(i)

    fig, ax = plt.subplots(figsize =(10, 7))
    ax.hist(counts, bins=100)
    print(min(counts))
    plt.show()
    plt.savefig("histogram_random.png")
