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
        self._grid = grid
        self.guesses = 0

    def solve(self, solved_cell_collector=[]):
        '''
            The algorithm is :

          1. For each cell, calculate the set of possible values by eliminating any solved
             values that are already in the cells peers (cells in the same row, column
             and sub grid)
          2. If after step 1 some cells only have one possible value, we can consider those
             cells to be solved.
          3. Repeat steps 1 and 2 until no more cells can be solved.
          4. In each row, column and sub grid, if there is only one place a value can go,
             then put it there and repeat steps 1 and 2 for all that cells peers.
          5. If the grid is not solved, start searching for a solution.  Gather all the
             unsolved cells and order them by the number of possible values they have, start
             with the lowest.
          6. Go through the possible values for each cell and attempt to solve the grid using
             all these rules, when we find an cell that does not have a value and has no possible
             values, or if we try every possible value for a cell and can't find a solution, we
             need to backtrack and then try another value.

          Because this method is called recursively
          we collect all the cells we solve in the list supplied.
        '''
        num_solved, unsolved = 1, self._grid.unsolved()
        while num_solved > 0:
            num_solved = len(solved_cell_collector)
            for cell in unsolved:
                self._exclude(cell, solved_cell_collector)
            # did we manage any ?
            num_solved = len(solved_cell_collector) - num_solved

        if not self._grid.is_solved():
            solved_cells = len(solved_cell_collector)
            self._find_unique_values_in_units(solved_cell_collector)
            if len(solved_cell_collector) - solved_cells is not 0:
                self.solve(solved_cell_collector)
            else:
                # no progress possible with our logic, start searching
                # for a solution...
                self._search(solved_cell_collector)

        return solved_cell_collector

    def _exclude(self, cell, solved_cell_collector):
        '''
            This is the process of looking at a cells subgrid, row and column and excluding from the
            list 1..9 all numbers that are already in the subgrid, row and column (peers).
        '''
        if cell.value is not 0:
            return []

        value_from_peers = [x.value for x in self._grid.peers(cell)]
        possible_values = [x for x in range(1, 10) if x not in value_from_peers]
        if len(possible_values) is 1:
            cell.value = possible_values[0]
            solved_cell_collector.append(cell)
        elif len(possible_values) > 0:
            cell.possible_values = possible_values
        else:
            raise ValueError('Cell has no possible value [' +
                             str(cell.row) + ', ' + str(cell.col) + ']')

    def _find_unique_values_in_units(self, solved_cell_collector):
        '''
            Looks for unique values amonst the set of possible values for a unit.
            If we find one, assign that value for the cell and then call _exclude
            on the cells peers.
        '''

        # get the sub grids
        sub_grids = [self._grid.same_sub_grid_as(Cell(x, y))
                     for y in range(0, 9, 3)
                     for x in range(0, 9, 3)]

        for unit in [x for l in [self._grid.rows, self._grid.columns(), sub_grids] for x in l]:
            for unsolved_cell in [cell for cell in unit if cell.value is 0]:
                all_other_vals = [x.possible_values for x in unit if x is not unsolved_cell]
                # all_other_vals is an [[]] where each element is the set of possible values
                # for a cell in the unit.
                all_other_vals = [x for l in all_other_vals for x in l]
                # now it's a flat list so we can easily check if there any values in the cell
                # we're considering that are not in any other cells possibles values...
                found = [x for x in unsolved_cell.possible_values if x not in all_other_vals]
                if len(found) is 1:
                    unsolved_cell.value = found[0]
                    solved_cell_collector.append(unsolved_cell)      

    def _search(self, solved_cell_collector):
        '''
            This is the backtracking search.  The "solved_cell_collector" is used to implement the
            backtracking, so that we can undo values that were set following a guess that leads to
            a dead end.
        '''
        # get the unsolved cells, ordered according to the selection policy
        cell = sorted(self._grid.unsolved(), key=lambda cell: len(cell.possible_values))[0]
        
        for value in cell.possible_values:
            # take a copy of the currently solved cells
            copied = solved_cell_collector[:]
            # try one of the values...
            self.guesses += 1
            cell.value = value
            solved_cell_collector.append(cell)
            try:
                self.solve(solved_cell_collector)
                if self._grid.is_solved():
                    # wahey !!
                    return
            except ValueError as inconsistency:
                # here's the back tracking part, we've ended up in a position where we
                # can't progress, so before we try another value, undo all the values
                # we set since the last guess.
                solved_since_last_guess = [x for x in solved_cell_collector if x not in copied]
                for undo_me in solved_since_last_guess:
                    undo_me.possible_values = []
                    undo_me.value = 0
                solved_cell_collector = copied
        # If we get here then we're also stuck since we haven't found a solution despite trying
        # all possible values for a cell.
        raise ValueError('Tried all values for this cell  [' +
                          str(cell.row) + ', ' + str(cell.col) + ']')