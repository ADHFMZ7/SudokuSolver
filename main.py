#!/opt/anaconda3/envs/sudoku/bin/python3
from sudoku.board import *

board = Board()

for i in range(15):
    board.solve_puzzle()
