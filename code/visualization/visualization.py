"""
Visualize a solution to a Rush hour puzzle
"""
import re
from csv import reader
from matplotlib.colors import ListedColormap, hsv_to_rgb
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random


def main(solution_file_name, steps, puzzle_name):

    # Get puzzle size
    size = int(re.search(
        "Rushhour.+x", puzzle_name).group().lstrip("Rushhour").rstrip("x"))

    # Visualize initial total_movements
    total_movements = [[0] * size for i in range(0, size)]
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

    # Load initial total_movements
    for car in cars.values():
        if car['orientation'] == 'H':
            for j in range(car['x'], car['x'] + car['len']):
                total_movements[car['y']][j] = car['color']

        else:
            for j in range(car['y'], car['y'] + car['len']):
                total_movements[j][car['x']] = car['color']

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
    ims = [[ax.imshow(total_movements, cmap=custom_colors, animated=True)]]
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # read the solution file name
    with open(solution_file_name, 'r') as f:
        file_reader = reader(f)
        next(file_reader)
        step = 0

        # move cars in order of the solution file
        for line in file_reader:
            step += 1
            car = cars[line[0]]
            distance = int(line[1])

            if car['orientation'] == 'H':

                # remove current position of car
                for j in range(car['x'], car['x'] + car['len']):
                    total_movements[car['y']][j] = 0

                car['x'] += distance

                # add new position for car
                for j in range(car['x'], car['x'] + car['len']):
                    total_movements[car['y']][j] = car['color']

            else:

                # remove current position of car
                for j in range(car['y'], car['y'] + car['len']):
                    total_movements[j][car['x']] = 0

                car['y'] += distance

                # add new position for car
                for j in range(car['y'], car['y'] + car['len']):
                    total_movements[j][car['x']] = car['color']

            # check if the steps dont exceed the maximum step
            if step < steps:
                im = ax.imshow(total_movements,
                               cmap=custom_colors, animated=True)
                ims.append([im])

    # specify animation attributes
    ani = animation.ArtistAnimation(
        fig, ims, interval=200, blit=True, repeat_delay=2000)

    # save the file
    output_file_name = solution_file_name.rstrip('.csv') + ".gif"
    ani.save(output_file_name, writer=animation.PillowWriter(fps=2))

    plt.show()
