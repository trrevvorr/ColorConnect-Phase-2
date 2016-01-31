# AI - CS 5400 - Sec 1A
# Puzzle Assignmet 1 - Phase 1
#
# Trevor Ross
# 01/27/2016
# from sys import argv
import sys
import copy
from Queue import Queue
import random
import time
start_time = time.time()

################################################################################
## CLASSES
################################################################################

# for use with printing pretty colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Node():
    """Tree node for State Tree"""
    def __init__(self, ID=None, parent_node=None, state=None, action=None):
        self.ID = ID # integer
        self.p_ID = parent_node # integer
        self.state = state # format: [[... row 1 ...], [... row 2 ...], ...]
        self.action = action # format: [c, x, y]
        # where x and y are in [-1, 0, 1] and x is the row move, y is the
        # col move, and c is the color
        self.path_cost = None # integer (depth of state in tree)

        self.path_heads = {} # dictionary containing the furthes a color path
        # has travled in the current state. format: {0:[r0,c0], 1:[r1,c1], ...}


class StateTree():
    """Creates a State Tree for all possible states of Puzzle"""
    def __init__(self, initial_puzzle, number_of_colors):
        # a globla ID index for creating unique node IDs
        self.ID = 0
        # create a root node
        self.root = Node(self.ID, state=initial_puzzle)
        self.num_colors = number_of_colors
        # find start and end locations of puzzle colors
        self.color_start = FindColorStart(self.root.state, self.num_colors)
        self.root.path_heads = self.color_start
        self.color_end = FindColorEnd(self.root.state, self.num_colors)
        self.root.path_cost = 0
        # dictionary of nodes indexed by their ID
        self.node_dict = {self.root.ID:self.root}

        # TIMING VARIABLES
        self.total_time_on_final = 0.0
        self.total_time_on_action = 0.0
        self.total_time_on_creation = 0.0
        self.total_time_on_result = 0.0
        self.BFTS_start_time = time.time()

    # PURPOSE: finds optimal solution to puzzle by using breadth first search
    # Each state is first enqued, in a FIFO queue. Later, the element will be
    # dequeued. Once it is dequeued, all it's valid moves will be found and
    # a child state will be created and enqueued for each one.
    # OUTPUT: either False or list of states leading to solution
    def BreadthFirstTreeSearch(self):
        self.BFTS_start_time = time.time()
        # queue will store the ID of the node, to get the node, look up the
        # ID in the node_dict
        queue = Queue()
        queue.put(self.root.ID)

        # loop until final state is found or queue is emptied
        while not queue.empty():
            # dequeue the front element
            to_examine = self.node_dict[queue.get()]
            # print '='*20
            # print '== PARENT =='
            # Visualize(to_examine.state)

            # retrive all valid actions from this color's path head
            valid_actions = self.Action(to_examine)
            valid_colors = valid_actions.keys()
            random.shuffle(valid_colors)
            # for color_num in valid_actions:
            #     print '%d:' % color_num, DirPrint(valid_actions[color_num]['action'])
            # iterate through colors in puzzle, checking for actions on each
            for color_num in valid_colors:
                # print '-- COLOR %d --' % color_num
                color_actions = valid_actions[color_num]['action']
                color_coords = valid_actions[color_num]['coord']
                # create a new child state for each valid action
                for i in xrange(len(color_actions)):
                    time_before_creation = time.time()
                    action = color_actions[i]
                    action_coord = color_coords[i]
                    self.ID += 1
                    # retulting child state from parent acted on by action
                    c_state = self.Result(to_examine.state, to_examine.path_heads[color_num], action)
                    # Visualize(c_state)
                    # create new node
                    action_coord.insert(0, color_num)
                    child = Node(ID=self.ID, parent_node=to_examine.ID, state=c_state, action=action_coord)
                    # updated the child's path heads
                    child.path_heads = to_examine.path_heads.copy()
                    child.path_heads[color_num] = action_coord[1:]
                    # update child's path cost
                    child.path_cost = to_examine.path_cost + 1
                    # add child to the dict
                    self.node_dict[child.ID] = child
                    # check if child is Goal State
                    colors_connected = self.VerifyFinal(child.state)
                    if colors_connected == True:
                        # a goal state has been found
                        # return the final state and it's ancestors
                        # self.EndSequence(True)
                        return (self.TraceBack(child))
                    # push child onto queue
                    queue.put(child.ID)
                    self.total_time_on_creation += (time.time() - time_before_creation)
        # queue is empty if loop breaks
        # self.EndSequence(False)
        return False

    # PURPOSE: give a node, return a list of valid actions
    # VALID MOVE DISQUALIFICATION: if one of the colors hits a dead end
    # A.K.A. it has no valid moves, no valid moves will be returned for any color
    # OUTPUT: dictionary with color nums as keys and their valid outputs
    def Action(self, to_examine):
        valid_actions = {} # format: {0:{action:[[0,1],...], 'coord':[[2,3],...]},...}

        # find which colors are already connected
        colors_connected = self.VerifyFinal(to_examine.state)
        # get a list of colors in puzzle and shuffle it
        color_numbers = range(self.num_colors)
        # trim down the list of numbers to colors action on
        # if the color is already connected, no further action needed on color
        for color in color_numbers:
            if color in colors_connected:
                color_numbers.remove(color)

        # iterate through remaining colors, finding actions for each
        random.shuffle(color_numbers)
        for color in color_numbers:
            coord = to_examine.path_heads[color]
            color_actions = self.ActionOnCoord(to_examine.state, coord)
            if len(color_actions['action']) == 0:
                # color path hit a dead end, this state is dead
                return {}
            else:
                # otherwise add it to a list to be returned
                valid_actions[color] = color_actions

        return valid_actions


    # PURPOSE: given a state, a coordinate, and an end_position, the function
    # will return a list of all valid moves.
    # VALID MOVE DISQUALIFICATION:
    # 1) moves out of puzzle's bounds
    # 2) moves onto a pre-existing line
    # 3) path moves adjacent to itself, aka, the path 'touches' itself
    # OUTPUT: returns a list of valid actions as well as the coordinates they result in
    # FORMAT: the 4 possible moves are: [[-1,0], [0,1], [1,0], [0,-1]]
    # Function returns a dict with 'action' being the key to the list of
    # valid actions. 'coord' is the key for valid coordinates
    def ActionOnCoord(self, p_state, coord):
        time_before_action_check = time.time()
        upper_bound = len(p_state)
        lower_bound = 0
        color =  int(p_state[coord[0]][coord[1]])
        end_coord = self.color_end[color]
        valid_actions = []
        valid_coords = []

        # actions in order: down, right, up, left
        action_options = [[-1,0], [0,1], [1,0], [0,-1]]
        random.shuffle(action_options)
        for action in action_options:
            new_row = coord[0]+action[0]
            new_col = coord[1]+action[1]
            # check if move is out-of-bounds
            if new_col < lower_bound or new_col == upper_bound:
                continue
            if new_row < lower_bound or new_row == upper_bound:
                continue
            # check if space is already occupied
            if p_state[new_row][new_col] != 'e':
                continue
            # check if move results in path becoming adjacent to itself
            adj_itself = 0
            for adj in action_options:
                adj_row = new_row+adj[0]
                adj_col = new_col+adj[1]
                # check if adjacent square is out-of-bounds
                if adj_col < lower_bound or adj_col == upper_bound:
                    continue
                if adj_row < lower_bound or adj_row == upper_bound:
                    continue
                if p_state[adj_row][adj_col] == str(color):
                    if [adj_row, adj_col] != end_coord:
                        adj_itself += 1
            if adj_itself > 1:
                continue
            # if move is in-bounds, space is not occupied, and path isn't
            # adjacent to itself, it is a valid move
            new_coord = [new_row, new_col]
            valid_actions.append(action)
            valid_coords.append(new_coord)

        self.total_time_on_action += (time.time() - time_before_action_check)
        return {'action':valid_actions, 'coord':valid_coords}

    # PURPSOSE: return the result of taking action on the coordinate of the
    # given state
    # OUTPUT: returns state in the form: [[... row 1 ...], [... row 2 ...], ...]
    def Result(self, p_state, coord, action):
        time_before_result = time.time()
        new_state = copy.deepcopy(p_state)
        # retrieve the 'color' of the path to be extended
        color_path_to_extend = p_state[coord[0]][coord[1]]
        # find the location to place the extention
        new_row = coord[0]+action[0]
        new_col = coord[1]+action[1]
        # 'color' the new loaction, extending the line
        new_state[new_row][new_col] = color_path_to_extend

        self.total_time_on_result += (time.time() - time_before_result)
        return new_state

    # PURPOSE: verify that the passed state is a final state
    # IF FINAL: return True
    # IF NOT FINAL: return a list of those colors who are final
    def VerifyFinal(self, pzzl_state):
        time_before_final_check = time.time()
        colors_connected = []
        upper_bound = len(pzzl_state)
        lower_bound = 0

        for color in self.color_end:
            # find the end point coordinats for color
            end = self.color_end[color]
            # if the endpoint is adjacent to the its color's path then colors are connected
            for direction in [[-1,0], [0,1], [1,0], [0,-1]]:
                adj_row = end[0]+direction[0]
                adj_col = end[1]+direction[1]
                # ignore if out-of-bounds
                if adj_col < lower_bound or adj_col == upper_bound:
                    continue
                if adj_row < lower_bound or adj_row == upper_bound:
                    continue

                if pzzl_state[adj_row][adj_col] == str(color):
                    # color has been connected
                    colors_connected.append(color)
                    break

        self.total_time_on_final += (time.time() - time_before_final_check)
        if len(colors_connected) == self.num_colors:
            # if all colors are connected, return true
            return True
        else:
            # otherwise return a list of the colors who are connected
            return colors_connected

    # PURPOSE: given the final node. find path from the final node to the root
    # OUTPUT: list of all the nodes from root to final. [root, ... , final]
    def TraceBack(self, end_node):
        node_path = []
        node = end_node
        # keep adding node to node_path until root node is found
        while node.action != None:
            # insert in front of list since traversal is bottom-up
            node_path.insert(0, node)
            # move to partent node
            node = self.node_dict[node.p_ID]
        # add the root
        node_path.insert(0, node)
        return node_path

    # PURPOSE: print out time and states statistics so program can be analized
    def EndSequence (self, sol_found):
        print '-- TIME --'
        print 'TOTAL:       ', (time.time() - self.BFTS_start_time)
        print 'FINAL CHECK: ', self.total_time_on_final
        print 'ACTION CHECK:', self.total_time_on_action
        print 'RESULT:      ', self.total_time_on_result
        print 'CREATION:    ', self.total_time_on_creation
        print '-- STATES --'
        print 'CREATED: ', self.ID
        print 'EXPANDED:', (self.node_dict[self.ID]).p_ID

    # PURPOSE: allows user to enter a state's ID and see the state
    # LOOP: loops infinatly until user enters anything but a number
    def StateLookup(self):
        print 'Enter Desired State ID to look up State'
        user_in = int(raw_input('>'))
        while True:
            state = self.node_dict[user_in]
            print 'State ID:', state.ID, 'Parent ID:', state.p_ID
            Visualize(state.state)
            user_in = int(raw_input('>'))


