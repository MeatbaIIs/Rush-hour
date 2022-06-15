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
        # make a copy of the total displacement of every car in the grid
        # the dictionary is {A:0, B:0, ... , X: 0} at the start
        self._movement_nodes = [copy.deepcopy(self._grid._total_movements)]
        self._current_node = copy.deepcopy(self._grid._total_movements)

        # keep remembering the previous node
        self._previous_node = copy.deepcopy(self._current_node)

        # remember the exact moves that have been done for the current node
        # dit is bijvoorbeeld [A 1, X -2, B 3, G 1, H -1, etc...]
        self._done_movements = []

        self._n_backtracks = 0

    """
    Function that does a step in the depth first algorithm. It calculates all possible nodes (grids in Rushhour)
    from the current possible moves and then takes a random possible move.
    If there are no possible moves because the next nodes are already saved in the database we go back a step
    If the grid is a win condition we set that as the maximum length of steps to look at
    """
    def step(self):
        # check what the moves possible are from the current grid node
        possible_moves = self._grid.poss_move_cars()
        # print(f"possible_moves before node checking are {possible_moves}")

        # update what the possible grid configurations are when considering the possible moves and return remaining possible moves
        possible_moves = self.update_nodes(possible_moves)
        # print(f"after nodes is {possible_moves}")

        # check that there are still moves possible
        if possible_moves:
            # make a copy of the current node and update the next node
            self._previous_node = copy.deepcopy(self._current_node)

            # get a random car that moves with a random distnace
            car_name = random.choice(list(possible_moves.keys()))
            distance = random.choice(possible_moves[car_name])

            # change the current grid and the node configuration
            print(f"{car_name} is moving a distance {distance}")
            self._grid.move(car_name, distance=distance)

            # update the current node
            new_node = copy.deepcopy(self._current_node)
            new_node[car_name] += distance
            self._current_node = new_node
            print(f"current node is {self._current_node}")
            
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

                print(f"{car_name} is moving back with distance {distance}")

                # move the previous car backwards!
                self._grid.move(car_name, - distance)
                
                self._fut_prev_node = copy.deepcopy(self._previous_node)

                # change the grid node so that the car moved back aswell
                self._fut_prev_node[car_name] -= distance

                # change the current and previous nodes accordingly
                self._current_node = copy.deepcopy(self._previous_node)
                print(f"current node after backwards is {self._current_node}")
                self._previous_node = copy.deepcopy(self._fut_prev_node)

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
            for i in range(len(possible_moves[car_name])):
                iterator = 0
                distance = possible_moves[car_name][iterator]
                # deepcopy as to not destroy current dictionary of moves and update what it would be when moved
                future_node = copy.deepcopy(self._current_node)
                future_node[car_name] += distance
                # print(f"were comparing dictionary {future_node} with move {car_name} {distance}")

                # # check that the future node is not already in the list or remove the possible movement
                # for dic in self._movement_nodes:
                #     # print(dic)
                #     if future_node == dic:
                #         # print(f"same")
                #         break
                
                if dict_compare(future_node, self._movement_nodes) == True:
                    
                    # if multiple movements are possible for one car just remove the distance that has been moved before
                    if len(possible_moves[car_name]) > 1:
                        # print(f"deleting distance {distance} from car {car_name}")
                        possible_moves[car_name].remove(distance)
                    # if no movements for the car allowed, remove entire key
                    else:
                        # remove the possible move from the dict of possible moves
                        # print(f"deleting {car_name}")
                        del possible_moves[car_name]
                    # free the deepcopy memory
                    # del future_node
                # if it's a new possible grid configuration save it to all possible grids
                else:
                    self._movement_nodes.append(future_node)
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
        for i in range(20):
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
            
    
