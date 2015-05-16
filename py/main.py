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
with open('../puzzles.txt') as f:
    puzzles = f.readlines()
    for puzzle in puzzles:
        puzzle_count += 1
        grid = Grid(puzzle.strip('\n'))
        solver = Solver(grid)
        print(grid)
        start = time.time() * 1000
        try:
            solver.solve()
            took = round(time.time() * 1000 - start)
            print(str(grid) +"\n")
            print("solved in "+str(took)+"ms with "+str(solver.guesses)+" guesses.")
            total_time += took
            total_guesses += solver.guesses 
        except ValueError as inconsistency:
            print("Couldn't solve it")
            print(inconsistency)
            print(grid)


       
print("Solved "+ str(puzzle_count)+" in avg "+str(round(total_time / puzzle_count)) + "ms. Total time: "+str(total_time)+"ms")
print("Had to make "+str(total_guesses)+ " guesses")