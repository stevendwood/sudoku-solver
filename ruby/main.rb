text = File.open('../puzzles.txt').read
text.each_line do |line|
    grid = Grid.new(line)
end