################################################################################
## FUNCTIONS
################################################################################

# PURPSOSE: reads in a puzzle file and parses the data for solving
# INPUT: first line: # rows/columns, # of colors
# the input puzzle will follow as a square matrix
# OUTPUT: returns a tuple with the number of colors and the puzzle as a 2D array
def ReadInput(pzzl_file):
    f_hand = open(pzzl_file)

    pzzl_array = []
    # read every line into pzzle_array (even first line)
    for line in f_hand:
        line = line.split()
        pzzl_array.append(line)
    # pop first line and store it's second element (num colors)
    first_line = pzzl_array.pop(0)
    num_colors = int(first_line.pop())

    f_hand.close()
    return (num_colors, pzzl_array)


# PURPOSE: given the puzzle and the number of colors to find, function will
# return a dict with the FIRST occurance of the number as the key and its
# coordinates as the value
# OUTPUT: dictionary in the format: {0:[r0,c0], 1:[r1,c1],...}
def FindColorStart(puzzle, num_colors):
    coordinates = {} # format: {0:[r0,c0], 1:[r1,c1],...} where r = row, c = col
    dim = len(puzzle)
    color_nums = range(num_colors) # list of all color numbers
    # find coordinate for each color start
    for row_i in xrange(dim):
        for col_i in xrange(dim):
            char_found = puzzle[row_i][col_i]
            if char_found == 'e':
                continue
            # if number has not been seen yet, it is the Start Position
            if int(char_found) in color_nums:
                num_found = int(char_found)
                # remove it from the list so it won't be found again
                color_nums.remove(num_found)
                coordinates[num_found] = [row_i, col_i]

    # error checking to make sure right number of colors were found
    if len(coordinates) != num_colors:
        print 'ERROR: PROBLEMS FINDING COLORS'
        print 'COORDINATES: %r' % coordinates
        print 'START COLORS TO BE FOUND: %r' % range(num_colors)
        exit(1)

    return coordinates


