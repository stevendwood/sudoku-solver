# sudoku-solver
A sudoku solver in various languages, the actual algorithm to solve the puzzles doesn't seem very efficient, but it works.  Just me attempting to learn some new languages (and implement the same solution in some I already know...)

  * Python
  * JavaScript (ES6)
  * Java 8
  * Ruby

There's a list of hard puzzles pruned from the project euler site.  The program reads the file and solves each puzzle. Each line is e.g.

....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...

Since each language so far supports OO there are 3 classes and a "main" file or class to run the thing.

* Grid - models a Sudoku puzzle as a list of lists (9x9)
* Cell - models a single Cell, and retains a list of "possible values" that a solver can fiddle with.
* Solver - implements the Solver algorithm.  

The algorithm works something like this.

1. Compute the list of possible values for all unsolved cells.
2. If any cells have only one possible value, set it.
3. If a cell is the only one in it's column, row or subgrid to contain a particular possible value, then set it.
4. If after steps 1 - 3 we haven't found a solution start searching.
5. Pick the cell with the least possible values and set a value for it.
6. Try and solve the grid using steps 1 - 5 until we either solve it or hit a dead end. When we hit a dead end, undo the last guess and it's side effects and try the next value.

The backtracking bit is done by throwing and catching exceptions which is probably not very efficient but i chose it so it to learn about the languages Exception handling features.

There are 106 puzzles,

* Java ~2s avg 19ms per puzzle
* ES6  ~4.4s avg 42ms per puzzle
* Python 3.4 ~8.7s avg 82ms per puzzle
* Ruby 2.0.0 ~17s avg 160ms per puzzle

To compile and run the Java source from /java

javac src/main/java/org/woody/sudoku/*.java
java -classpath ./src/main/java org.woody.sudoku.Main
