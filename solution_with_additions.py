#import timing

'''
# Uncertainty with global variables and ease of use: chose to use function to get all the 'constant' variables
def all_variables(): # NOT IN USE
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)
    
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    diagonal_one = [diagonal(rows, cols)] # diagonal starting from box A1
    diagonal_two = [diagonal(''.join(rows), ''.join(reversed(cols)))] # diagonal starting from box A9
    diagonal_units = diagonal_one + diagonal_two # combining units for both diagonals
    unitlist = row_units + column_units + square_units + diagonal_units # adding diagonal elements to unitlist
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    
    return boxes, unitlist, units, peers, rows, cols
'''

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # prints for debugging
    # display(values)
    # print("\n" + box + "\n" + value) 

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    #print(assignments) # testing purposes
    return values
    

def cross(A, B):
    "Cross product of elements in A and elements in B."  
    return [a+b for a in A for b in B]
    

def diagonal(A, B):
    "Building the diagonal with the elements in A and elements in B."  
    return [A[i]+B[i] for i in range(0,9)]
    

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    
    #[boxes, unitlist, units, peers, rows, cols] = all_variables()
    
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    #display(dict(zip(boxes, chars))) # for testing purposes
   
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    
    #[boxes, unitlist, units, peers, rows, cols] = all_variables()
    
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return    
    

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    
    #[boxes, unitlist, units, peers, rows, cols] = all_variables()
    
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            #if (len(values[peer]) > 1): # added if, not to replace values that are already set, in non-diagonal matrices
                #values[peer] = values[peer].replace(digit,'') # COMMENTED OUT FOR assignments usage
                #display(values) # for debugging purposes
                #print("\n") # for debugging purposes
            values = assign_value(values, peer, values[peer].replace(digit,'')) # assignments usage
    return values
    

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    #[boxes, unitlist, units, peers, rows, cols] = all_variables()

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit # COMMENTED OUT FOR assignments usage
                values = assign_value(values, dplaces[0], digit)
    return values
    

def naked_twins(values): 
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    """
    OVERALL STRUCTURE:
    Initialization:
        Make a list of sudoku cells that contain string with len(str) == 2 (twin_values)
        Go through the twin_values list: Make another list of naked twins 
            Cell belongs to naked_tw list if it is one of the peers of the cell in twin_values list and of equal value
        Identify the relevant peers within the relevant units
            [NOTE: Crucial to identify and handle situations in which different naked twin pairs overlap over different units]
    Replacement:
        Go through the relevant_peers and 
        eliminate included digits from other peers within the same relevant unit (excluding the twin, though)
            [NOTE: if eliminate() function would be run after the naked_twins(): possible need to add 'len(values[peer]) > 1' to if statement in replacement]
    """
    
    # Get all the variables
    #[boxes, unitlist, units, peers, rows, cols] = all_variables()
    
    #INITIALIZATION
    # First gather all the cells with two digits (len == 2)
    twin_values = [box for box in values.keys() if len(values[box]) == 2] 
    # Find the naked twins amongst the twin_values and the peers
    naked_tw = [ref_box for box in twin_values for ref_box in peers[box] if values[ref_box] == values[box]]
    #getting the relevant units: those which contain naked twins
    relevant_units = [unit for box in twin_values for ref_box in peers[box] for unit in unitlist if (values[ref_box] == values[box] and ref_box in unit and box in unit)]
    #print(naked_tw) # for testing purposes
    #print(relevant_units) # for testing purposes
    for nt in naked_tw: # go through the naked twins
        #relevant peers are those which belong to the same unit as both of the naked twins
        relevant_peers = [peer for unit in relevant_units for twin in naked_tw for peer in unit if (twin != nt and values[twin] == values[nt] and nt in unit and twin in unit)]
        relevant_peers = list(set(relevant_peers)) # remove duplicates from the list by converting it to set and then back to list
        #print(relevant_peers) #for debugging purposes
        '''
        # for-loop-structure (now commented out, same result as list comprehension above) 
        relevant_peers = [] # initializing relevant_peers list
        for unit in relevant_units: # identify the relevant units 
            for twin in naked_tw:
                if (twin != nt and values[twin] == values[nt] and nt in unit and twin in unit): # compare 'twin' to 'nt'
                    for peer in unit: # if comparison was successful add the peers of the unit to the relevant_peers list
                        relevant_peers.append(peer)
        #print(relevant_peers) #for debugging purposes
        '''  
        #REPLACEMENT
        for peer in relevant_peers:   
            if (not values[peer] == values[nt]): # and len(values[peer]) > 1): # quick-fix
                for digit in values[nt]: # go through the digits in the naked twin
                    if digit in values[peer]: # if digit is found within the peer proceed to replace it with ''
                        #values[peer] = values[peer].replace(digit,'') # remove the found digit from the peer, COMMENTED OUT: assign_value
                        values = assign_value(values, peer, values[peer].replace(digit,'')) # assign_value usage
    return values


