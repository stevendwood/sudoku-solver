package org.woody.sudoku.tests;

import junit.framework.TestCase;

import org.woody.sudoku.Grid;
import org.woody.sudoku.Cell;


public class GridTest extends TestCase {

	private Grid grid = null;
	
	public void setUp() {
		String gridData = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......";
		grid = new Grid(gridData);
	}
	
	public void testThereAreNineSubgrids() {
		assertEquals(grid.subgrids().size(), 9);
		
	}
	
	public void testThereAreNineRows() {
		assertEquals(grid.rows().size(), 9);
		grid.rows().forEach(cells -> assertEquals(cells.size(), 9));
		
	}
	
	public void testThereAreNineColumns() {
		assertEquals(grid.columns().size(), 9);
		grid.columns().forEach(cells -> assertEquals(cells.size(), 9));
	}
	
	public void testSubGridStructure() {
		grid.subgrids().forEach(sg -> {
			assertEquals(sg.size(), 3);
			sg.forEach(cells -> {
				assertEquals(cells.size(), 3);
			});
		});
	}
	
	public void testNumberOfPeers() {
		for (int i=0; i<9; i++) {
			for (int j=0; j<9; j++) {
				Cell cell = grid.rows().get(i).get(j);	
				assertEquals(grid.peers(cell).size(), 20);
			}
		}
		
	}
	
}