# PURPOSE: given the puzzle and the number of colors to find, function will
# return a dict with the LAST occurance of the number as the key and its
# coordinates as the value
# OUTPUT: dictionary in the format: {0:[r0,c0], 1:[r1,c1],...}
def FindColorEnd(puzzle, num_colors):
    coordinates = {} # format: {0:[r0,c0], 1:[r1,c1],...}  where r = row, c = col
    dim = len(puzzle)
    color_nums = range(num_colors) # list of all color numbers
    # find coordinate for each color start
    for row_i in xrange(dim):
        for col_i in xrange(dim):
            char_found = puzzle[row_i][col_i]
            # if char found is an e then go to then skip it
            if char_found == 'e':
                continue
            # remove the first number of the pair from the color_nums list
            if int(char_found) in color_nums:
                num_found = int(char_found)
                color_nums.remove(num_found)
            # if the number doesnt exist in color_nums then it is end number
            else:
                num_found = int(char_found)
                coordinates[num_found] = [row_i, col_i]

    # error checking to make sure right number of colors were found
    if len(coordinates) != num_colors:
        print 'ERROR: PROBLEMS FINDING COLORS'
        print 'COORDINATES: %r' % coordinates
        print 'END COLORS TO BE FOUND: %r' % range(num_colors)
        exit(1)

    return coordinates

