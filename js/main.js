(function() {
	"use strict"

	var fs = require('fs');
	var Grid = require("./grid");
	var Solver = require("./solver");

	fs.readFile("../hard-puzzles.txt", "utf-8", function(error, data) {
		var puzzles = data.split("\n"),
			totalTime = 0,
			puzzleCount = 0,
			totalGuesses = 0;

		puzzles.forEach(puzzle => {
			puzzleCount++;

			var g = new Grid(puzzle.trim()),
				solver = new Solver(g),
				start;

			console.log(g.toString());
			start = Date.now();
			
			solver.solve();
			let time =  Date.now() - start;
			totalTime += time
			totalGuesses += solver.guesses;
			if (g.isSolved()) {
				console.log(g.toString());
				console.log("solved in "+(time)+" with "+solver.guesses +" guesses.");
			} else {
				console.log("Couldn't solve it.");
				console.log(g.toString());
			}
			console.log("\n");
		});

		console.log("Solved in avg "+totalTime / puzzleCount);
		console.log("Had to make "+totalGuesses+ " guesses");
	});
}());