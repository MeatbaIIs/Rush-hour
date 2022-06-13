"""
Initialize a grid with the Rush Hour puzzle given as command line argument, solve the puzzle, and visualize the solution.
Usage: loader.py [PUZZLE_NAME.CSV]
"""

import time
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import csv
from grid import Grid
import argparse
import re


def main(input_file_name):
    # Get grid size from the input file name
    size = re.search(
        "Rushhour.+x", input_file_name).group().lstrip("Rushhour").rstrip("x")

    # Load grid
    grid = Grid(int(size))

    # Load cars in the grid
    with open(input_file_name) as f:

        # Skip over first line
        f.readline()

        while True:
            line = f.readline().strip().split(",")

            if line == [""]:
                break

            grid.add_car(line[0], line[1], int(line[2]) - 1,
                         int(line[3]) - 1, int(line[4]))

    # grid.print_grid()
    # grid.give_empties()
    # print("doing all possible moves")
    # grid.give_all_possible_moves()

    #grid.neighbours(1, 1)
    # grid.possible_cars(3, 4)

    # grid.print_grid()

    # start_time = time.time()
    # grid.other_random_algorithm()
    # print("--- %s seconds ---" % (time.time() - start_time))

    # grid.possible_cars(3, 4)
    # grid.random_algorythm()

    # Set up figure
    # fig, ax = plt.subplots(figsize=(10, 10))
    # ims = []

    # colors_list = []
    # for i in range(100):
    #     r = 0.3 + i*0.6/100
    #     g = 0.7 - i*0.4/100
    #     b = 0.9 - i*0.45/100
    #     colors_list.append((r, g, b))
    # custom_colors = ListedColormap(colors_list)

    # names = []
    # x_pos = []
    # y_pos = []

    # for car in grid._cars.values():
    #     for i in range(car._length):
    #         names.append(car._name)
    #         if car._orientation == 'H':
    #             x_pos.append(car._x + i)
    #             y_pos.append(car._y)
    #         else:
    #             x_pos.append(car._x)
    #             y_pos.append(car._y + i)
    # ax.scatter(x_pos, y_pos, marker="s", s=200, cmap=custom_colors)

    # plt.imshow(grid._grid)
    # plt.show()
    # Find solution and output solution to csv file
    filename = input_file_name.rstrip(".csv") + "_solution.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['car', 'move'])

        while not grid.win():
            # ord
            # Visualize one frame
            # names = []
            # x_pos = []
            # y_pos = []

            # for car in grid._cars.values():
            #     for i in range(car._length):
            #         names.append(car._name)
            #         if car._orientation == 'H':
            #             x_pos.append(car._x + i)
            #             y_pos.append(car._y)
            #         else:
            #             x_pos.append(car._x)
            #             y_pos.append(car._y + i)
            # im = ax.scatter(x_pos, y_pos, marker="s",
            #                 s=200, cmap=custom_colors)
            # ims.append([im])

            # Take step in algorith
            step = grid.random_step()

            # Write step to csv
            csvwriter.writerow(step.split(","))

    # ani = animation.ArtistAnimation(
    #     fig, ims, interval=50, blit=True, repeat_delay=1000)
    # output_file_name = input_file_name + ".gif"
    # ani.save(output_file_name, writer=animation.PillowWriter(fps=24))

    print("found a solution!")


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
