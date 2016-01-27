# AI - CS 5400 - Sec 1A
# Puzzle Assignmet 1 - Phase 1
#
# Trevor Ross
# 01/27/2016
# from sys import argv
import re

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
    return (num_colors, pzzl_array)


def DepthFirstSearch(num_colors, puzzle):
    Visualize(puzzle)
    color_start = FindColorStart(puzzle, num_colors)
    # search_tree = BuildSearchTree(puzzle, color_start)
    color_end = FindColorEnd(puzzle, num_colors)

    # Search the tree via depth-first-search for final state
    # ...

    # solution_path = TraceBack(search_tree, state_id)

    print color_start
    print color_end


# PURPOSE: given the puzzle and the number of colors to find, function will
# return a dict with the FIRST occurance of the number as the key and its
# coordinates as the value
# OUTPUT: dictionary in the format: {0 : [c0, r0], 1 : [c1, r1], ...}
# NOTICE: coorditates are NOT stored in the typical [r, c] fasion
def FindColorStart(puzzle, num_colors):
    coordinates = {} # format: {0:[c0,r0], 1:[c1,r1],...} where r = row, c = col
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
                coordinates[num_found] = [col_i, row_i]

    # error checking to make sure right number of colors were found
    if len(coordinates) != num_colors:
        print 'ERROR: PROBLEMS FINDING COLORS'
        print 'COORDINATES: %r' % coordinates
        print 'START COLORS TO BE FOUND: %r' % range(num_colors)
        exit(1)

    return coordinates





def BuildSearchTree(puzzle, color_start):
    pass


# PURPOSE: given the puzzle and the number of colors to find, function will
# return a dict with the LAST occurance of the number as the key and its
# coordinates as the value
# OUTPUT: dictionary in the format: {0 : [c0, r0], 1 : [c1, r1], ...}
# NOTICE: coorditates are NOT stored in the typical [r, c] fasion
def FindColorEnd(puzzle, num_colors):
    coordinates = {} # format: {0:[c0,r0], 1:[c1,r1],...} where r = row, c = col
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
                coordinates[num_found] = [col_i, row_i]

    # error checking to make sure right number of colors were found
    if len(coordinates) != num_colors:
        print 'ERROR: PROBLEMS FINDING COLORS'
        print 'COORDINATES: %r' % coordinates
        print 'END COLORS TO BE FOUND: %r' % range(num_colors)
        exit(1)

    return coordinates


def VerifyFinal(pzzl_state):   # REVIEW: ask if i should name the function FINAL
    pass


def TraceBack(search_tree, state_id):
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
pzzl_num = 1
(num_colors, pzzl_array) = ReadInput(pzzl_num)
DepthFirstSearch(num_colors, pzzl_array)
