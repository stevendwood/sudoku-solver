package org.woody.sudoku;

import java.util.ArrayList;
import java.util.List;


public class Cell {

	private int row;
	
	private int col;
	
	private int value;
	
	private List<List<Cell>> subgrid = null;
	
	private List<Cell> peers = null;
	
	private List<Integer> possibleValues = new ArrayList<>();
	
	public Cell(int row, int col, int value) {
		this.row = row;
		this.col = col;
		this.value = value;
	}

	public int getRow() {
		return row;
	}

	public void setRow(int row) {
		this.row = row;
	}

	public int getCol() {
		return col;
	}

	public void setCol(int col) {
		this.col = col;
	}

	public int getValue() {
		return value;
	}

	public void setValue(int value) {
		this.value = value;
	}

	public List<Integer> getPossibleValues() {
		return possibleValues;
	}

	public void setPossibleValues(List<Integer> possibleValues) {
		this.possibleValues = possibleValues;
	}
	
	public List<Cell> getPeers() {
		return peers;
	}

	public void setPeers(List<Cell> peers) {
		this.peers = peers;
	}

	public List<List<Cell>> getSubgrid() {
		return subgrid;
	}

	public void setSubgrid(List<List<Cell>> subgrid) {
		this.subgrid = subgrid;
	}
	
	@Override
	public boolean equals(Object that) {
		if (that instanceof Cell) {
			Cell other = (Cell) that;
			return other.row == this.row && other.col == this.col;
		}
		
		return false;
	}
	
	@Override
	public String toString() {
		return this.value == 0 ? "." : Integer.toString(this.value);
	}
	
}
