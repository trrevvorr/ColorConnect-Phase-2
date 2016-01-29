# AI - CS 5400 - Sec 1A
# Puzzle Assignmet 1 - Phase 1
#
# Trevor Ross
# 01/27/2016
# from sys import argv
import re
import copy
import random

################################################################################
## CLASSES
################################################################################

class Node():
    """Tree node for State Tree"""
    def __init__(self, ID=None, parent_node=None, state=None, action=None):
        self.ID = ID # integer
        self.p_ID = parent_node # integer
        self.state = state # format: [[... row 1 ...], [... row 2 ...], ...]
        self.action = action # format: [x, y] where x and y are in [-1, 0, 1]
        self.path_cost = None # integer (depth of state in tree)

        self.path_heads = {} # dictionary containing the furthes a color path
        # has travled in the current state. format: {0:[r0,c0], 1:[r1,c1], ...}


class StateTree():
    """Creates a State Tree for all possible states of Puzzle"""
    def __init__(self, initial_puzzle, number_of_colors):
        # a globla ID index for creating unique node IDs
        self.ID = 0
        self.root = Node(self.ID, state=initial_puzzle)
        # self.puzzle = initial_puzzle
        self.num_colors = number_of_colors
        self.color_start = FindColorStart(self.root.state, self.num_colors)
        self.root.path_heads = self.color_start
        self.color_end = FindColorEnd(self.root.state, self.num_colors)
        # dictionary of relations. format: {parent_ID:child_ID}
        self.relation_dict = {self.root.ID:None}
        # dictionary of states indexed by their ID
        self.state_dict = {self.root.ID:self.root}


    def BreadthFirstTreeSearch(self):
        queue = [self.root]
        ocational_period = 10000

        while True:
            # dequeue the front element
            to_examine = queue.pop(0)
            # Visualize(to_examine.state)
            # examine element
            colors_connected = self.VerifyFinal(to_examine.state)
            if colors_connected == True:
                # a goal state has been found
                print 'GOALLLLLLLLLL!!!!!!!'
                Visualize(to_examine.state)
                break
            # go through each color, finding actions for each
            color_numbers = to_examine.path_heads.keys()
            random.shuffle(color_numbers)
            for color_num in color_numbers:
                # ignore colors that have already found their goal state
                if color_num in colors_connected: continue
                # get the coordinates of the furthest point of the color's path
                coord = to_examine.path_heads[color_num]
                # retrive all valid actions from this color's path head
                valid_actions, valid_coords = Actions(to_examine.state, coord)
                # print 'valid extentions of %d:' % color_num, valid_coords
                # create a new child state for each valid action
                for i in xrange(len(valid_actions)):
                    action = valid_actions[i]
                    action_coord = valid_coords[i]
                    self.ID += 1
                    # retulting child state from parent acted on by action
                    c_state = Result(to_examine.state, coord, action)
                    # create new node
                    child = Node(ID=self.ID, parent_node=to_examine.ID, state=c_state, action=action)
                    # updated the child's path heads
                    child.path_heads = to_examine.path_heads.copy()
                    child.path_heads[color_num] = action_coord
                    # push child onto queue
                    queue.append(child)
                    self.state_dict[child.ID] = child
            if self.ID > ocational_period:
                print '.',
                ocational_period+=10000
            # print 'FRONTIER:',
            # for node in queue:
            #     print node.ID,
            # print
            # print 'EXAMINED:', to_examine.ID
        self.PrintSolution(to_examine.ID)
        self. StateLookup()


    def VerifyFinal(self, pzzl_state):   # REVIEW: ask if i should name the function FINAL
        p_copy = copy.deepcopy(pzzl_state)
        colors_connected = []
        upper_bound = len(pzzl_state)
        lower_bound = 0

        for color in self.color_start:
            start = self.color_start[color]
            end = self.color_end[color]
            curr_loc = start

            # loop until end of line is reached
            while p_copy[curr_loc[0]][curr_loc[1]] != 'x':
                old_loc = curr_loc[:]
                if curr_loc == end:
                    colors_connected.append(color)
                    break
                for action in [[-1,0], [0,1], [1,0], [0,-1]]:
                    check_row = curr_loc[0]+action[0]
                    check_col = curr_loc[1]+action[1]
                    # ignore if out-of-bounds
                    if check_col < lower_bound or check_col == upper_bound:
                        continue
                    if check_row < lower_bound or check_row == upper_bound:
                        continue
                    # if the path contiues
                    if p_copy[check_row][check_col] == str(color):
                        # move to the next location along the line
                        curr_loc = [check_row, check_col]
                        break
                p_copy[old_loc[0]][old_loc[1]] = 'x'

        if len(colors_connected) == self.num_colors:
            return True
        else:
            return colors_connected


    def PrintSolution(self, solution_ID):
        print '\n\n=== SOLUTION ==='
        node = self.state_dict[solution_ID]
        solution = [node.state]

        while node.p_ID != None:
            node_ID = node.p_ID
            node = self.state_dict[node_ID]
            solution.insert(0, node.state)

        for state in solution:
            Visualize(state)
            print '      |'
            print '      V'
        print     '  FINISHED'


    def StateLookup(self):
        print 'Enter Desired State ID to look up State'
        user_in = int(raw_input('>'))
        while user_in != -1:
            state = self.state_dict[user_in]
            print 'State ID:', state.ID, 'Parent ID:', state.p_ID
            Visualize(state.state)
            user_in = int(raw_input('>'))


