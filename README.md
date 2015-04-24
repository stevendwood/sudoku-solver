# sudoku-solver
A sudoku solver in various languages, the actual algorithm to solve the puzzles doesn't seem very efficient, but it works.  Nothing much to see here, just me attempting to learn some new languages (and implement the same solution in some I already know...)

  * Python (main file is sudoku.py)
  * JavaScript JS version uses some ES6 features, (arrow functions, for..of and let) so i used  
  
        iojs --harmony_arrow_functions main.js
        
 
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

 
 The backtracking works by undoing the last guess and every cell solved since it was made. e.g. in Python (supposing 'cell' is an unsolved cell we picked to start searching from)
 ```python 
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
         # we did it !!
         return
     except ValueError as inconsistency:
       solved_since_last_guess = [x for x in solved_cell_collector if x not in copied]
       for undo_me in solved_since_last_guess:
         undo_me.possible_values = []
         undo_me.value = 0
         solved_cell_collector = copied
      # If we get here then we're also stuck since we haven't found a solution despite trying
      # all possible values for a cell.
      raise ValueError('Tried all values for this cell  [' +
                          str(cell.row) + ', ' + str(cell.col) + ']')