# PURPOSE: given a list of action coordinates, it will translate them into
# plain english ['right', 'up', 'down', or 'right']
def DirPrint(directions):
    dir_array = []
    for direction in directions:
        row_dir = direction[0]
        col_dir = direction[1]

        if row_dir == 0:
            if col_dir == 1:
                dir_array.append('right')
            elif col_dir == -1:
                dir_array.append('left')
            else:
                # this one should never be used
                dir_array.append('stay')
        elif row_dir == 1:
            dir_array.append('down')
        else:
            dir_array.append('up')

    return dir_array

# PURPOSE: prints out action sequence and final array
# INPUT: list of nodes from root to final for solution path and number of colors
# OUTPUT: action format: color col_moved_to row_moved_to, color col_moved_to etc.
def UglyPrint(sol_nodes, num_colors):
    colors_connected = []
    root_state = sol_nodes[0].state
    final_state = sol_nodes[-1].state
    upper_bound = len(final_state)
    lower_bound = 0

    # find all actions stored by states
    actions = []
    for node in sol_nodes:
        if node.action == None:
            continue
        else:
            actions.append(node.action)
    # find the last actions to get to 'officially' connect the colors
    endpoints = FindColorEnd(root_state, num_colors)
    for color in endpoints:
        # find the end point coordinats for color
        end = endpoints[color]
        actions.append([color, end[0], end[1]])

    for i, action in enumerate(actions):
        # switch the row and col actions because thats how Dr. T wants it
        if i+1 < len(actions): comma = ','
        else: comma = ''

        print '%d %d %d%s' % (action[0], action[2], action[1], comma),
    print

    # print final state
    for row in final_state:
        for char in row:
            print char,
        print

# PURPOSE: prints out a visual representation of the 2D state array
# INPUT: accepts square matricies in the form of a 2D array only
def Visualize(puzzle):
    # pretty colors
    colors = [bcolors.HEADER, bcolors.OKGREEN, bcolors.WARNING,
                bcolors.FAIL, bcolors.OKBLUE]
    # top horizontal divider
    print '%s%s' % (('+---' * len(puzzle)), '+')
    for row in puzzle:
        print '|', # front vertical divider
        for char in row:
            # empty + vertical divider
            if char == 'e': print ' ', '|',
            # color num + vertical divider
            else: print colors[int(char)%5] + char + bcolors.ENDC, '|',
        # horizontal divider
        print '\n%s%s' % (('+---' * len(row)), '+')

################################################################################
## Main
################################################################################

random.seed()
appreciation_4_beauty = False

## READ IN PUZZLE FROM FILE ##
if len(sys.argv) > 1:
    p_file = sys.argv[1]
    # parse the input file
    (num_colors, pzzl_array) = ReadInput(p_file)
    # check for a second extra argumanet
    if len(sys.argv) > 2:
        if sys.argv[2] == 'true':
            appreciation_4_beauty = True
else:
    print 'ERROR: you must include the file name in argument list'
    print 'EXAMPLE: "python solver.py input_p1.txt"'
    exit(1)

## BUILD TREE AND BFTS FOR SOLUTION ##
PTree = StateTree(pzzl_array, num_colors)
solution = PTree.BreadthFirstTreeSearch()

## PRINT SOLUTION ##
# if puzzle is impossible, say so
if solution == False:
    print '== NO SOLUTION POSSIBLE! =='
# UGLY SOLUTION
elif not appreciation_4_beauty:
    # time in microseconds
    print int((time.time() - start_time)*1000000)
    # path cost of solution
    print solution[-1].path_cost + num_colors
    # print actions and final state
    UglyPrint(solution, num_colors)
# PRETTY SOLUTION
else:
    for node in solution:
        print '== STATE %d LEVEL %d ==' % (node.ID, node.path_cost)
        Visualize(node.state)
    print '== FINISHED IN %4.4f SECONDS ==' % (time.time() - start_time)



###################################
### TODO

# finish the UGLY PRINT option
# remove unnessisary functions
