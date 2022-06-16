"""
Anneloes'en Duncans wondercode
"""
import copy
from dis import dis
from math import dist
from matplotlib.pyplot import cla
from code.classes.grid import Grid
from code.helpers import loader, dict_compare
import random
import time

class DepthFirst:
    def __init__(self, data_file) -> None:
        grid = loader(data_file)
        self._grid = grid

        # load the first grid configuration as a function of how many steps each car has
        # moved from the starting position
        self._current_configuration = {}
        for car_name in self._grid._cars:
            self._current_configuration[car_name] = 0

        # the dictionary is {A:0, B:0, ... , X: 0} at the start
        self._grid_configurations = [copy.deepcopy(self._current_configuration)]
        
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
        print(f"possible_moves before node checking are {possible_moves}")

        # check which configurations we already have before we start updating the nodes
        for config in self._grid_configurations:
            print(config)

        # calculates the grid configurations for the possible moves
        # also remove possible moves when the grid configuration is already in the list of movement nodes
        possible_moves = self.update_nodes(possible_moves)
        print(f"after nodes is {possible_moves}")

        # check that there are still moves possible
        if possible_moves:
            # get a random car that moves with a random distnace
            car_name = random.choice(list(possible_moves.keys()))
            distance = random.choice(possible_moves[car_name])

            # change the current grid and the node configuration
            print(f"{car_name} is moving a distance {distance}")
            self._grid.move(car_name, distance=distance)

            # update the current node
            new_node = copy.deepcopy(self._current_configuration)
            new_node[car_name] += distance
            self._current_configuration = new_node
            print(f"current node is {self._current_configuration}")
            
            self._grid.print_grid()

            
            # keep track of whih movents have been done
            self._done_movements.append([car_name, distance])
        
        # if there are no possible movements, go back to a previous node untill 
        # there are movements possible again
        else: 
            if len(self._done_movements) == 0:
                print("no further movements possible")
            else:
                # move back the last done movement
                car_name, distance = self._done_movements[-1]
                # move the previous car backwards!
                self._grid.move(car_name, - distance)

                print(f"{car_name} is moving back with distance {distance}")

                # change the current and previous nodes accordingly
                previous_node = copy.deepcopy(self._current_configuration)
                previous_node[car_name] -= distance
                self._current_configuration = previous_node
                
                # remove the last move from the movements as we returned
                self._done_movements.pop()
                self._n_backtracks += 1
    
    """
    Function to update the upcoming dict nodes of the grid configurations based on current possible moves
    also gives the moves that are possible after checking if the nodes already existed
    """
    def update_nodes(self, possible_moves):
        # loop over all values in every cars possible movement
        for car_name in list(possible_moves.keys()):
            # loop over the possible distances per car
            for i in range(len(possible_moves[car_name])):
                iterator = 0
                distance = possible_moves[car_name][iterator]
                # deepcopy as to not destroy current dictionary of moves and update what it would be when moved

                future_node = copy.deepcopy(self._current_configuration)
                future_node[car_name] += distance
                new_node = True
                
                # if dict_compare(future_node, self._grid_configurations) == True:
                for known_dicts in self._grid_configurations:
                    if known_dicts == future_node:
                        new_node = False
                        print(f"for {car_name} {distance} were comparing dictionary {known_dicts} with move {future_node}")
                        # if multiple movements are possible for one car just remove the distance that has been moved before
                        if len(possible_moves[car_name]) > 1:
                            print(f"{car_name} has {len(possible_moves[car_name])} moves and removing {distance}")
                            # print(f"deleting distance {distance} from car {car_name}")
                            possible_moves[car_name].remove(distance)
                        # if no movements for the car allowed, remove entire key
                        else:
                            # remove the possible move from the dict of possible moves
                            print(f"deleting entire key {car_name} from possible moves")
                            del possible_moves[car_name]
                        break

                # if it's a new possible grid configuration save it to all possible grids
                if new_node == True:
                    self._grid_configurations.append(future_node)
                    # if no value is removed we iterate to the next dict item
                    iterator += 1

        return possible_moves

    """
    Run the code until the grid is won
    """
    def run(self):
        step_number = 0
        t = time.time()
        # while self._grid.win() == False:
        for i in range(10):
            print(f"step is {step_number}")
            self.step()
            step_number += 1
        self._grid.print_grid()
        
        print(f"Yay, solved in {step_number} steps and {time.time() - t} seconds, while taking {len(self._done_movements)}")
        print(self._done_movements, self._n_backtracks)

# bugs zijn de movements na terug gaan
# ook runt die soms oneindig
# dus er worden teveel random gekke borden gecreeerd!!
# gebruik zo print grid
            
    
