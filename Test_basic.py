import solution

[boxes, unitlist, units, peers, rows, cols] = solution.all_variables()

#print(unitlist)

'''
values = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
solution.solve(values)
#values_return = solution.search(solution.grid_values(values))
#print(values_return)
#solution.display(values_return)

print("\n")
'''
# diagonal sudoku
values = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
solution.solve(values)
#values_return = solution.search(solution.grid_values(values))
#print(values_return)
#solution.display(values)

print("\n")

# Golden nugget
values = ".......39....1...5..3..58....8..9..6.7..2....1..4.......9..8.5..2....6..4..7....."
solution.solve(values)
#values_return = solution.search(solution.grid_values(values))
#print(values_return)
#solution.display(values)

print(unitlist)



# Trying out the assignments list
#solution.display(solution.assignments)


'''
#testing units

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = solution.cross(rows, cols)

row_units = [solution.cross(r, cols) for r in rows]
column_units = [solution.cross(rows, c) for c in cols]
square_units = [solution.cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_one = [solution.diagonal(rows, cols)] # diagonal starting from box A1
diagonal_two = [solution.diagonal(''.join(rows), ''.join(reversed(cols)))] # diagonal starting from box A9
diagonal_units = diagonal_one + diagonal_two # combining units for both diagonals
unitlist = row_units + column_units + square_units + diagonal_units # adding diagonal elements to unitlist

print(diagonal_units)
print(type(diagonal_units))
print(unitlist)
print(type(unitlist))

values = solution.search(solution.grid_values(values))

width = 1+max(len(values[s]) for s in boxes)
line = '+'.join(['-'*(width*3)]*3)
for r in rows:
    print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                  for c in cols))
    if r in 'CF': print(line)
'''