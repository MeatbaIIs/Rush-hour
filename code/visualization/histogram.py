"""
Code to make histograms from codes and alogrithms to dertemine what a feasable upper bound for the number of steps is

"""

from helpers import loader
from matplotlib import pyplot as plt


file_name = "data/Rushhour12x12_7.csv"
grid = loader(file_name)
grid.print_grid()

N = 100
print(f"going to solve previous grid {N} times")

counts = []
counts_2 = []

for i in range(N):
    grid = loader(file_name)
    tries = grid.random_algorythm()
    tries_2 = grid.other_random_algorithm()

    counts.append(tries)
    counts_2.append(tries_2)

fig, ax = plt.subplots(figsize =(10, 7))
ax.hist(counts, bins=20)
plt.show()

