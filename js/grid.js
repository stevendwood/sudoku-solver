/***************************************************************
	Grid...
*/
(function() {
    "use strict"

    var Cell = require("./cell");

    class Grid {
        constructor(input) {
            var currentRow;
            this.rows = [];
          
        	for (var idx=0; idx<input.length; idx++) {
        		if (idx % 9 === 0) {
        			currentRow = [];
        			this.rows.push(currentRow);
        		}

        		currentRow.push(new Cell(this.rows.length-1, currentRow.length, input[idx]));
        	}
        }

    	toString() {
    		var output = "";
    		for (let i=0; i<this.rows.length; i++) {
    			if (i !== 0 && i % 3 === 0) {
    				output += "---------+---------+---------\n";
    			}
    			
    			let currentRow = this.rows[i];
    			for (let j=0; j<currentRow.length; j++) {
    				if (j !== 0 && j % 3 === 0) {
    					output += "|";
    				}

    				output += " " + currentRow[j].toString() + " ";
    			}

    			output += "\n";
    		}

    		return output;
    	}

    	subgrids() {
            if (!this.grids) {
        		this.grids = [];
        		for (let i=0; i<9; i+=3) {
           			for (let j=0; j<9; j+=3) {
           				this.grids.push(this.sameSubGridAs(new Cell(i, j)));
           			}
           		}
            }

       		return this.grids;
       	}
    	
    	columns() {
    		var columns = [];
    		for (let i=0; i<9; i++) {
    			columns.push([]);
    		}
    		this.rows.forEach(function(row) {
    			row.forEach(function(cell, idx) {
    				columns[idx].push(cell);
    			});
    		});

    		return columns;
    	}

    	sameRowAs(cell) {
    		return this.rows[cell.row];
    	}

    	sameColAs(cell) {
    		var column = [];
    		this.rows.forEach(function(r) { 
    			column.push(r[cell.col]);
    		});

    		return column;
    	}

    	sameSubGridAs(cell) {

            /*
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
            */

            // row:
            // 0 - 2 -> 0
            // 3 - 5 -> 3
            // 6 - 8 -> 5

            // col:
            // same as above
            if (!cell.subgrid) {
                let index = function(x) {
                	if (x <= 2) { return 0; }
                	else if (x <= 5) { return 3; }
                	else { return 6; }
                };

                let startRow = index(cell.row),
                	startCol = index(cell.col),
                	subgrid = [];
                for (let i=startRow; i<startRow+3; i++) {
                	let row = this.rows[i],
                		subGridRow = [];
                	for (let j=startCol; j<startCol+3; j++) {
                		subGridRow.push(row[j]);
                	}

                	subgrid.push(subGridRow);
                }
                cell.subgrid = subgrid;
            }

            return cell.subgrid;
    	}

    	unsolved() {
    		var unsolved = [];
    		this.rows.forEach(row => {
    			unsolved = unsolved.concat(row.filter(c => c.value === 0));
    		});

    		return unsolved;
    	}

    	isSolved() {
    		for (let i=0; i<this.rows.length; i++) {
    			for (let col=0; col<9; col++) {
    				if ((this.rows[i][col]).value === 0) {
    					return false;
    				} 
    			}
    		}
    		return true;
    	}

    	peers(cell) {
            /*
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
            */
            if (!cell.peers) {
                cell.peers = this.sameColAs(cell)
            		     .concat(this.sameRowAs(cell))
            		     // need to flatten the sub grids as it's an [[]]
            		     .concat([].concat.apply([], this.sameSubGridAs(cell)))
            		     .filter(x => x !== cell);
            }

            return cell.peers;
        }
    }

    module.exports = Grid;
}());