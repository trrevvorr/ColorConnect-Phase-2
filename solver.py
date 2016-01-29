# AI - CS 5400 - Sec 1A
# Puzzle Assignmet 1 - Phase 1
#
# Trevor Ross
# 01/27/2016
# from sys import argv
import re
import copy
import random
import time
start_time = time.time()

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

        self.path_head = []


class StateTree():
    """Creates a State Tree for all possible states of Puzzle"""
    def __init__(self, initial_puzzle, number_of_colors, focus_color=0):
        # a globla ID index for creating unique node IDs
        self.ID = 0
        self.root = Node(self.ID, state=initial_puzzle)
        # self.puzzle = initial_puzzle
        self.num_colors = number_of_colors
        self.focus_color = focus_color
        self.color_start = FindColorStart(self.root.state, self.focus_color)
        self.root.path_head = self.color_start
        self.color_end = FindColorEnd(self.root.state, self.focus_color)
        self.root.path_cost = 0
        # dictionary of states indexed by their ID
        self.state_dict = {self.root.ID:self.root}


    def BreadthFirstTreeSearch(self):
        queue = [self.root]
        interupt_state = 20000
        last_interrupt = time.time()
        total_time_on_final = 0.0
        total_time_on_action = 0.0
        total_time_on_creation = 0.0
        BFTS_start_time = time.time()
        found_final = False

        while not found_final:
            # dequeue the front element
            if len(queue) == 0:
                # queue is empty, no solution could be found
                return False
            to_examine = queue.pop(0)
            # examine element
            if self.VerifyFinal(to_examine.state):
                # a goal state has been found
                if self.focus_color+1 == self.num_colors:
                    # if all colors have been focused on then we're done
                    print 'FINAL GOAL:'
                    Visualize(to_examine.state)
                    return [to_examine.state]
                else:
                    # create a new tree that focuses on the next color
                    print 'TEMP GOAL:'
                    Visualize(to_examine.state)
                    NextTree = StateTree(to_examine.state, self.num_colors, self.focus_color+1)
                    NextSolution = NextTree.BreadthFirstTreeSearch()
                    if NextSolution != False:
                        solution_list = [to_examine.state]
                        solution_list = solution_list + NextSolution
                        return solution_list
                    else:
                        print 'TEMP GOAL FAILED'
            else:
                # Visualize(to_examine.state)
                valid_actions, valid_coords = Actions(to_examine.state, to_examine.path_head, self.color_end)
                # print '%d: VALID ACTIONS: %r' % (self.focus_color, DirPrint(valid_actions))
                # create a new child state for each valid action
                for i in xrange(len(valid_actions)):
                    action = valid_actions[i]
                    action_coord = valid_coords[i]
                    self.ID += 1
                    # retulting child state from parent acted on by action
                    c_state = Result(to_examine.state, to_examine.path_head, action)
                    # create new node
                    child = Node(ID=self.ID, parent_node=to_examine.ID, state=c_state, action=action)
                    # updated the child's path heads
                    child.path_head = action_coord
                    # update child's path cost
                    child.path_cost = to_examine.path_cost + 1
                    # store child in dictionary for reference later
                    self.state_dict[child.ID] = child
                    # check if child is Goal State
                    # if self.VerifyFinal(child.state):
                    #     # a goal state has been found
                    #     if self.focus_color+1 == self.num_colors:
                    #         # if all colors have been focused on then we're done
                    #         print 'FINAL GOAL:'
                    #         Visualize(child.state)
                    #         return [child.state]
                    #     else:
                    #         # create a new tree that focuses on the next color
                    #         print 'TEMP GOAL:'
                    #         Visualize(child.state)
                    #         NextTree = StateTree(child.state, self.num_colors, self.focus_color+1)
                    #         NextSolution = NextTree.BreadthFirstTreeSearch()
                    #         if NextSolution != False:
                    #             solution_list = [child.state]
                    #             solution_list = solution_list + NextSolution
                    #             return solution_list
                    #         else:
                    #             print 'TEMP GOAL FAILED'
                    # else:
                    #     # push child onto queue
                    queue.append(child)
            # if found_final: break

            # if self.ID > interupt_state:
            #     print '-- TIME --'
            #     print 'TOTAL:', (time.time() - BFTS_start_time)
            #     print "SPLIT:", (time.time() - last_interrupt)
            #     print '- '*10
            #     print 'FINAL CHECK: ', total_time_on_final
            #     print 'ACTION CHECK:', total_time_on_action
            #     print 'CREATION:    ', total_time_on_creation
            #     print '-- EXAM STATE --'
            #     print 'STATE:', to_examine.ID
            #     print 'DEPTH:', to_examine.path_cost
            #     Visualize(to_examine.state)
            #     print '-- LATEST CREATION --'
            #     print 'STATE:', self.ID
            #     print 'DEPTH:', (self.state_dict[self.ID]).path_cost
            #     Visualize((self.state_dict[self.ID]).state)
            #     interupt_state+=20000
            #     last_interrupt = time.time()
            # print 'FRONTIER:',
            # for node in queue:
            #     print node.ID,
            # print
            # print 'EXAMINED:', to_examine.ID
        self.PrintSolution(child.ID)
        print 'STATES:', self.ID
        # self. StateLookup()


    def VerifyFinal(self, pzzl_state): # REVIEW: ask if i should name the function FINAL
        upper_bound = len(pzzl_state)
        lower_bound = 0

        for direction in [[-1,0], [0,1], [1,0], [0,-1]]:
            adj_row = self.color_end[0]+direction[0]
            adj_col = self.color_end[1]+direction[1]
            # ignore if out-of-bounds
            if adj_col < lower_bound or adj_col == upper_bound:
                continue
            if adj_row < lower_bound or adj_row == upper_bound:
                continue

            if pzzl_state[adj_row][adj_col] == str(self.focus_color):
                # color has been connected
                return True

        return False



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
def FindColorStart(puzzle, color):
    dim = len(puzzle)
    # find coordinate for each color start
    for row_i in xrange(dim):
        for col_i in xrange(dim):
            char_found = puzzle[row_i][col_i]
            if char_found == 'e':
                continue
            if int(char_found) == color:
                coordinates = [row_i, col_i]
                # print 'COORDINATES OF FIRST %d: %r' % (color, coordinates)
                return coordinates

    # error checking to make sure color was found
    print 'FindColorStart ERROR: %d WAS NOT FOUND IN:' % color
    Visualize(puzzle)
    print 'END ERROR'
    exit(1)


