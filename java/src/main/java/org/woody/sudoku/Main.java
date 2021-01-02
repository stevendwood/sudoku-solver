package org.woody.sudoku;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.stream.Collectors;
import java.util.List;

public class Main {

	public static void main(String[] args) throws IOException {
		 
		try (BufferedReader buf = new BufferedReader(new FileReader("puzzles.txt"))) {
			
			/* 
			 * All right so this is a bit over the top, but I'm doing this
			 * to learn about streams and map/reduce/collect and all that.
			 * Since there are 106 puzzles to solve and each solve operation
			 * is computationally independant, run them in parallel.
			 */
			List<SolveResult> results = 
				buf.lines()
				 //  .parallel()
				   .map(Main::solve)
				   .collect(Collectors.toList());
			
			results.forEach(result -> {
				System.out.println(result.solvedGrid);
				System.out.println("Solved in "+result.time+"ms. with "+result.guesses+" guesses.");
				System.out.println();
			});
			
			long totalTime = results.stream()
					.map(result -> result.time)
					.reduce((long) 0, (x, y) -> x + y);
			
			int totalGuesses = results
					.stream()
					.map(x -> x.guesses)
					.reduce(0, (x, y) -> x + y);
			
			System.out.println("Solved "+results.size()+" in avg "+(totalTime / (float) results.size())+" ms. Total time: "+totalTime+"ms");
			System.out.println("Had to make "+totalGuesses+ " guesses");
			
		} 
		
	}
	
	private static SolveResult solve(String puzzle) {
		Grid grid = new Grid(puzzle);
		long start = System.currentTimeMillis();
		Solver s = new Solver(grid);
		s.solve();
		return new SolveResult(grid, (System.currentTimeMillis() - start), s.getGuesses());
	}
	
	static class SolveResult {
		final int guesses;
		final long time;
		final Grid solvedGrid;
		
		public SolveResult(Grid solvedGrid, long time, int gueses) {
			this.guesses = gueses;
			this.time = time;
			this.solvedGrid = solvedGrid;
		}
	}
}
