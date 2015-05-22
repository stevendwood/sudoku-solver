
require 'set'

class Grid

    attr_accessor :rows

    def initialize(input_str)
        @rows = []
        @cols = []
        @grids = []
        row_idx = 0
        until input_str.length == 0 do
            row = input_str.slice!(0..8)
            current_row = []
            if ! row.include? "\n"
                
                for col in 0..8
                    value = row[col]
                    value = value == "." ? 0 : value.to_i
                    current_row << Cell.new(row_idx, col, value)
                end

                row_idx += 1
                @rows << current_row
            end
        end
    end

    def same_row_as(cell) 
       return @rows[cell.row]
    end

    def same_col_as(cell)
        return columns[cell.col]
    end

    def _sub_grid_idx(x)
        if x <= 2
            return 0
        elsif x <= 5
            return 3
        else
            return 6
        end 
    end

    def is_solved?
        return ! @rows.flatten.any? { |x| x.value == 0 }
    end

    def same_sub_grid_as(cell)
        if cell.subgrid.nil?
            start_row = _sub_grid_idx(cell.row)
            start_col = _sub_grid_idx(cell.col)
            subgrid = []
            (start_row..start_row+2).each do |i|
                row = @rows[i]
                sub_grid_row = []
                (start_col..start_col+2).each { |j| sub_grid_row << row[j] }
                subgrid << sub_grid_row
            end           
            cell.subgrid = subgrid; 
        end

        return cell.subgrid
    end

    def subgrids
        if @grids.length == 0
            (0..8).step(3).each do |i| 
                (0..8).step(3).each { |j| @grids << same_sub_grid_as(Cell.new(i, j, 0)) }
            end
        end
        return @grids;
    end

    def unsolved
        return @rows.flatten.select {|c| c.value == 0}
    end

    def columns
        if @cols.length == 0
            for idx in 0..8
                @cols << []
            end
            @rows.each do |row|
                row.each_with_index { |cell, idx| @cols[idx] << cell }
            end
        end

        return @cols
    end

    def peers(cell)
        if cell.peers.nil?
            # concatenate all cells in the same row, column and sub grid, then flatten them
            # and remove the argument cell, should produce a list of 20 cells.
            cell.peers = [].concat(same_row_as(cell))
                        .concat(same_col_as(cell))
                        .concat(same_sub_grid_as(cell).flatten)
                        .select { |x| x != cell }
                        .to_set
        end
        return cell.peers
    end

    def to_s 
        #Provide a string representation of a grid.
        output = ""
        for row in 0..@rows.length-1
            if row != 0 && row % 3 == 0
                output += "---------+---------+---------\n"
            end

            current_row = @rows[row];
            for col in 0..8
                if col != 0 && col % 3 == 0
                    output += "|"
                end
                output = output + " " + current_row[col].to_s + " "
            end
            output += "\n"
        end

        return output;
        
    end
end

class Cell
  # getter and setter
  attr_accessor :value, :possible_values, :row, :col, :subgrid, :peers

  # read only
  attr_reader :row, :col

  def initialize(row, col, value)  
    # Instance variables  
    @row = row
    @col = col
    @value = value
    @possible_values = []
    @subgrid
    @peers
  end

  def to_s
    if @value == 0
        return '.'
    end
    return @value.to_s
  end
end