"""

    The structure is :

        Grid - a class representing the 9x9 Sudoku grid
        Cell - represents an individual cell, so there's 81 of these
        Solver - implements the algorithm to solve the puzzle.

"""
import time
from grid import Grid
from solver import Solver

total_time, total_guesses, puzzle_count = 0, 0, 0
# ooh this is a nice feature of python, if your object implements
# __enter__ and __exit__ the you can use with rather than try: finally
with open('../test-puzzles.txt') as f:
    puzzles = f.readlines()
    for puzzle in puzzles:
        puzzle_count += 1
        grid = Grid(puzzle.strip('\n'))
        solver = Solver(grid)
        start = time.time()
        try:
            solved_cells = solver.solve()
        except ValueError as inconsistency:
            print("Couldn't solve it")
            print(grid)
        print("solved in "+str(time.time() - start)+" with "+str(solver.guesses)+" guesses.")
        total_time += time.time() - start
        total_guesses += solver.guesses 
        print(grid)
print("Solved in avg "+str(total_time / puzzle_count))
print("Had to make "+str(total_guesses)+ " guesses")