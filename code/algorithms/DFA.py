"""
Anneloes'en Duncans wondercode
"""
import copy
from dis import dis
from math import dist
from shutil import move
from matplotlib.pyplot import cla, step
from code.classes.grid import Grid
from code.helpers import loader, dict_compare
import random
import time

class DepthFirst:
    def __init__(self, data_file) -> None:
        grid = loader(data_file)
        self._grid = grid

        self._win_max = 1000
        # load the first grid configuration as a function of how many steps each car has
        # moved from the starting position
        self._current_configuration = {}
        for car_name in self._grid._cars:
            self._current_configuration[car_name] = 0

        # the dictionary is {A:0, B:0, ... , X: 0} at the start
        self._visited_configurations = [copy.deepcopy(self._current_configuration)]
        
        # remember the exact moves that have been done for the current node
        # dit is bijvoorbeeld [A 1, X -2, B 3, G 1, H -1, etc...]
        self._done_movements = []

        # calculate how many times 
        self._n_backtracks = 0

    """
    Function that does a step in the depth first algorithm. It calculates all possible nodes (grids in Rushhour)
    from the current possible moves and then takes a random possible move.
    If there are no possible moves because the next nodes are already saved in the database we go back a step
    """
    def step(self):
        # check what the moves possible are from the current grid node
        possible_moves = self._grid.poss_move_cars()
        # print(f"possible_moves before checking configs {possible_moves}")

        # checks if the possible moves go to visited configurations or and removes them
        possible_moves = self.update_nodes(possible_moves)
        # print(f" possible moves after checking configs is {possible_moves}")

        # move backwards if there are no possible moves or if the current state moves beyond
        # a preset maximum moves
        if not possible_moves or len(self._done_movements) > self._win_max:
            # move back the last done movement
            car_name, distance = self._done_movements[-1]
            # move the previous car backwards!
            self._grid.move(car_name, - distance)

            # change the current and previous nodes accordingly
            previous_config = copy.deepcopy(self._current_configuration)
            previous_config[car_name] -= distance
            self._current_configuration = previous_config
            
            # remove the last move from the movements as we returned
            self._done_movements.pop()
            self._n_backtracks += 1
        # make a random move if other moves are possible
        else:
            # get a random car that moves with a random distnace
            car_name = random.choice(list(possible_moves))
            distance = random.choice(possible_moves[car_name])

            # change the current grid and the node configuration
            # print(f"{car_name} is moving a distance {distance}")
            self._grid.move(car_name, distance=distance)
            

            # update the current node
            new_node = copy.deepcopy(self._current_configuration)
            new_node[car_name] += distance
            self._current_configuration = new_node
            # add to visited nodes
            self._visited_configurations.append(self._current_configuration)
            # print(f"current node is {self._current_configuration}")
            
            self._grid.print_grid()
            
            # keep track of whih movents have been done
            self._done_movements.append([car_name, distance])
        
        # if there are no possible movements, go back to a previous node untill 
        # there are movements possible again
        


    """
    Function to update the upcoming dict nodes of the grid configurations based on current possible moves
    also gives the moves that are possible after checking if the nodes already existed
    """
    def update_nodes(self, possible_moves):
        # make a dictionary of the next possible moves
        move_dict = {}
        # loop over all the movable cars
        for car_name in list(possible_moves):
            move_dict[car_name] = []
            car_movement_list = move_dict[car_name]
       
            # loop over the possible distances per car
            for distance in possible_moves[car_name]:
                
                # deepcopy as to not destroy current dictionary of moves and update what it would be when moved
                future_node = copy.deepcopy(self._current_configuration)
                future_node[car_name] += distance
                # keep track if a new config can be made when the car moves with this distance
                new_config = True

                # if dict_compare(future_node, self._grid_configurations) == True:
                for known_dicts in self._visited_configurations:
                    if known_dicts == future_node:
                        new_config = False
                        # print(f"{car_name} {distance} is in the known configurations")

                # if it's a new possible grid configuration allow the movement to be possible
                if new_config == True:
                    car_movement_list.append(distance)
            
            # delete the empty list if there are no movements possible
            if len(car_movement_list) == 0:
                del move_dict[car_name]

        return move_dict

    """
    Run the code until the grid is won
    """
    def run(self):
        step_number = 0
        t = time.time()
        while self._grid.win() == False:
            step_number += 1
            self.step()
        
        self._grid.print_grid()
        print(f"Yay, solved in {step_number} steps and {time.time() - t} seconds, while taking {len(self._done_movements)}")
        # return
        # state a maximum number of moves that are allowed
        self._win_max = len(self._done_movements)
        self._first_win = self._win_max
        self._min_win_moves = self._done_movements

        step_number_2 = 0
        # update the max allowed steps when another win is detected
        t = time.time()
        while self._done_movements:
            self.step()
            step_number_2 += 1
            if self._grid.win():
                self._win_max = len(self._done_movements)
                self._min_win_moves = self._done_movements
                print(self._win_max, self._min_win_moves)
                
                
        
        print(f"Yay, solved in {step_number_2} steps and {time.time() - t} seconds, while taking {self._win_max}")
        print(self._first_win, self._win_max)


# bugs zijn de movements na terug gaan
# ook runt die soms oneindig
# dus er worden teveel random gekke borden gecreeerd!!
# gebruik zo print grid
            
    
