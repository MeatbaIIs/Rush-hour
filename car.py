class Car():
    def __init__(self, name, orientation, x, y, length, grid_size) -> None:
        self._name = name
        self._orientation = orientation
        self._x = x
        self._y = y
        self._length = length
        # give the columns of the grid for the win condition
        self._grid_size = grid_size

    # gives the coordinates of the car as a list of (x, y)
    def coordinates(self):
        coordinate = [self._x, self._y]

        return coordinate

<<<<<<< HEAD
    def set_coordinates(self, new_x, new_y):
        self._x = new_x
        self._y = new_y
=======
    # returns true if the red car is over the finish line
    def win(self):
        # red car is denoted by X
        if self._name == "X":
            # for i in range(self._x, self._grid_size)
            if self._x == self._grid_size - 1:
                return True
            else:
                return False
        else:
            return False
>>>>>>> 9e4ad599ad0417b6a4a759702df099b0ec5564c5

    # def can_move_to(self, x, y):
    #     """ Check whether the car can move to the given coordinates. """
    #     if
    #     if self._orientation == 'H':

    #         if not self._y == y:
    #             return False

    #         for i in range(self._x + self._length-1, x):
    #             if not i == '*':
    #                 return False
    #         return True

    #     # If the car is vertical
    #     if not self._x == x:
    #         return False

    #     pass
# # possibly a subclass for a red car is quicker as we only loop over 1 car rather than all cars
# # depends on our grid model for checking the win condition
# class RedCar(Car):
#     def __init__(self, name, orientation, col, y, length, grid_size) -> None:
#         super().__init__(name, orientation, col, y, length, grid_size)
