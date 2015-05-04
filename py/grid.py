'''
    grid.py

    Defines a Grid and Cell types

    A custom iterator because I'm learning Python and it allows me to iterate over
    a Grids content using the  languages for in loop e.g.
    for cell in grid:
        ...
'''
import math

class Grid(object):
    '''
        Models a grid as a list of lists of 9 cells.
        Currently requires to be created using an input string of 81 characters
        e.g.

        6.2.5.........4.3..........43...8....1....2........7..5..27...........81...6.....
    '''
    def __init__(self, input_str):
        self.rows = []
        self._sub_grids = None
        self._sub_grid_dict = {} # cache the sub grid a cell is in
        for row_idx in range(0, len(input_str), 9):
            row = input_str[row_idx:row_idx+9]
            current_row = []
            for col in range(9):
                current_row.append(Cell(len(self.rows), col, row[col]))
            self.rows.append(current_row)

    def peers(self, cell):
        '''
            Get the peers for the cell.  The peers for the cell "c" are pictorially
            represented below by the cells marked "x"

            x x x | . . . | . . .
            x c x | x x x | x x x
            x x x | . . . | . . .
            ------+-------+------
            . x . | . . . | . . .
            . x . | . . . | . . .
            . x . | . . . | . . .
            ------+-------+------
            . x . | . . . | . . .
            . x . | . . . | . . .
            . x . | . . . | . . .
        '''
        
        if cell.peers is None:
            cell.peers = [x for x in self.same_sub_grid_as(cell) +
                                        self.same_col_as(cell) + 
                                        self.same_row_as(cell) if x is not cell]
        return cell.peers

    def columns(self):
        '''
            Get all the columns in the grid as a list of lists.
            [0] is the list of cells in column 1, [1] the list of cells
            in column 2 etc.
        '''
        return [[row[col] for row in self.rows] for col in range(9)]

    def subgrids(self):
        if self._sub_grids is None:
            self._sub_grids = [self.same_sub_grid_as(Cell(x, y))
                     for y in range(0, 9, 3)
                     for x in range(0, 9, 3)]
        return self._sub_grids

    def same_row_as(self, cell):
        '''
            Get all the cells in the same row as the given cell.
        '''
        return self.rows[cell.row]

    def same_col_as(self, cell):
        '''
            Get all the cells in the same column as the given cell.
        '''
        return [x[cell.col] for x in self.rows]

    def same_sub_grid_as(self, cell):
        '''
            Get all the cells in the same "sub grid" as the given cell. e.g.
            for the cell "c" below the cells in the "same_sub_grid" (which are
            marked x below) are returned along with the argument cell.

            x x x | . . . | . . .
            x c x | . . . | . . .
            x x x | . . . | . . .
            ------+-------+------
            . . . | . . . | . . .
            . . . | . . . | . . .
            . . . | . . . | . . .
            ------+-------+------
            . . . | . . . | . . .
            . . . | . . . | . . .
            . . . | . . . | . . .
        '''
        # I could of course have divided the grid into
        # sub grids at construction time and give the cell
        # a reference to that...maybe I should have. But since
        # we get asked to provide this "sub grid" frequently
        # might as well cache it.

        cell_id = id(cell)
        if cell_id in self._sub_grid_dict:
            return self._sub_grid_dict[cell_id]

        grid_start_row = 0

        if cell.row < 3:
            grid_start_row = 0
        elif cell.row < 6:
            grid_start_row = 3
        else:
            grid_start_row = 6

        grid_start_col = 0

        if cell.col < 3:
            grid_start_col = 0
        elif cell.col < 6:
            grid_start_col = 3
        else:
            grid_start_col = 6

        sub_grid = [self.rows[grid_start_row + i][grid_start_col + j]
                    for j in range(3) for i in range(3)]
        self._sub_grid_dict[cell_id] = sub_grid
        return sub_grid
    
    def is_solved(self):
        for row in self.rows:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def unsolved(self):
        '''
            Get all the cells in this Grid that are unsolved
        '''
        unsolved = []
        for row in self.rows:
            for cell in row:
                if cell.value == 0:
                    unsolved.append(cell)
        return unsolved

    def __str__(self):
        '''
            Provide a string representation of this Grid.
        '''
        output = ''
        for row in range(9):
            output += '\n'

            if row is not 0 and row % 3 == 0:
                output += '---------+---------+---------\n'
            for col in range(9):
                cell = self.rows[row][col]
                if col is not 0 and col % 3 == 0:
                    output += '|'
                output += ' ' + str(cell) + ' '

        return output

class Cell(object):
    '''
        Represents a single cell of the puzzle.  Is used to
        store a value, and a list of possible values as well as the
        row and column the cell is in.
    '''

    def __init__(self, row, col, value=0):
        self.row = row
        self.col = col
        if value is '.':
            value = 0
        self.value = int(value)
        self.possible_values = []
        self.peers = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.value == 0:
            return '-'
        else:
            return str(self.value)
