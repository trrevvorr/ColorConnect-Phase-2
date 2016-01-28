# AI - CS 5400 - Sec 1A
# Puzzle Assignmet 1 - Phase 1
#
# Trevor Ross
# 01/27/2016
# from sys import argv
import re
import copy

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


class StateTree():
    """Creates a State Tree for all possible states of Puzzle"""
    def __init__(self, initial_puzzle, number_of_colors):
        self.puzzle = initial_puzzle
        self.num_colors = number_of_colors
        self.color_start = FindColorStart(self.puzzle, self.num_colors)
        self.color_end = FindColorEnd(self.puzzle, self.num_colors)
        self.ID = 0
        self.relation_dict = {self.ID:None}
        self.state_dict = {self.ID:self.puzzle}

    def BreadthFirstSearch(self):
        self.BuildSearchTree(self.color_start)
        # color_end = FindColorEnd(self.puzzle, self.num_colors)

        # Search the tree via depth-first-search for final state
        # ...

        # solution_path = TraceBack(search_tree, state_id)


    def BuildSearchTree(self, colors_path_head):
        parent_id = self.ID
        print '\n=== CHILDREN OF STATE %d ===' % parent_id

        # go through each color
        for color_num in colors_path_head:
            # get the coordinates of the furthest point of the color's path
            coord = colors_path_head[color_num]
            print '\n--- COLOR %d COORDINATE: %r ---' % (color_num, coord)
            # retrive all valid actions from this color's path head
            valid_actions = Actions(self.state_dict[parent_id], coord)
            print 'valid actions:', valid_actions
            # create a new child state for each valid action
            for action in valid_actions:
                self.ID += 1
                # retulting child state from parent acted  on by action
                c_state = Result(self.state_dict[parent_id], coord, action)
                print 'STATE:', self.ID
                # update the futhest point of the color's path
                new_c_path_head = colors_path_head.copy()
                new_c_path_head[color_num] = action
                # add the child-parent relation to the dict
                self.relation_dict[self.ID] = parent_id
                # add the state to the dict
                self.state_dict[self.ID] = c_state
                Visualize(self.state_dict[self.ID])
                print 'new path head:', new_c_path_head
                print 'new relation dict:', self.relation_dict

                if False:
                #if VerifyFinal(self.state_dict[self.ID], self.color_start, self.color_end):
                    print '*** STATE %d IS FINAL ***'
                else:
                    # if current state is not final state then go deeper
                    self.BuildSearchTree(new_c_path_head)

            print '\n--- END COLOR %d COORDINATE: %r ---' % (color_num, coord)
        print '\n=== END CHILDREN OF STATE %d ===' % parent_id


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





def VerifyFinal(pzzl_state, colors_start, colors_end):   # REVIEW: ask if i should name the function FINAL
    p_copy = copy.deepcopy(pzzl_state)

    for color in colors_start:
        start = colors_start[color]
        end = colors_end[color]
        curr_state = start

        while True:
            if curr_state == end:
                break
            for action in [[-1,0], [0,1], [1,0], [0,-1]]:
                new_row = coord[0]+action[0]
                new_col = coord[1]+action[1]
                if p_copy[new_coord[0]][new_coord[1]] != 'e':
                    continue


def TraceBack(search_tree, state_id):
    pass


def Actions(p_state, coord):
    upper_bound = len(p_state)
    lower_bound = 0
    valid_actions = []

    # action order: down, right, up, left
    for action in [[-1,0], [0,1], [1,0], [0,-1]]:
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
        valid_actions.append(new_coord)

    return valid_actions



def Result(p_state, coord, action):
    new_state = copy.deepcopy(p_state)
    color_path_to_extend = p_state[coord[0]][coord[1]]
    new_state[action[0]][action[1]] = color_path_to_extend
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
pzzl_num = 0
(num_colors, pzzl_array) = ReadInput(pzzl_num)
print '== INITIAL PUZZLE =='
Visualize(pzzl_array)
PTree = StateTree(pzzl_array, num_colors)
PTree.BreadthFirstSearch()


# color_start = FindColorStart(pzzl_array, num_colors)
# print 'Color Start:', color_start
# relation_dict = {0:None}
# state_dict = {0:pzzl_array}
# valid_actions = Actions(state_dict[0], color_start[0])
# print 'Valid Actions:', valid_actions
#
# a = 1
# for action in valid_actions:
#     new_state = Result(pzzl_array, color_start[0], action)
#     print 'ACTION: %d' % a
#     Visualize(new_state)
#     a += 1
#
# color_end = FindColorEnd(pzzl_array, num_colors)
# print 'Color End:', color_end
