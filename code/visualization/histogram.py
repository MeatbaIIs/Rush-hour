from code.helpers import loader, batchrunner
from matplotlib import pyplot as plt
import numpy

"""
Get a histogram for all methods for a certain filename after batchrunning N times
"""
def histogram_and_plot(file_name, N):
    # give strings for the current differen methods, more can be added
    # this is the way they needed to be loaded in batchrunner
    different_methods = ["DF", "BF", "BFF", "MaxRandom", "Random"]
    total_moves = []
    total_coords = []

    # binsize can be adjusted here
    bins = numpy.linspace(0, 1000, 10)

    # loop over the methods and batchrun for the file, then save 
    for method in different_methods:
        # get the moves, movement list 
        moves, movement_list, times = batchrunner(file_name, method, N)
        total_moves.append(moves)
        # get the smallest number of moves required of the entire batchrun for the method
        print(f"{min(moves)} is least number of moves for method {method}")

        # save the sub histograms
        plt.hist(moves, bins, alpha=0.5, label=method)
        # save total coords to make plots later
        total_coords.append((moves, times))

    name = file_name.rstrip(".csv")
    # plot the entire histogram and save it to data 
    plt.legend(loc='upper right')
    plt.savefig(file_name.rstrip(".csv") + f"_{N}_histogram.png")
    plt.xlabel("Number of moves needed")
    plt.ylabel("Counts")
    plt.title(f"Histogram of number of moves needed to solve {name} {N} times for different methods")
    plt.show()

    fig = plt.figure()
    # add more colors if there are more methods!
    colors = ['r', 'b', 'g', 'c', 'm']
    # loop over the time-move coordinates generated per method batchrun
    for i in range(len(total_coords)):
        times = total_coords[i][1]
        moves = total_coords[i][0]
        # make a scatterplot
        plt.scatter(x=times, y=moves, color = colors[i], alpha=0.5, label = different_methods[i])
    
    plt.legend(loc='upper right')
    
    plt.xlabel("Time t")
    plt.ylabel("Number of moves")
    # plot logarithmic because of random steps
    plt.yscale("log")
    plt.title(f"Time and move scatterplot of number of moves needed to solve {name} {N} times for different methods")
    plt.savefig(file_name.rstrip(".csv") + f"_{N}_move_time_plot.png")
    plt.show()

    
    
