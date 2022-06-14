


class Random():
    def __init__(self, grid):
        self._grid = grid

    def random_algorythm(self):
        """Move a random car randomly and check for the win condition"""
        random_car = random.choice(list(self._cars.keys()))

        steps = 0
        # t = time.time()
        while not self.win():
            # get the possible moves and pick a random one
            moves = self.possible_moves(random_car)

            if moves:
                steps += 1
                random_move = random.choice(moves)
                self.move(random_car, random_move)
            # pick a new random car
            random_car = random.choice(list(self._cars.keys()))
        # print(f"Yay, solved in {steps} steps and {time.time() - t} seconds")

        return steps
    def other_random_algorithm(self):
        iterator = 0
        while self.win() == False:
            list_of_empties = self.give_empties()
            empty = random.choice(list_of_empties)
            possible_moves = self.movable_neighbours(empty[0], empty[1])

            if len(possible_moves) != 0:
                moving_car = random.choice(list(possible_moves.keys()))
                car_name, car_distance = possible_moves[moving_car]

                self.move(car_name, car_distance)
                iterator += 1

        self.print_grid()
        print(f"we have won after {iterator} moves")

    def random_step(self):
        """Move a random car randomly and check for the win condition"""
        # auto's uit het
        cars = self._cars
        moves = []

        while not moves:
            random_car = random.choice(list(cars.keys()))
            moves = self.possible_moves(random_car)

        random_move = random.choice(moves)
        self.move(random_car, random_move)
        return random_car + ',' + str(random_move)
