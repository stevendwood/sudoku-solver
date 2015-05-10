package org.woody.sudoku;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader buf = null;
		int totalGuesses = 0;
		long totalTime = 0;
		int puzzleCount = 0;
		try {
			buf = new BufferedReader(new FileReader("../hard-puzzles.txt"));
			String currentLine;
			while ((currentLine = buf.readLine()) != null) {
				puzzleCount++;
				Grid grid = new Grid(currentLine);
				System.out.println(grid);
				long start = System.currentTimeMillis();
				Solver s = new Solver(grid);
				s.solve();
				long took = (System.currentTimeMillis() - start);
				totalTime += took;
				System.out.println(grid);
				System.out.println("Solved in "+took+"ms. with "+s.getGuesses() + " guesses");
				totalGuesses += s.getGuesses();
			}
			
			System.out.println("Solved in avg "+Math.round(totalTime / puzzleCount)+" ms.");
			System.out.println("Had to make "+totalGuesses+ " guesses");
		} finally {
			buf.close();
		}
		
	}
	
	
}
