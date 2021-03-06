'''
    solver.py.

    Defines the solver type, to be user along with a "Grid" g as in
    solver = Solver(g)
    solver.solve()
'''
DIGITS = set(x for x in range(1, 10))

class Solver(object):
    '''
        Defines the solver algorithm.  
    '''
    def __init__(self, grid):
        self.grid = grid
        self.guesses = 0
        self._solved_cells = []

    def solve(self):
        '''
            Solve the grid.  The algorithm is to first work out what the list
            of possible values is for each unsolved cell. In some cases this
            will result in a list of length 1, in which case we can set the value
            for the cell to it's only possible value.  Having done this the next
            step is to see whether there are any unsolved cells that have a possible
            value which occurs in no other cell in the same row, same column or same
            3x3 sub grid.  Repeat until we either solve the grid or no other cells
            can be solved in which case we need to start searching for a solution.
        '''
        # work out what the set of possible values is for each unsolved cell.
        self.init_possible_values()
        # if there are any with only one possible value, set it.
        self.find_cells_with_one_possible_value(self.grid.unsolved())
        # find any cells that have a possible value that doesn't occur
        # anywhere else in the column, row or subgrid it's in
        self.find_unique_values_in_units()
        if not self.grid.is_solved():
            # this is a more tricky puzzle, so start searching for a solution.
            self._search()

    def _search(self):      
        cell = min(self.grid.unsolved(), key=lambda c: len(c.possible_values)* 100 + (c.row + c.col))
        num_possibilities = len(cell.possible_values)
        for idx, value in enumerate(cell.possible_values):
            num_solved = len(self._solved_cells)
            self.guesses += 1
            try:
                self.set_value_for_cell(cell, value)
                if not self.grid.is_solved():
                    # no luck, keep looking...
                    self._search()
            except ValueError:
                # we've ended up in a position where we
                # can't progress, so before we try another value, undo all the values
                # we set since the last guess.
                if idx != (num_possibilities -1):
                    # get the cells that we provided a value for before we got stuck
                    solved_since_last_guess = self._solved_cells[num_solved:]
                    reset = []
                    for c in solved_since_last_guess:
                        c.value = 0
                        reset += self.grid.peers(c)
                    # need to provide a new set of possible values for all those cells
                    # that are affected by the incorrect guess.
                    self.init_possible_values([x for x in set(reset) if x.value == 0])
                    self._solved_cells = self._solved_cells[:num_solved]

        if not self.grid.is_solved():
            # If we get here then we're also stuck since we haven't found a solution despite trying
            # all possible values for a cell.
            raise ValueError("Tried all values for this cell  [" + str(cell.row) + ", " + str(cell.col) + "]" + str(cell.possible_values))

    def init_possible_values(self, cells=None):
        ''' 
            Initialise the possible values for the provided list of cells or
            all the unsolved cells in the grid if no list was provided.

            To do this we collect the "peers" for each cell (cells not marked . for the cell c):

            x x x | . . . | . . .
            5 c x | x x 2 | x 9 x
            x x 3 | . . . | . . .
            ------+-------+------
            . x . | . . . | . . .
            . x . | . . . | . . .
            . x . | . . . | . . .
            ------+-------+------
            . x . | . . . | . . .
            . 7 . | . . . | . . .
            . x . | . . . | . . .

            Remove from the peers any unsolved cells, then exclude from the list 1..9 any 
            numbers already present in the list of solved peers. e.g. in the above grid assuming
            that any cell containing an x or a number is a peer of c and that the cells containing
            the numbers are solved then the possible values for "c" are:

            [1, 2, 3, 4, 5, 6, 7, 8, 9] - [5, 3, 2, 9, 7] = [8, 1, 4, 6]

        '''
        if cells is None:
            cells = self.grid.unsolved()
        for cell in cells:
            cell.possible_values = list(DIGITS - set(x.value for x in self.grid.peers(cell) if x.value != 0))

    def remove_value_from_peers(self, cell):
        '''
            Remove the value of the given cell from the possible values
            of any unsolved peer cells.

            If this results in a cell having no possible values, then 
            raise an exception.
        '''
        peers = self.grid.peers(cell)
        for p in (peer for peer in peers if peer.value == 0):
            if cell.value in p.possible_values:
                p.possible_values.remove(cell.value)
            if len(p.possible_values) == 0:
                raise ValueError("No possible value [" + str(p.row) + ", " + str(p.col) + "]")

    def set_value_for_cell(self, cell, value):
        peers = self.grid.peers(cell)
        
        if any(x.value is value for x in peers):
            raise ValueError('Tried to set value that already exists in peers')
        
        cell.value = value
        cell.possible_values = []
        self._solved_cells.append(cell)
        self.remove_value_from_peers(cell)
        self.find_cells_with_one_possible_value(peers)
        self.find_unique_values_in_units(cell)
            
    def find_cells_with_one_possible_value(self, cells):
        # comprehension with side-effects instead of for loop...
        [self.set_value_for_cell(cell, cell.possible_values[0]) 
         for cell in cells if cell.value == 0 and len(cell.possible_values) == 1]

    def find_unique_values_in_units(self, cell=None):
        if cell is not None:
            for unit in [self.grid.same_sub_grid_as(cell), self.grid.same_col_as(cell), self.grid.same_row_as(cell)]:
                self.find_unique_possibility_in_unit(unit)  
        else:
            for unit in [x for l in [self.grid.rows, self.grid.columns(), self.grid.subgrids()] for x in l]:
                self.find_unique_possibility_in_unit(unit)

    def find_unique_possibility_in_unit(self, unit):
        for unsolved_cell in [cell for cell in unit if cell.value == 0]:
            all_other_vals = [x.possible_values for x in unit if x is not unsolved_cell]
            # all_other_vals is an [[]] where each element is the set of possible values
            # for a cell in the unit.
            all_other_vals = [x for l in all_other_vals for x in l]
            # now it's a flat list so we can easily check if there any values in the cell
            # we're considering that are not in any other cells possibles values...
            found = [x for x in unsolved_cell.possible_values if x not in all_other_vals]
            if len(found) == 1:
                self.set_value_for_cell(unsolved_cell, found[0])