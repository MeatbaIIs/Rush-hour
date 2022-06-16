"""
Visualize a solution to a Rush hour puzzle
Usage: visualization.py solution_file_name
"""
import argparse
import re
import matplotlib.pyplot as plt
from csv import reader
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import random


def main(solution_file_name, steps):
    # Get puzzle
    puzzle_name = solution_file_name.rstrip("_solution.csv") + ".csv"

    # Get puzzle size
    size = int(re.search(
        "Rushhour.+x", puzzle_name).group().lstrip("Rushhour").rstrip("x"))

    # Visualize initial state
    state = [[0] * size for i in range(0, size)]
    color = 0
    cars = {}

    # Load cars
    with open(puzzle_name, 'r') as f:
        file_reader = reader(f)
        next(file_reader)
        for line in file_reader:
            color += 1
            name = line[0]
            car_dict = {
                'name': line[0],
                'orientation': line[1],
                'x': int(line[2]) - 1,
                'y': int(line[3]) - 1,
                'len': int(line[4]),
                'color': color
            }
            cars[name] = car_dict

    # Load initial state
    for car in cars.values():
        if car['orientation'] == 'H':
            for j in range(car['x'], car['x'] + car['len']):
                state[car['y']][j] = car['color']
        else:
            for j in range(car['y'], car['y'] + car['len']):
                state[j][car['x']] = car['color']

    # Make custom color map
    colors_list = [(1, 1, 1)]
    for i in range(color-1):
        hsv = (i/color, 1, random.randrange(7, 11)/10)
        rgb = hsv_to_rgb(hsv)
        colors_list.append(rgb)
    colors_list.append((1, 0, 0))
    custom_colors = ListedColormap(colors_list)

    # Visualize steps
    fig, ax = plt.subplots()
    ims = [[ax.imshow(state, cmap=custom_colors, animated=True)]]

    with open(solution_file_name, 'r') as f:
        file_reader = reader(f)
        next(file_reader)
        step = 0
        for line in file_reader:
            step += 1
            car = cars[line[0]]
            distance = int(line[1])

            if car['orientation'] == 'H':

                for j in range(car['x'], car['x'] + car['len']):
                    state[car['y']][j] = 0

                car['x'] += distance

                for j in range(car['x'], car['x'] + car['len']):
                    state[car['y']][j] = car['color']

            else:

                for j in range(car['y'], car['y'] + car['len']):
                    state[j][car['x']] = 0

                car['y'] += distance

                for j in range(car['y'], car['y'] + car['len']):
                    state[j][car['x']] = car['color']

            if step < steps:
                im = ax.imshow(state, cmap=custom_colors, animated=True)
                ims.append([im])
    ani = animation.ArtistAnimation(
        fig, ims, interval=200, blit=True, repeat_delay=2000)

    output_file_name = solution_file_name.rstrip('.csv') + ".gif"
    ani.save(output_file_name, writer=animation.PillowWriter(fps=2))

    plt.show()


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")
    parser.add_argument("-s",
                        "--steps", type=int, default=200, help="maximum amount of steps/frames to visualize (default: 200)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input, args.steps)
