class Grid

    attr_accessor :rows

    def initialize(input_str)
        @rows = []
        row_idx = 0
        until input_str.length == 0 do
            row = input_str.slice!(0..8)
            current_row = []
            if ! row.include? "\n"
                row_idx += 1
                for col in 0..8
                    value = row[col]
                    value = value == "." ? 0 : value.to_i
                    current_row << Cell.new(row_idx, col, value)
                end
                @rows << current_row
            end
        end
    end

    def to_s
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
  attr_accessor :value, :possible_values

  # read only
  attr_reader :row, :col

  def initialize(row, col, value)  
    # Instance variables  
    @row = row
    @col = col
    @value = value
    @possible_values = []
  end

  def to_s
    if @value == 0
        return '.'
    end
    return @value.to_s
  end
end