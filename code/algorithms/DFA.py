"""
Anneloes'en Duncans wondercode
"""
import copy
from matplotlib.pyplot import cla
from ..classes.grid import Grid
from helpers import loader

class DepthFirst:
    def __init__(self, data_file) -> None:
        grid = loader(data_file)

        self._grid = grid
        # make a copy of the current total moves, where the lst number in the list is the number of steps
        self._movement_nodes = [grid._total_moves[:]]
        self._current_node = grid._total_moves[:]

        # last number of the total movements is the number of steps
        self._N_steps = self._current_node[-1]

        # keep remembering the previous node
        self._previous_node = self._current_node

        # remember the exact moves that have been done for the current node
        self._done_movements = []


    # """
    # pseudocode for the steps
    # """"
    # def step(self):
    #     # this is for the next nodes when starting at a certain point
    #     moves = self.grid.possible_moves()

    #     berekent voor alle mogelijke moves wat de total moves zouden zijn als we naar die node zouden bewegen
    #     for move in moves:
    #         current_node + move
    #         movement_nodes.append(node)
        
    #     self.previous_node = self.current_node
    #     self.grid.move(random.choice van moves)
    #     self.current_node = self.grid._total_movements

    #     if self._current_node in self.movement_nodes:
    #         self.movement_nodes.pop(self.current_node)

    #         self.current_node.move(laatste element in de gedane stappen)
    #         self.previous_node.move(laatste en enalaatste element in de gedane stappen)


        
    

    def run(self):
        # loopt tot de grid opgelost is
        while not win:
            self.step()
    

algorithm = DepthFirst("data/Rushhour6x6_1.csv")
algorithm.step()