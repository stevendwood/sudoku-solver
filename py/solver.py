'''
    solver.py.

    Defines the solver type, to be user along with a "Grid" g as in
    solver = Solver(g)
    solver.solve()
'''

from grid import Cell

class Solver(object):
    '''
        Defines the solver algorithm
    '''
    def __init__(self, grid):
        self.grid = grid
        self.guesses = 0
        self._solved_cells = [];

    def solve(self):
        # work out what the set of possible values is for each unsolve cell.
        self.init_possible_values()
        # if there are any with only one possible value, set it.
        self.find_cells_with_one_possible_value(self.grid.unsolved())
        # find any cells that have a possible value that doesn't occur
        # anywhere else in the column, row or subgrid it's in
        self.find_unique_values_in_units()
        if not self.grid.is_solved():
            # this is a more tricky puzzle, so start searching for a solution.
            self._search();    

    def init_possible_values(self):
        for cell in self.grid.unsolved():
            peers = self.grid.peers(cell)
            value_from_peers = [x.value for x in peers]
            cell.possible_values = [x for x in range(1, 10) if x not in value_from_peers]
            
    def find_cells_with_one_possible_value(self, cells):
        for cell in cells:
            if cell.value == 0 and len(cell.possible_values) == 1:
                self.set_value_for_cell(cell, cell.possible_values[0])

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

    def find_unique_values_in_units(self, cell=None):
            if cell is not None:
                sg = self.grid.same_sub_grid_as(cell)
                for unit in [sg, self.grid.same_col_as(cell), self.grid.same_row_as(cell)]:
                    self.find_unique_possibility_in_unit(unit)  
            else:
                for unit in [x for l in [self.grid.rows, self.grid.columns(), self.grid.subgrids()] for x in l]:
                    self.find_unique_possibility_in_unit(unit)
                                
    def set_value_for_cell(self, cell, value):
        peers = self.grid.peers(cell);
           
        if any(x.value is value for x in peers):
            raise ValueError('Tried to set value that already exists in peers')
          
        cell.value = value
        self._solved_cells.append(cell)
        self.remove_value_from_peers(cell)
        self.find_cells_with_one_possible_value(peers)
        self.find_unique_values_in_units(cell)

    def remove_value_from_peers(self, cell):  
        for p in (peer for peer in self.grid.peers(cell) if peer.value == 0):
            if cell.value in p.possible_values:
                p.possible_values.remove(cell.value)
            if len(p.possible_values) == 0:
                raise ValueError("No possible value [" + str(p.row) + ", " + str(p.col) + "]")

    def _search(self):
           
        cell = sorted(self.grid.unsolved(), key=lambda c: len(c.possible_values) * 100 + (c.row + c.col))[0]
        #print("Values "+str(cell.possible_values))
        for value in cell.possible_values:
            #print("Trying a "+str(value)+" cell  [" + str(cell.row) + ", " + str(cell.col) + "]" + str(cell.possible_values))
            num_solved = len(self._solved_cells)
            self.guesses += 1;

            try:
                self.set_value_for_cell(cell, value);
                if not self.grid.is_solved():
                    #no luck, keep looking...
                    self._search()              
                
            except ValueError as inconsistency:
                # here's the back tracking part, we've ended up in a position where we
                # can't progress, so before we try another value, undo all the values
                # we set since the last guess.   
                #print(inconsistency)
                #print(self.grid);
                solved_since_last_guess = self._solved_cells[num_solved:]
                # print("Undoing "+str(len(solved_since_last_guess)))
                for c in solved_since_last_guess:
                    c.value = 0
                self._solved_cells = self._solved_cells[:num_solved]
                self.init_possible_values()

        if not self.grid.is_solved():
            # If we get here then we're also stuck since we haven't found a solution despite trying
            # all possible values for a cell.
            raise ValueError("Tried all values for this cell  [" + str(cell.row) + ", " + str(cell.col) + "]" + str(cell.possible_values))
            
        
        



            

   
   