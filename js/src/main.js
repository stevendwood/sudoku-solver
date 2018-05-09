const fs = require('fs');
const util = require('util')
const Grid = require("./grid");
const Solver = require("./solver");

const readFile = util.promisify(fs.readFile);

Array.prototype.flatten = function() { return [].concat.apply([], this); };

(async () => {
    try {
        const data = await readFile("../../puzzles.txt", "utf-8");
        let puzzles = data.split("\n"),
            totalTime = 0,
            puzzleCount = 0,
            totalGuesses = 0;

        puzzles.forEach(puzzle => {
            puzzleCount++;

            let g = new Grid(puzzle.trim()),
                solver = new Solver(g),
                start;

            console.log(g.toString());

            start = Date.now();
            solver.solve();
            let time = Date.now() - start;
            totalTime += time
            totalGuesses += solver.guesses;
            if (g.isSolved()) {
                console.log(g.toString());
                console.log("solved in " + (time) + "ms with " + solver.guesses + " guesses.");
            } else {
                console.log("Couldn't solve it.");
                console.log(g.toString());
            }
            console.log("\n");
        });

        console.log("Solved " + puzzleCount + " in avg " + Math.round(totalTime / puzzleCount) + " ms. Total time :" + totalTime + "ms");
        console.log("Had to make " + totalGuesses + " guesses");
    } catch (err) {
        console.error("Failed to load puzzles...", err);
    }
})();