################################################################################
## FUNCTIONS
################################################################################
def ReadInput(pzzl_num):
    pzzl_file = 'input_p%s.txt' % pzzl_num
    f_hand = open(pzzl_file)

    pzzl_array = []
    for line in f_hand:
        line = line.split()
        pzzl_array.append(line)

    first_line = pzzl_array.pop(0)
    num_colors = int(first_line.pop())

    # transpose array since dr. t wants the coordinates in [c, r] format
    # pzzl_array = Transpose(pzzl_array)
    return (num_colors, pzzl_array)


def Transpose(matrix):
    t_matrix = copy.deepcopy(matrix)
    dem = len(matrix)

    for i in xrange(dem):
        for j in xrange(dem):
            t_matrix[i][j] = matrix[j][i]
    return t_matrix


# PURPOSE: given the puzzle and the number of colors to find, function will
# return a dict with the FIRST occurance of the number as the key and its
# coordinates as the value
# OUTPUT: dictionary in the format: {0:[r0,c0], 1:[r1,c1],...}
def FindColorStart(puzzle, num_colors):
    coordinates = {} # format: {0:[r0,c0], 1:[r1,c1],...} where r = row, c = col
    dim = len(puzzle)
    color_nums = range(dim) # list of all color numbers
    # find coordinate for each color start
    for row_i in xrange(dim):
        for col_i in xrange(dim):
            char_found = puzzle[row_i][col_i]
            if char_found == 'e':
                continue
            if int(char_found) in color_nums:
                num_found = int(char_found)
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
    color_nums = range(dim) # list of all color numbers
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


def TraceBack(search_tree, state_id):
    pass


def Actions(p_state, coord):
    upper_bound = len(p_state)
    lower_bound = 0
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
        # if move is in-bounds and space is not occupied, it is a valid move
        new_coord = [new_row, new_col]
        valid_actions.append(action)
        valid_coords.append(new_coord)

    return (valid_actions, valid_coords)



def Result(p_state, coord, action):
    new_state = copy.deepcopy(p_state)
    # retrieve the 'color' of th path to be extended
    color_path_to_extend = p_state[coord[0]][coord[1]]
    # find the location to place the extention
    new_row = coord[0]+action[0]
    new_col = coord[1]+action[1]
    # 'color' the new loaction, extending the line
    new_state[new_row][new_col] = color_path_to_extend
    return new_state


def MovePathHead(colors_path_head, action):
    pass


def Visualize(puzzle):
    print '%s%s' % (('+---' * len(puzzle)), '+') # top horizontal divider
    for row in puzzle:
        print '|', # front vertical divider
        for char in row:
            if char == 'e': print ' ', '|', # empty + vertical divider
            else: print char, '|', # color num + vertical divider
        print
        print '%s%s' % (('+---' * len(row)), '+') # horizontal divider

################################################################################
## Main
################################################################################
#script, pzzl_num = argv
random.seed()
print random.randint(1,5)
pzzl_num = 1
(num_colors, pzzl_array) = ReadInput(pzzl_num)
print '== INITIAL PUZZLE =='
Visualize(pzzl_array)
PTree = StateTree(pzzl_array, num_colors)
PTree.BreadthFirstTreeSearch()
