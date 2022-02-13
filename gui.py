from itertools import count
from random import randint
import pygame
import copy
import csv
import sys
from math import floor, ceil
from board import Board, Square

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

class Cell_GUI():
    def __init__(self, square, dim, path_colour, background_colour = (255, 255, 255)):
        self.square = square
        self.dim = dim
        self.path_colour = path_colour
        self.background_colour = background_colour
        self.grid = [[self.background_colour for i in range(self.dim)] for j in range(self.dim)]
        self.find_center()
        self.update_grid()

    def rotate(self, ccw = False):
        temp_grid = [[] for i in range(self.dim)]
        for row in self.grid:
            for cindex, cell in enumerate(row):
                if not ccw:
                    temp_grid[cindex].insert(0, cell)
                    if self.square.orientation == 3:
                        self.square.orientation = 0
                    else:
                        self.square.orientation += 1
                else:
                    temp_grid[-cindex - 1].append(cell)
                    if self.square.orientation == 0:
                        self.square.orientation = 3
                    else:
                        self.square.orientation -= 1
        self.grid = copy.deepcopy(temp_grid)

    def reset(self):
        self.grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    def update_grid(self):
        pass

    def find_center(self):
        self.path_locations = (int(floor(self.dim * 2 / 5)), int(ceil(self.dim * 3 / 5)))


class Cell_1_GUI(Cell_GUI):
    def update_grid(self):
        for i in range(self.path_locations[0]):
            for j in range(*self.path_locations):
                self.grid[i][j] = self.path_colour
        
        #20% of length
        factor = self.path_locations[1] - self.path_locations[0]
        factor *= 0.3
        for i in range(int(floor(self.path_locations[0] - factor)),int(ceil(self.path_locations[1] + factor))):
            for j in range(int(floor(self.path_locations[0] - factor)),int(ceil(self.path_locations[1] + factor))):
                self.grid[i][j] = self.path_colour   

        for _ in range(self.square.orientation):
            self.rotate()
        self.square.orientation = self.square.begin_orientation

class Cell_2_GUI(Cell_GUI):
    def update_grid(self):
        for i in range(self.path_locations[1]):
            for j in range(*self.path_locations):
                self.grid[i][j] = self.path_colour
                self.grid[j][i] = self.path_colour
        
        for _ in range(self.square.orientation):
            self.rotate()
        self.square.orientation = self.square.begin_orientation

class Cell_3_GUI(Cell_GUI):
    def update_grid(self):
        for i in range(self.path_locations[1]):
            for j in range(*self.path_locations):
                self.grid[i][j] = self.path_colour
                self.grid[j][i] = self.path_colour
                self.grid[j][-i] = self.path_colour

        for _ in range(self.square.orientation):
            self.rotate()
        self.square.orientation = self.square.begin_orientation

class Cell_4_GUI(Cell_GUI):
    def update_grid(self):
        for i in range(len(self.grid)):
            for j in range(*self.path_locations):
                self.grid[i][j] = self.path_colour
                self.grid[j][i] = self.path_colour
        
        for _ in range(self.square.orientation):
            self.rotate()
        self.square.orientation = self.square.begin_orientation
    

class Board_GUI():
    def __init__(self, board, path_colour, background_colour = (255, 255, 255)):
        self.board = board
        self.num_width = len(self.board.board[0])
        self.num_height = len(self.board.board)
        self.path_colour = path_colour
        self.background_colour = background_colour
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()

        self.myfont = pygame.font.SysFont('Monospace', 16)

        self.gw = SCREEN_WIDTH / self.num_width
        self.gh = SCREEN_HEIGHT / self.num_height
        self.dim = int(min(self.gw, self.gh))


        self.create_board()

    def run_game(self):
        while True:
            self.clock.tick(10)
            self.draw_grid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    button = event.button
                    col_index = floor(pos[0] / self.dim)
                    row_index = floor(pos[1] / self.dim)

                    if button == 1:
                        self.cell_board[row_index][col_index].rotate()
                        self.update_cell(row_index, col_index)
                    elif button == 3:
                        self.cell_board[row_index][col_index].rotate(True)
                        self.update_cell(row_index, col_index)
                    else:
                        pass

            self.screen.blit(self.surface, (0,0))
            pygame.display.update()

    def draw_grid(self):
        for rowindex, row in enumerate(self.drawn_grid):
            for colindex, cell in enumerate(row):
                r = pygame.Rect((colindex, rowindex), (1, 1))
                pygame.draw.rect(self.surface, cell, r)
    
    def make_drawn_grid(self):
        self.drawn_grid = [['x' for i in range(self.dim * len(self.cell_board[0]))] for j in range(self.dim * len(self.cell_board))]

        for row_index, row in enumerate(self.cell_board):
            for cell_index, cell in enumerate(row):
                for iindex, i in enumerate(self.drawn_grid[row_index * self.dim: row_index * self.dim + self.dim]):
                    i[cell_index * self.dim: cell_index * self.dim + self.dim] = cell.grid[iindex]

    def update_cell(self, row_index, col_index):
        counter = 0
        for grid_row_index in range(row_index * self.dim, row_index * self.dim + self.dim):
            self.drawn_grid[grid_row_index][col_index * self.dim : col_index * self.dim + self.dim] = self.cell_board[row_index][col_index].grid[counter]
            counter += 1

    def create_board(self):
        self.cell_board = []
        for row in self.board.board:
            self.cell_board.append([])
            for square in row:
                if square.size == 0:
                    self.cell_board[-1].append(Cell_GUI(square, self.dim, self.path_colour, self.background_colour))
                elif square.size == 1:
                    self.cell_board[-1].append(Cell_1_GUI(square, self.dim, self.path_colour, self.background_colour))
                elif square.size == 2:
                    self.cell_board[-1].append(Cell_2_GUI(square, self.dim, self.path_colour, self.background_colour))
                elif square.size == 3:
                    self.cell_board[-1].append(Cell_3_GUI(square, self.dim, self.path_colour, self.background_colour))
                else:
                    self.cell_board[-1].append(Cell_4_GUI(square, self.dim, self.path_colour, self.background_colour))


if __name__ == "__main__":
    x = Board(width = randint(5, 10), height = randint(5, 10))
    y = Board_GUI(x, (randint(0, 255), randint(0, 255), randint(0, 255)), (0, 0, 0))
    y.make_drawn_grid()
    y.run_game()
