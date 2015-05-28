package org.woody.sudoku;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Solver {
    
    private Grid grid;
    
    private List<Cell> solvedCells = new ArrayList<>();
    
    private int guesses = 0;
    
    public Solver(Grid grid) {
        this.grid = grid;
    }
    
    public void solve() {
        // work out what the set of possible values is for each unsolved cell.
        this.initPossibleValues();
        // if there are any with only one possible value, set it.
        this.findCellsWithOnePossibleValue();
        // find any cells that have a possible value that doesn't occur
        // anywhere else in the column, row or subgrid it's in
        this.findUniqueValuesInUnits(null);
        if (!this.grid.isSolved()) {
            // this is a more tricky puzzle, so start searching for a solution.
            this.search();
        }
    }
    
    private void search() {
        Cell cell = Collections.min(this.grid.unsolved(), (x, y) -> {
            int xVal = x.getPossibleValues().size() * 100 + (x.getRow() + x.getCol()),
            	yVal = y.getPossibleValues().size() * 100 + (y.getRow() + y.getCol());
            
            return xVal - yVal;
        });
        
        for (int value : cell.getPossibleValues()) {
            // remember how many cells we had solved before we begin incase
            // we need to unwind
            int numSolved = this.solvedCells.size();
            this.guesses += 1;
            
            try {
                this.setValueForCell(cell, value);
                if (!this.grid.isSolved()) {
                    // no luck, keep looking...
                    this.search();
                }
            } catch (DeadEnd inconsistency) {
                // backtrack...
                HashSet<Cell> resetPossibilities = new HashSet<>();
                List<Cell> removals = this.solvedCells.subList(numSolved, this.solvedCells.size());
                
                removals.forEach(c -> {
                    c.setValue(0);
                    resetPossibilities.add(c);
                    resetPossibilities.addAll(this.grid.peers(c));
                });
                
                this.solvedCells = new ArrayList<Cell>(this.solvedCells.subList(0, numSolved));
                this.initPossibleValues(resetPossibilities.stream()
                		.filter(x -> x.getValue() == 0)
                		.collect(Collectors.toList()));
            }
        }
        if (!this.grid.isSolved()) {
            // If we get here then we're also stuck since we haven't found a
            // solution despite trying
            // all possible values for a cell.
            throw new DeadEnd("Tried all values for this cell  ["
            		+ cell.getRow() + ", " + cell.getCol() + "]"
            		+ cell.getPossibleValues());
        }
    }
    
    private void initPossibleValues() {
        this.initPossibleValues(this.grid.unsolved());
    }
    
    private void initPossibleValues(List<Cell> cells) {
        /* 
            Initialise the possible values for the provided list of cells or
            all the unsolved cells in the grid if no list was provided.

            To do this we collect the "peers" for each cell (cells not marked . for the cell c):

            x x x | . . . | . . .
            5 c x | x x 2 | x 9 x
            x x 3 | . . . | . . .
            ------+-------+------
            . x . | . . . | . . .
            . x . | . . . | . . .
            . x . | . . . | . . .
            ------+-------+------
            . x . | . . . | . . .
            . 7 . | . . . | . . .
            . x . | . . . | . . .

            Remove from the peers any unsolved cells, then exclude from the list 1..9 any 
            numbers already present in the list of solved peers. e.g. in the above grid assuming
            that any cell containing an x or a number is a peer of c and that the cells containing
            the numbers are solved then the possible values for "c" are:

            [1, 2, 3, 4, 5, 6, 7, 8, 9] - [5, 3, 2, 9, 7] = [8, 1, 4, 6]

        */
        cells.forEach(cell -> {
            List<Integer> peerValues = this.grid.peers(cell).stream()
            		.filter(peerCell -> peerCell.getValue() != 0)
            		.map(peerCell -> peerCell.getValue())
            		.collect(Collectors.toList());
            
            List<Integer> possibleValues = Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9)
            		.filter(d -> !peerValues.contains(d))
            		.collect(Collectors.toList());
            
            cell.setPossibleValues(possibleValues);
        });
    }
    
    private void removeValueFromPeers(Cell cell) {
        // Summary:
        // Remove the value of cell from the possible values of
        // it's peers.
        this.grid.peers(cell)
        	.stream()
        	.filter(x -> x.getValue() == 0)
        	.forEach(p -> {
	            List<Integer> possibleValues = p.getPossibleValues();
	            // .remove(int) will remove at that index, need to
	            // make sure remove(Object) is called.
	            possibleValues.remove(new Integer(cell.getValue()));
	            
	            if (possibleValues.size() == 0) {
	                throw new DeadEnd("No possible values for cell ["
	                + p.getRow() + ", " + p.getCol() + "] "
	                + p.getValue());
	            }
	        });
    }
    
    private void setValueForCell(Cell cell, int value) {
        List<Cell> peers = this.grid.peers(cell);
        
        if (peers.stream().anyMatch(x -> x.getValue() == value)) {
            throw new DeadEnd("Tried to set a value that already exists in peers");
        }
        
        cell.setValue(value);
        cell.setPossibleValues(new ArrayList<>());
        this.solvedCells.add(cell);
        this.removeValueFromPeers(cell);
        this.findCellsWithOnePossibleValue(peers);
        this.findUniqueValuesInUnits(cell);
    }
    
    private void findCellsWithOnePossibleValue() {
        this.findCellsWithOnePossibleValue(this.grid.unsolved());
    }
    
    private void findCellsWithOnePossibleValue(List<Cell> cells) {
        cells.forEach(cell -> {
            int value = cell.getValue();
            List<Integer> possibleValues = cell.getPossibleValues();
            
            if (value == 0 && possibleValues.size() == 1) {
                this.setValueForCell(cell, possibleValues.get(0));
            }
        });
    }
    
    private List<Cell> flattenSubGrid(List<List<Cell>> subgrid) {
        // A "subgrid" being a 3x3 square in a grid, it's modelled
        // as:
        //
        // [[Cell, Cell, Cell],
        // [Cell, Cell, Cell],
        // [Cell, Cell, Cell]]
        //
        // This method will return a flat list:
        // [Cell, Cell, Cell, Cell....]
        //
        return subgrid.stream()
        		.flatMap(s -> s.stream())
        		.collect(Collectors.toList());
    }
    
    private void findUniqueValuesInUnits(Cell cell) {
        
        if (cell != null) {
            Arrays.asList(this.grid.sameColAs(cell),
            			  this.grid.sameRowAs(cell),
            			  this.flattenSubGrid(this.grid.sameSubGridAs(cell)))
            	.forEach(this::findUniquePossibiltyInUnit);   
        } else {
        	Arrays.asList(this.grid.columns(), this.grid.rows())
        		  .forEach(units -> units.forEach(this::findUniquePossibiltyInUnit));
        	this.grid.subgrids().forEach(sg -> {
        		this.findUniquePossibiltyInUnit(this.flattenSubGrid(sg));
        	});
        }
    }
    
    private void findUniquePossibiltyInUnit(List<Cell> unit) {
        unit.stream()
        	.filter(x -> x.getValue() == 0)
        	.forEach(unsolvedCell -> {
        		List<Integer> otherCellsPossValues = unit.stream()
        				.filter(c -> !c.equals(unsolvedCell))
        				.map(c -> c.getPossibleValues())
        				.flatMap(listStream -> listStream.stream())
        				.collect(Collectors.toList());
            
                List<Integer> unique = unsolvedCell.getPossibleValues().stream()
            		.filter(x -> !otherCellsPossValues.contains(x))
            		.collect(Collectors.toList());
            
            if (unique.size() == 1) {
                this.setValueForCell(unsolvedCell,
                unique.get(0));
            }
        });
    }
    
    public int getGuesses() {
        return this.guesses;
    }
    
    /* Unchecked exception so it can be thrown from lambda */
    public static class DeadEnd extends RuntimeException {
        
        public DeadEnd(String message) {
            super(message);
        }
        
    }
    
}