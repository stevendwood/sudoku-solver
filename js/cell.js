/****************************************************************

	Cell...


*/

function Cell(row, col, value) {
	this.value = value || 0;
	this.row = row;
	this.col = col;
	if (value == '.') {
         this.value = 0;
     } else {
     	this.value = parseInt(value, 10);
     }

     this.possibleValues = [];
}

Cell.prototype.toString = function() {
	return this.value || "-";
}

module.exports = Cell