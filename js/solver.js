
(function() {

    "use strict";

    // [[1, 2, 3], [1, 2, 3]].flatten() gives [1, 2, 3, 1, 2, 3]
    Array.prototype.flatten = () => [].concat.apply([], this);

    var DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9];

    // These are a couple of useful map functions, pulling them up here
    // speeds things up.
    var valueOfCell = (cell => cell.value),
        possibleValuesOfCell = (cell => cell.possibleValues),
        isUnsolved = (cell => cell.value === 0);

    class Solver {

        constructor(grid) {
            this.grid = grid;
            this.guesses = 0;
            this._solvedCells = [];
        }

        solve() {
            // work out what the set of possible values is for each unsolve cell.
            this._initPossibleValues();
            // if there are any with only one possible value, set it.
            this._findCellsWithOnePossibleValue();
            // find any cells that have a possible value that doesn't occur
            // anywhere else in the column, row or subgrid it's in
            this._findUniqueValuesInUnits();
            if (!this.grid.isSolved()) {
                // this is a more tricky puzzle, so start searching for a solution.
                this._search();
            }
        }

        _search() {
            // pick the cell with least possible values (more chance of guessing correctly)
            var cell = (this.grid.unsolved().sort((x, y) => {
                var xVal = x.possibleValues.length * 100 + (x.row + x.col),
                    yVal = y.possibleValues.length * 100 + (y.row + y.col);

                return xVal - yVal;
            }))[0];

            for (let value of cell.possibleValues) {
                // remember how many cells we had solved before we begin incase
                // we need to unwind
                let numSolved = this._solvedCells.length;
                this.guesses += 1;

                try {
                    this._setValueForCell(cell, value);
                    if (!this.grid.isSolved()) {
                        // no luck, keep looking...
                        this._search();                      
                    }
                } catch (inconsistency) {
                    // here's the back tracking part, we've ended up in a position where we
                    // can't progress, so before we try another value, undo all the values
                    // we set since the last guess.   
                    let resetPossibilities = [];   
                    this._solvedCells.splice(numSolved, this._solvedCells.length - numSolved)
                                     .forEach(cell => { 
                                        cell.value = 0;
                                        resetPossibilities = resetPossibilities.concat(this.grid.peers(cell));
                                     }, this);

                    this._initPossibleValues(new Set(resetPossibilities.filter(isUnsolved)));
                }
            }
            if (!this.grid.isSolved()) {
                // If we get here then we're also stuck since we haven't found a solution despite trying
                // all possible values for a cell.
                throw "Tried all values for this cell  [" + cell.row + ", " + cell.col + "]" + cell.possibleValues;
            }
        }

        _initPossibleValues(cells) {
            (cells || this.grid.unsolved()).forEach((cell) => {
                let peerValues = this.grid.peers(cell).map(valueOfCell),
                    possibleValues = DIGITS.filter(d => peerValues.indexOf(d) === -1);
                    cell.possibleValues = possibleValues;
            }, this);
        }

        _removeValueFromPeers(cell) {
            // Summary:
            //  Remove the value of cell from the possible values of 
            //  it's peers.
            this.grid.peers(cell)
                    .filter(isUnsolved)
                    .forEach((p) => { 
                        var idx = p.possibleValues.indexOf(cell.value);
                        if (idx !== -1) {
                            p.possibleValues.splice(idx, 1);
                        }

                        if (p.possibleValues.length === 0) {
                            throw "No possible values for cell ["+p.row+", "+p.col+"] "+p.value;
                        }
                    });
        }

        _setValueForCell(cell, value) {
            var peers = this.grid.peers(cell);
           
            if (peers.some(x => x.value === value)) {
                throw "Tried to set a value that already exists in peers";
            }
            
            cell.value = value;
            this._solvedCells.push(cell);
            this._removeValueFromPeers(cell);
            this._findCellsWithOnePossibleValue(peers);
            this._findUniqueValuesInUnits(cell);
        }

        _findCellsWithOnePossibleValue(cells) {
            cells = (cells || this.grid.unsolved());
            cells.forEach(cell => {
                if (cell.value === 0 && cell.possibleValues.length === 1) {
                    this._setValueForCell(cell, cell.possibleValues[0]);
                }
            }, this);
        }

        _findUniqueValuesInUnits(cell) {

            if (cell) {
                [this.grid.sameSubGridAs(cell).flatten(),
                 this.grid.sameColAs(cell),
                 this.grid.sameRowAs(cell)].forEach(this._findUniquePossibiltyInUnit, this);
            } else {
                let subGrids = this.grid.subgrids().map(sg => sg.flatten());
            
                for (let units of [subGrids, this.grid.columns(), this.grid.rows]) {
                    for (let unit of units) {
                        this._findUniquePossibiltyInUnit(unit);
                    }
                }
            }
        }

        _findUniquePossibiltyInUnit(unit) {
            let unsolved = unit.filter(isUnsolved);
            unsolved.forEach(unsolvedCell => {
                var unique,
                    otherCellsPossValues = unit
                        .filter(c => c !== unsolvedCell)
                        .map(possibleValuesOfCell)
                        .flatten();
                        //.reduce((a, b) => a.concat(b));  
               
                unique = unsolvedCell.possibleValues.filter(x => otherCellsPossValues.indexOf(x) === -1);
                if (unique.length === 1) {
                    this._setValueForCell(unsolvedCell, unique[0]);
                }
            }, this);
        }
    }

    module.exports = Solver;

}());