require_relative 'grid'
require_relative 'solver'

total_guesses = 0
puzzle_count = 0
total_time = 0
text = File.open('../puzzles.txt').read
text.each_line do |line|
    total_guesses += 1
    puzzle_count += 1
    grid = Grid.new(line)
    puts grid
    solver = Solver.new(grid)
    start = Time.now
    solver.solve
    took = ((Time.now - start) * 1000).to_i
    total_time += took
    puts
    puts grid
    puts
    puts "solved in #{took}ms with #{solver.guesses} guesses."
    total_guesses += solver.guesses
    puts
end
puts
puts "Solved #{puzzle_count}  in avg #{(total_time / puzzle_count).to_i} ms. Total time  #{total_time}ms"
puts "Had to make #{total_guesses} guesses"

