class Grid

    def initialize(input_str)
       
    end

class Cell  
  attr_accessor :value

  attr_reader :row, :col

  def initialize(row, col, value)  
    # Instance variables  
    @row = row
    @col = col
    @value = value  
  end 
end  