def board_validation(values): # NOT IN USE
    """
    Additional check up, where units are reviewed after each full iteration.
    If two same single digits are found within same unit, return True.
    Otherwise all is well, and return False.
    """
    #[boxes, unitlist, units, peers, rows, cols] = all_variables()
    
    single_digits = [box for box in values.keys() if len(values[box]) == 1]
    for box in single_digits:
        for peer in peers[box]:
            if (values[box] == values[peer]):
                return True
    
    return False


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice() [TK: and naked_twins()]. 
    If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    
    #[boxes, unitlist, units, peers, rows, cols] = all_variables()
    
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values) 
        #display(values) # added for testing
        values = only_choice(values)
        #display(values) # added for testing
        values = naked_twins(values) # Added naked twins algorithm        
        #display(values) # added for testing
        #if (board_validation(values)):  # Separate validation for duplicate values within units
        #    return False                # if validation didn't pass, return false
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."

    #[boxes, unitlist, units, peers, rows, cols] = all_variables()

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False: # returns false if reduze_puzzle returns false: meaning sudoku has cells with len == 0 [NOT IN USE: or board validation failed]
        return False 
    if all(len(values[s]) == 1 for s in boxes): # indicates that sudoku is solved
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = search(grid_values(grid))
    return values


# Global variables
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_one = [diagonal(rows, cols)] # diagonal starting from box A1
diagonal_two = [diagonal(''.join(rows), ''.join(reversed(cols)))] # diagonal starting from box A9
diagonal_units = diagonal_one + diagonal_two # combining units for both diagonals
unitlist = row_units + column_units + square_units + diagonal_units # adding diagonal elements to unitlist
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# End of global variables


if __name__ == '__main__':
    
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3' # original diagonal sudoku
    # additional test cases 
    #diag_sudoku_grid = '.......39....1...5..3..58....8..9..6.7..2....1..4.......9..8.5..2....6..4..7.....' # golden nugget, NON-diagonal
    #diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................' # submit test sudoku, OK
    #diag_sudoku_grid = '.....3.5..........6781..3.................................192.4.1..5.7.....827...' # submit test sudoku2, runs too long!
    #diag_sudoku_grid = '..4....7.5..37..6.1.7...3.5..............7.1..........6......4.2....6........9...' # submit test sudoku3, runs too long!
    #diag_sudoku_grid = '.....1.........4......5..8.8........375418629.24........8.......4.....3.7....25..' # submit test sudoku4, runs too long!
    #diag_sudoku_grid = '96......7.....92.54.................64..25.8.......5....9.....2...9.............3' # submit test sudoku5, runs too long!
    diag_sudoku_grid = '....56...................6.....1..45...6..92......46...3..6.....6......3....9.8.6' # submit test sudoku6, runs too long!  
        
    display(solve(diag_sudoku_grid))

    
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
        
