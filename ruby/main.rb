require_relative 'grid'


#text = File.open('../puzzles.txt').read
#text.each_line do |line|
#    grid = Grid.new(line)
#    puts grid
#end
grid_data = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
grid = Grid.new(grid_data)

puts grid
puts
puts grid.columns[0][8]
puts grid.rows[0]