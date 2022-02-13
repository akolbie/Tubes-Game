import csv
from doctest import OutputChecker
from random import randint


class SetupKeyError(Exception):
    pass

class Square():
    def __init__(self, size, orientation, accounted_for = 0):
        self.size = size
        self.begin_orientation = orientation
        self.orientation = orientation
        self.moves = 0
        self.accounted_for = accounted_for

    def rotate_clockwise(self, step = 1):
        if not self.size:
            return
        self.orientation += 1
    
    def rotate_counterclockwise(self, step = 1):
        if not self.size:
            return
        self.orientation -= 1
    
    def open_spots(self):
        return self.size - self.accounted_for

    def __str__(self):
        return f'{self.size}'

class Board():
    def __init__(self, **kwargs):
        self.board = []
        if 'location' in kwargs:
            self.create_board_from_csv(kwargs['location'])
        elif 'width' in kwargs and 'height' in kwargs:
            self.create_random_board(kwargs['width'], kwargs['height'])
        else:
            raise SetupKeyError('No valid **kwargs enters')

    def create_board_from_csv(self, location):
        with open(location, 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                self.board.append([])
                for cell in row:
                    self.board[-1].append(Square(
                                                    cell[0],
                                                    cell[1]))
    
    def create_random_board1(self, width, height):
        for i in range(int(height)):
            self.board.append([])
            for j in range(int(width)):
                update_left_cell = False
                accounted_for = 0
                max_possible = 4
                min_possible = 0

                #checks top cell
                if i == 0:
                    max_possible -= 1
                if self.board[i - 1][j].accounted_for != self.board[i - 1][j].size:
                    accounted_for += 1
                
                #checks left cell
                if j == 0:
                    max_possible -= 1
                if self.board[i][j - 1].size == 2 and self.board[i][j - 1].accounted_for == 1:
                    pass

    def create_random_board(self, width, height):
        for i in range(int(height)):
            self.board.append([])
            for j in range(int(width)):
                update_left_cell = False
                accounted_for = 0
                max_possible = 4
                min_possible = 0
                
                
                #checks cell above
                if i - 1 < 0:
                    max_possible -= 1
                else:
                    if self.board[i - 1][j].open_spots() > 0:
                        min_possible += 1
                        accounted_for += 1
                        self.board[i - 1][j].accounted_for += 1
                    else:
                        max_possible -= 1

                #checks cell to left
                if j - 1 < 0: 
                    max_possible -= 1
                else:
                    if self.board[i][j - 1].open_spots() > 1:
                        min_possible += 1
                        accounted_for += 1
                        self.board[i][j - 1].accounted_for += 1
                    elif self.board[i][j - 1].open_spots() == 1:
                        update_left_cell = True
                        #some how have to update adjacent cell 
                        pass #not sure this is right
                    else:
                        max_possible -= 1

                #checks cell to right
                if j + 1 == width:
                    max_possible -= 1
                
                #checks cell below
                if i + 1 == height:
                    max_possible -= 1

                #set up block 
                if min_possible == max_possible:
                    self.board[i].append(Square(min_possible, 0, accounted_for))
                else:
                    size = randint(min_possible, max_possible)
                    if size == max_possible and update_left_cell:
                        self.board[i][j - 1].accounted_for += 1
                        accounted_for += 1
                    elif size == min_possible:
                        pass
                    elif update_left_cell:
                        if randint(0, 1):
                            self.board[i][j - 1].accounted_for += 1
                            accounted_for += 1
                    self.board[i].append(Square(size, randint(0,3), accounted_for))

    def __str__(self):
        output = ""
        for row in self.board:
            for cell in row:
                output += f'{cell}'
            output += '\n'
        return output

