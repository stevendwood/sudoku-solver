require 'set'

class Solver

    attr_accessor :guesses

    def initialize(grid)
        @grid = grid
        @guesses = 0
        @solved_cells = []
        @digits = (1..9).to_a
    end

    def solve
        # work out what the set of possible values is for each unsolved cell.
        init_possible_values(nil)
        # if there are any with only one possible value, set it.
        find_cells_with_one_possible_value(@grid.unsolved)
        # find any cells that have a possible value that doesn't occur
        # anywhere else in the column, row or subgrid it's in
        find_unique_values_in_units(nil)
        unless @grid.is_solved?
            # this is a more tricky puzzle, so start searching for a solution.
            search
        end
    end

    def search
        # pick the cell with least possible values (more chance of guessing correctly)
        cell = @grid.unsolved.min { |x, y| x.possible_values.length * 100 + (x.row + x.col) <=> y.possible_values.length * 100 + (y.row + y.col) }
        cell.possible_values.each do |value|        
            # remember how many cells we had solved before we begin incase
            # we need to unwind
            num_solved = @solved_cells.length
            @guesses += 1

            begin
                set_value_for_cell(cell, value)
                unless @grid.is_solved?
                    # no luck, keep looking...
                    search   
                end                   
                
            rescue Exception => inconsistency
                reset_possibilities = []
                @solved_cells.slice!(num_solved, @solved_cells.length - num_solved)
                                    .each do |cell|  
                                        cell.value = 0;
                                        reset_possibilities << cell
                                        reset_possibilities.concat(@grid.peers(cell).to_a)
                                    end

                init_possible_values(reset_possibilities.select { |x| x.value == 0 }.to_set)
            end
        end

        unless @grid.is_solved?
            # If we get here then we're also stuck since we haven't found a solution despite trying
            # all possible values for a cell.
            raise "Tried all values for this cell  [#{cell.row},  #{cell.col}]"
        end
    end

    def init_possible_values(cells)
        if cells.nil?
            cells = @grid.unsolved
        end

        cells.each do |cell| 
            #puts "peers length is #{@grid.peers(cell).length}"
            peer_values = @grid.peers(cell).select {|x| x.value != 0 }.map { |x| x.value }
           # puts "Peer values is #{peer_values}"
            cell.possible_values = @digits.select { |d| !peer_values.include? d }
          #  puts "Possible values #{cell.possible_values} for #{cell.row}, #{cell.col}"
        end
    end

    def remove_value_from_peers(cell)
        # Summary:
        # Remove the value of cell from the possible values of 
        # it's peers.
        @grid.peers(cell)
            .select { |x| x.value == 0 }
            .each do |p| 
                p.possible_values.delete_if { |v| v == cell.value }
                if p.possible_values.length == 0
                    raise "No possible values for cell [#{p.row} , #{p.col}], having set #{cell.row}, #{cell.col}"
                end
            end
    end

    def set_value_for_cell(cell, value)
        peers = @grid.peers(cell)
           
        if peers.any? { |x| x.value === value }
            raise "Tried to set a value for #{cell.row}, #{cell.col} that already exists in peers #{value}"
        end
            
        cell.value = value
        cell.possible_values = []
        @solved_cells << cell
        remove_value_from_peers(cell)
        find_cells_with_one_possible_value(peers)
        find_unique_values_in_units(cell)
    end
        
    def find_cells_with_one_possible_value(cells)
        if cells.nil?
            cells = @grid.unsolved
        end
        
        cells.each do |cell| 
            if cell.value == 0 and cell.possible_values.length == 1
                set_value_for_cell(cell, cell.possible_values[0])
            end
        end
    end

    def find_unique_values_in_units(cell) 
        unless cell.nil?
            [@grid.same_sub_grid_as(cell).flatten,
             @grid.same_col_as(cell),
             @grid.same_row_as(cell)].each { |unit| find_unique_possibilty_in_unit(unit) }
        else
            subgrids = []
            @grid.subgrids.each { |sg| subgrids << sg.flatten }
            [subgrids, @grid.columns, @grid.rows].each do |list_of_units|
                list_of_units.each { |unit| find_unique_possibilty_in_unit(unit) }
            end
        end
    end

    def find_unique_possibilty_in_unit(unit)
        unsolved = unit.select { |x| x.value == 0 }
        unsolved.each do |unsolved_cell| 
            other_cells_poss_values = unit
                    .select { |c| c != unsolved_cell and c.value == 0 }
                    .map { |c| c.possible_values }
                    .flatten
               
            unique = unsolved_cell.possible_values.select { |x| !(other_cells_poss_values.include?(x)) }

            if (unique.length === 1)
                set_value_for_cell(unsolved_cell, unique[0])         
            end
        end
    end
end


                       