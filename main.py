#!/opt/anaconda3/envs/sudoku/bin/python3
from sudoku.board import *

for i in range(25):
    grid = collect()
    result = solver(grid)
    fill(result)
    driver.find_element_by_name('submit').click()
