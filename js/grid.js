/***************************************************************
	Grid...
*/
var Cell = require("./cell");

function Grid(input) {
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

Grid.prototype = {
	toString: function() {
		var output = "";
		for (var i=0; i<this.rows.length; i++) {
			if (i !== 0 && i % 3 === 0) {
				output += "---------+---------+---------\n";
			}
			
			var currentRow = this.rows[i];
			for (var j=0; j<currentRow.length; j++) {
				if (j !== 0 && j % 3 === 0) {
					output += "|";
				}

				output += " " + currentRow[j].toString() + " ";
			}

			output += "\n";
		}

		return output;
	},

	subgrids: function() {
		var grids = [];
		for (var i=0; i<9; i+=3) {
   			for (var j=0; j<9; j+=3) {
   				grids.push(this.sameSubGridAs(new Cell(i, j)));
   			}
   		}

   		return grids;
   	},
	

	columns: function() {
		var columns = [];
		for (var i=0; i<9; i++) {
			columns.push([]);
		}
		this.rows.forEach(function(row) {
			row.forEach(function(cell, idx) {
				columns[idx].push(cell);
			});
		});

		return columns;
	},

	sameRowAs: function(cell) {
		return this.rows[cell.row];
	},

	sameColAs: function(cell) {
		var column = [];
		this.rows.forEach(function(r) { 
			column.push(r[cell.col]);
		});

		return column;
	},

	sameSubGridAs: function(cell) {

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

        var index = function(x) {
        	if (x <= 2) { return 0; }
        	else if (x <= 5) { return 3; }
        	else { return 6; }
        };

        var startRow = index(cell.row),
        	startCol = index(cell.col),
        	subGrid = [];
        for (var i=startRow; i<startRow+3; i++) {
        	var row = this.rows[i],
        		subGridRow = [];
        	for (var j=startCol; j<startCol+3; j++) {
        		subGridRow.push(row[j]);
        	}

        	subGrid.push(subGridRow);
        }

        return subGrid;
	},

	unsolved: function() {
		var unsolved = [];
		this.rows.forEach(function(row) {
			unsolved = unsolved.concat(row.filter(function(c) { return c.value === 0; }));
		});

		return unsolved;
	},

	isSolved: function() {
		for (var i=0; i<this.rows.length; i++) {
			for (var col=0; col<9; col++) {
				if ((this.rows[i][col]).value === 0) {
					return false;
				} 
			}
		}
		return true;
	},

	peers: function(cell) {
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
        return this.sameColAs(cell)
        		.concat(this.sameRowAs(cell))
        		// need to flatten the sub grids as it's an [[]]
        		.concat([].concat.apply([], this.sameSubGridAs(cell)))
        		.filter(function(x) { return x !== cell; });
    }
};

module.exports = Grid;