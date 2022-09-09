from sudoku import *
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import numpy as np

global driver 
driver = webdriver.Chrome(ChromeDriverManager().install())



class Board:
    def __init__(self):
        print("created driver")

    def collect(self):
        driver.get('https://www.websudoku.com/')
        time.sleep(1)
        driver.switch_to.frame(driver.find_element_by_xpath('/html/frameset/frame'))
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        self.grid = np.zeros((9,9), dtype='int')

        for i in range(9):
            for j in range(9):
                tile_id = 'f'+str(j)+str(i)
                tile = soup.find('input', {'id': tile_id})

                try:
                    if tile['value'] != 0:
                        self.grid[i][j] = tile['value']
                except KeyError:
                    pass 
  
        
    def box(self, x, y):
        result = []
        if y <= 2:
            if x <= 2:
                for i in range(0, 3):
                    for j in range(0,3):
                        result.append(self.grid[j][i])
            elif x <= 5:
                for i in range(3, 6):
                    for j in range(0,3):
                        result.append(self.grid[j][i])

            elif x >= 6:
                for i in range(6, 9):
                    for j in range(0,3):
                        result.append(self.grid[j][i])
        elif y <= 5:
            if x <= 2:
                for i in range(0, 3):
                    for j in range(3,6):
                        result.append(self.grid[j][i])
            elif x <= 5:
                for i in range(3, 6):
                    for j in range(3,6):
                        result.append(self.grid[j][i])

            elif x >= 6:
                for i in range(6, 9):
                    for j in range(3,6):
                        result.append(self.grid[j][i])
            
        elif y >= 6:
            if x <= 2:
                for i in range(0, 3):
                    for j in range(6,9):
                        result.append(self.grid[j][i])
            elif x <= 5:
                for i in range(3, 6):
                    for j in range(6,9):
                        result.append(self.grid[j][i])

            elif x >= 6:
                for i in range(6, 9):
                    for j in range(6,9):
                        result.append(self.grid[j][i])
        return result 
   
        
    def valid(self, x, y, n):
        for i in range(9):
            if self.grid[y][i] == n:
                return False
        for i in range(9):
            if self.grid[i][x] == n:
                return False
        if n in self.box(x,y):
            return False
        return True      
    
        
    def solve(self):
        for x in range(9):
            for y in range(9):
                if self.grid[y][x] == 0:
                    for i in range(1,10):
                        if self.valid(x,y,i):
                            self.grid[y][x] = i
                            self.solve()
                            self.grid[y][x] = 0
                    return
        self.fill() 
        return


    def fill(self):
        for i in range(9):
            for j in range(9):
                tile_id = 'f'+str(j)+str(i)
                driver.find_element_by_id(tile_id).send_keys(str(self.grid[i][j]))
        driver.find_element_by_name('submit').click()  


    def solve_puzzle(self):
        self.collect()
        self.solve()
        driver.find_element_by_xpath("//input[@type='submit']").click()