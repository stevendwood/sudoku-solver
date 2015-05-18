require_relative 'grid'


text = File.open('../puzzles.txt').read
text.each_line do |line|
    grid = Grid.new(line)
    puts grid
    puts
end