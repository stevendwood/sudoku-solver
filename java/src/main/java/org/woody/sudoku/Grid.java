package org.woody.sudoku;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
* Models a Sudoku game.  This is a list of lists of cells unsurprisingly.
*
* Provides methods that a solver can use to find all the peers of a cell,
* all the cells in the same column as another cell and that sort of thing...
*
*
* @author stevenwood
*
*/
public class Grid {
    
    private List<List<Cell>> rows;
    
    private List<List<Cell>> columns = null;
    // 3x3 sub grids.
    private List<List<List<Cell>>> grids = null;
    
    public Grid(String inputStr) {
        this.rows = new ArrayList<List<Cell>>(9);
        ArrayList<Cell> currentRow = null;
        for (int idx = 0, l = inputStr.length(); idx < l; idx++) {
            if (idx % 9 == 0) {
                currentRow = new ArrayList<Cell>(9);
                this.rows.add(currentRow);
            }
            
            int value = Character.getNumericValue(inputStr.charAt(idx));
            if (value == -1) {
                value = 0;
            }
            currentRow.add(new Cell(this.rows.size() - 1, currentRow.size(),
            value));
        }
    }
    
    public List<List<Cell>> columns() {
        if (this.columns == null) {
            this.columns = new ArrayList<List<Cell>>(9);
            for (int i = 0; i < 9; i++) {
                this.columns.add(new ArrayList<Cell>(9));
            }
            this.rows.forEach(row -> {
                IntStream.range(0, row.size()).forEach(idx -> {
                    this.columns.get(idx).add(row.get(idx));
                });
            });
        }
        
        return this.columns;
    }
    
    public List<List<Cell>> rows() {
        return this.rows;
    }
    
    public List<Cell> sameRowAs(Cell cell) {
        return this.rows.get(cell.getRow());
    }
    
    public List<Cell> sameColAs(Cell cell) {
        return this.columns().get(cell.getCol());
    }
    
    public List<Cell> unsolved() {
        /*
        * Get all the cells in this Grid that are unsolved
        */
        List<Cell> unsolved = new ArrayList<Cell>();
        this.rows.forEach(row -> {
            unsolved.addAll(row.stream().filter(cell -> cell.getValue() == 0)
            .collect(Collectors.toList()));
        });
        
        return unsolved;
    }
    
    public List<List<Cell>> sameSubGridAs(Cell cell) {
        
        /*
        Get all the cells in the same "sub grid" as the given cell. e.g. for
        the cell "c" below the cells in the "same_sub_grid" (which are marked
        x below) are returned along with the argument cell.
        
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
        if (cell.getSubgrid() == null) {
            
            int startRow = subgridIndex(cell.getRow()), startCol = subgridIndex(cell
            .getCol());
            List<List<Cell>> subgrid = new ArrayList<List<Cell>>(3);
            for (int i = startRow; i < startRow + 3; i++) {
                List<Cell> row = this.rows.get(i);
                List<Cell> subGridRow = new ArrayList<Cell>(3);
                for (int j = startCol; j < startCol + 3; j++) {
                    subGridRow.add(row.get(j));
                }
                
                subgrid.add(subGridRow);
            }
            cell.setSubgrid(subgrid);
        }
        
        return cell.getSubgrid();
    }
    
    @Override
    public String toString() {
        String output = "";
        for (int i = 0; i < this.rows.size(); i++) {
            if (i != 0 && i % 3 == 0) {
                output += "---------+---------+---------\n";
            }
            
            List<Cell> currentRow = this.rows.get(i);
            for (int j = 0; j < currentRow.size(); j++) {
                if (j != 0 && j % 3 == 0) {
                    output += "|";
                }
                
                output += " " + currentRow.get(j).toString() + " ";
            }
            
            output += "\n";
        }
        
        return output;
    }
    
    public List<Cell> peers(Cell cell) {
        /*
        Get the peers for the cell. The peers for the cell "c" are
        pictorially represented below by the cells marked "x"
        
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
        if (cell.getPeers() == null) {
            List<Cell> peers = new ArrayList<Cell>();
            
            peers.addAll(this.sameColAs(cell));
            peers.addAll(this.sameRowAs(cell));
            this.sameSubGridAs(cell).forEach(peers::addAll);
            
            ArrayList<Cell> peersList = new ArrayList<>();
            peersList
            .addAll(new HashSet<Cell>(peers.stream()
            .filter(x -> !x.equals(cell))
            .collect(Collectors.toList())));
            cell.setPeers(peersList);
        }
        
        return cell.getPeers();
    }
    
    public boolean isSolved() {
        for (int i = 0; i < this.rows.size(); i++) {
            for (int col = 0; col < 9; col++) {
                if (this.rows.get(i).get(col).getValue() == 0) {
                    return false;
                }
            }
        }
        return true;
    }
    
    public List<List<List<Cell>>> subgrids() {
        if (this.grids == null) {
            this.grids = new ArrayList<List<List<Cell>>>(9);
            for (int i = 0; i < 9; i += 3) {
                for (int j = 0; j < 9; j += 3) {
                    this.grids.add(this.sameSubGridAs(new Cell(i, j, 0)));
                }
            }
        }
        
        return this.grids;
    }
    
    private int subgridIndex(int x) {
        if (x <= 2) {
            return 0;
            } else if (x <= 5) {
            return 3;
            } else {
            return 6;
        }
    }
    
}