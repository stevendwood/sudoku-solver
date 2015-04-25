/****************************************************************

    Solver...

*/
(function() {

    "use strict";

    var DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9];

    // The are a couple of useful map functions, pulling them up here
    // speeds things up.
    var valueOfCell = (cell => cell.value),
        possibleValuesOfCell = (cell => cell.possibleValues);

    function Solver(grid) {
        this.grid = grid;
        this.guesses = 0;
    }

    Solver.prototype = {

        solve: function(collector) {
            /*
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
            */
            var numSolved = 0;

            collector = (collector || []);

            do {
                numSolved = collector.length;
                this.grid.unsolved()
                         .forEach(this._exclude.bind(this, collector));
                // did we manage any ?
                numSolved = collector.length - numSolved;
            } while (numSolved > 0);

            if (!this.grid.isSolved()) {
                let solvedCells = collector.length;
                this._findUniqueValuesInUnits(collector);
                if (collector.length - solvedCells > 0) {
                    this.solve(collector);
                } else {
                    // no progress possible with our logic, start searching
                    // for a solution...
                    this._search(collector);
                }
            }

            return collector;
        },

        _exclude: function(collector, cell) {
            /*
               This is the process of looking at a cells subgrid, row and column and excluding from the
                list 1..9 all numbers that are already in the subgrid, row and column (peers).
            */

            if (cell.value === 0) {
                let peers = this.grid.peers(cell),
                    peerValues = peers.map(valueOfCell),
                    possibleValues = DIGITS.filter(d => peerValues.indexOf(d) === -1);

                if (possibleValues.length === 1) {
                    cell.value = possibleValues[0];
                    collector.push(cell);
                } else if (possibleValues.length > 0) {
                    cell.possibleValues = possibleValues;
                } else {
                    throw 'Cell has no possible value [' + cell.row + ', ' + cell.col + ']';
                }
            }
        },

        _findUniqueValuesInUnits: function(collector) {
            /*
                Looks for unique values amongst the set of possible values for a unit.
                If we find one, assign that value for the cell and then call _exclude
                on the cells peers.
            */
            // get the sub grids
            var subGrids = [];
            this.grid.subgrids().forEach((sg) => {
                subGrids.push([].concat.apply([], sg));
            });
            
            for (let units of [subGrids, this.grid.columns(), this.grid.rows]) {
                for (let unit of units) {
                    let unsolved = unit.filter(c => c.value === 0);
                    //console.log("Unsolved in the unit is ", unsolved.length)
                    unsolved.forEach((unsolvedCell) => {
                        var unique,
                            otherCellsPossValues = unit
                                    .filter(c => c !== unsolvedCell)
                                    .map(possibleValuesOfCell);
                        // flatten these...
                        otherCellsPossValues = [].concat.apply([], otherCellsPossValues);
                        unique = unsolvedCell.possibleValues.filter(x => otherCellsPossValues.indexOf(x) === -1);
                        if (unique.length === 1) {
                            unsolvedCell.value = unique[0];
                            collector.push(unsolvedCell);
                        }
                    });
                }
            }
        },

        _search: function(collector) {
            /*
                This is the backtracking search.  The "collector" is used to implement the
                backtracking, so that we can undo values that were set following a guess that leads to
                a dead end.
            */
            var cell = (this.grid.unsolved().sort((x, y) => x.possibleValues.length - y.possibleValues.length)[0]);

            for (let value of cell.possibleValues) {
                let copied = collector.slice();
                this.guesses += 1;
                cell.value = value;
                collector.push(cell);
                try {
                    this.solve(collector);
                    if (this.grid.isSolved()) {
                        // wahey !!
                        return;
                    }
                } catch (inconsistency) {
                    // here's the back tracking part, we've ended up in a position where we
                    // can't progress, so before we try another value, undo all the values
                    // we set since the last guess.      
                    collector.filter(x => copied.indexOf(x) === -1)
                             .forEach(this._undo);
                    collector = copied;
                }
            }
            // If we get here then we're also stuck since we haven't found a solution despite trying
            // all possible values for a cell.
            throw 'Tried all values for this cell  [' + cell.row + ', ' + cell.col + ']' + cell.possibleValues;
        },

        _undo: function(cell) {
            cell.possibleValues = [];
            cell.value = 0;
        }
    };

    module.exports = Solver;

}());