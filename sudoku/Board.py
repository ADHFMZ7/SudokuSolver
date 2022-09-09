from sudoku import *
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import numpy as np

global driver 
driver = webdriver.Chrome(ChromeDriverManager().install())

def box(x, y, puzzle):
    result = []
    if y <= 2:
        if x <= 2:
            for i in range(0, 3):
                for j in range(0,3):
                    result.append(puzzle[j][i])
        elif x <= 5:
            for i in range(3, 6):
                for j in range(0,3):
                    result.append(puzzle[j][i])

        elif x >= 6:
            for i in range(6, 9):
                for j in range(0,3):
                    result.append(puzzle[j][i])
    elif y <= 5:
        if x <= 2:
            for i in range(0, 3):
                for j in range(3,6):
                    result.append(puzzle[j][i])
        elif x <= 5:
            for i in range(3, 6):
                for j in range(3,6):
                    result.append(puzzle[j][i])

        elif x >= 6:
            for i in range(6, 9):
                for j in range(3,6):
                    result.append(puzzle[j][i])
        
    elif y >= 6:
        if x <= 2:
            for i in range(0, 3):
                for j in range(6,9):
                    result.append(puzzle[j][i])
        elif x <= 5:
            for i in range(3, 6):
                for j in range(6,9):
                    result.append(puzzle[j][i])

        elif x >= 6:
            for i in range(6, 9):
                for j in range(6,9):
                    result.append(puzzle[j][i])
    return result

def valid(x, y, n, puzzle):
    for i in range(9):
        if puzzle[y][i] == n:
            return False
    for i in range(9):
        if puzzle[i][x] == n:
            return False
    if n in box(x,y, puzzle):
        return False
    return True

def solve(puzzle):
    for x in range(9):
        for y in range(9):
            if puzzle[y][x] == 0:
                for i in range(1,10):
                    if valid(x,y,i, puzzle):
                        puzzle[y][x] = i
                        solve(puzzle)
                        puzzle[y][x] = 0
                return
    np.savetxt('data.csv', puzzle, delimiter=',', fmt='%i')
    return

def collect():
    driver.get('https://www.websudoku.com/')
    time.sleep(1)
    driver.switch_to.frame(driver.find_element_by_xpath('/html/frameset/frame'))
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    grid = np.zeros((9,9), dtype='int')

    for i in range(9):
        for j in range(9):
            tile_id = 'f'+str(j)+str(i)
            tile = soup.find('input', {'id': tile_id})

            try:
                if tile['value'] != 0:
                    grid[i][j] = tile['value']
            except KeyError:
                pass
    return grid

def solver(grid):

    solve(grid)

    result = np.genfromtxt('data.csv', delimiter=',')
    return result


def fill(result):
    for i in range(9):
        for j in range(9):
            tile_id = 'f'+str(j)+str(i)
            driver.find_element_by_id(tile_id).send_keys(str(result[i][j]))
    driver.find_element_by_name('submit').click()  