# PURPOSE: given the puzzle and the number of colors to find, function will
# return a dict with the LAST occurance of the number as the key and its
# coordinates as the value
# OUTPUT: dictionary in the format: {0:[r0,c0], 1:[r1,c1],...}
def FindColorEnd(puzzle, color):
    dim = len(puzzle)
    second_find = False
    # find coordinate for each color end
    for row_i in xrange(dim):
        for col_i in xrange(dim):
            char_found = puzzle[row_i][col_i]
            if char_found == 'e':
                continue
            if int(char_found) == color:
                if second_find:
                    coordinates = [row_i, col_i]
                    # print 'COORDINATES OF LAST %d: %r' % (color, coordinates)
                    return coordinates
                else:
                    second_find = True

    # error checking to make sure color was found
    print 'FindColorEnd ERROR: %d WAS NOT FOUND IN:' % color
    Visualize(puzzle)
    print 'END ERROR'
    exit(1)


def TraceBack(search_tree, state_id):
    pass


def Actions(p_state, coord, end_coord):
    upper_bound = len(p_state)
    lower_bound = 0
    color =  int(p_state[coord[0]][coord[1]])
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
                dir_array.append('stay')
        elif row_dir == 1:
            dir_array.append('down')
        else:
            dir_array.append('up')

    return dir_array


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

pzzl_num = 2  # TODO: make it so I can enter this number via command line
(num_colors, pzzl_array) = ReadInput(pzzl_num)

print '== INITIAL PUZZLE =='
Visualize(pzzl_array)
PTree = StateTree(pzzl_array, num_colors, 0)
pzzl_sol = PTree.BreadthFirstTreeSearch()

print '== PUZZLE SOLUTION =='
if pzzl_sol == False:
    print 'NO SOLUTION POSSIBLE!'
else:
    for solution in pzzl_sol:
        Visualize(solution)

print("--- %s seconds ---" % (time.time() - start_time))


###################################
### TODO

# remove all 'remove' statements as possible
