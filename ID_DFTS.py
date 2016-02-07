"""
Solves Color Connect Puzzle via iterative deepining, depth first search as per
Puzzle 2 requirement

AI - CS 5400 - Sec 1A
Puzzle Assignmet 2 - Phase 1

Trevor Ross
02/03/2016
"""
import copy
import random
import time

################################################################################
## CLASSES
################################################################################

class Node(object):
    """Tree node for State Tree"""
    def __init__(self, ID, state, parent_node=None, action=None):
        # Unique identifier for this node
        self.ID = ID  # integer
        # the curent state of this node in the form of a 2D array
        self.state = state  # format: [[... row 1 ...], [... row 2 ...], ...]
        # action that was taken on the parent node to produce this child node
        self.action = action  # format: [color_num, row_shift, col_shift]

        # copy info from parent if one exists
        if parent_node is None:
            self.p_ID = None
            self.path_cost = None
            self.path_start = None
            self.path_heads = None
            self.path_end = None
        else:
            # ID of parent node
            self.p_ID = parent_node.ID  # integer
            # the cost of the path starting at the root, ending at this node
            self.path_cost = parent_node.path_cost + 1  # integer
            # coordinates of start positions of all colors in puzzle
            self.path_start = parent_node.path_start.copy()  # format: {0:[r0,c0], 1:[r1,c1], ...}
            # coordinates of trail head positions of all colors in puzzle
            self.path_heads = parent_node.path_heads.copy()  # format: {0:[r0,c0], 1:[r1,c1], ...}
            # coordinates of end positions of all colors in puzzle
            self.path_end = parent_node.path_end.copy()  # format: {0:[r0,c0], 1:[r1,c1], ...}

    def state_info(self):
        """Prints contents of all member variables in node"""
        print '=' * 30
        print 'ID:', self.ID
        print 'p_ID:', self.p_ID
        print 'action:', self.action
        print 'path_cost:', self.path_cost
        print 'path_start:', self.path_start
        print 'path_heads:', self.path_heads
        print 'path_end:', self.path_end

    def visualize(self):
        """
        Prints out a visual representation of the node

        OUTPUT: 2D array of the state of the node, start and end points are
        underlined, trail heads are bolded
        """
        # pretty colors
        COLORS = ['\033[95m', '\033[92m', '\033[93m', '\033[91m', '\033[94m']
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        ENDC = '\033[0m'

        # top horizontal divider
        print '%s%s' % (('+---' * len(self.state)), '+')
        for r, row in enumerate(self.state):
            print '|',  # front vertical divider
            for c, char in enumerate(row):
                # empty + vertical divider
                if char == 'e':
                    print ' ', '|',
                # color num + vertical divider
                else:
                    c_num = int(char)
                    start_coord = self.path_start[c_num]
                    head_coord = self.path_heads[c_num]
                    end_coord = self.path_end[c_num]
                    # apply colors and styles to color number
                    # apply color
                    style = COLORS[c_num % 5]
                    if [r, c] == start_coord or [r, c] == end_coord:
                        # start and end points are underlined
                        style = UNDERLINE + style
                    if [r, c] == head_coord:
                        # trail heads are bolded
                        style = BOLD + style
                    # print the cell with style
                    print style + char + ENDC, '|',
            # horizontal divider
            print '\n%s%s' % (('+---' * len(row)), '+')


class StateTree(object):
    """Creates a State Tree for the puzzle, allowing ID-DFTS on said puzzle"""
    def __init__(self, initial_puzzle, number_of_colors):
        self.num_colors = number_of_colors
        # a globla ID index for creating unique node IDs
        self.uniq_ID = 0

        # create a root node and fill in the details
        self.root = Node(self.uniq_ID, state=initial_puzzle)
        # find coordinates of the start of the color path
        self.root.path_start = FindColorStart(self.root.state, self.num_colors)
        self.root.path_heads = self.root.path_start
        # find coordinates of the end of the color path
        self.root.path_end = FindColorEnd(self.root.state, self.num_colors)
        # the root has a path cost of 0
        self.root.path_cost = 0
        # timing variable
        self.run_time = None


    def ID_DFTS(self):
        """
        Iterative Depening - Depth First Tree search

        Calls DFTS with a depth limit starting at 0, going to infinity until
        either a goal is found or the puzzle is determined to be unsolvable
        """
        self.run_time = time.time()
        depth_limit = 0

        while True:
            # print '=== RUNNING DFTS WITH L = %d ===' % depth_limit
            result = self.RecursiveDFTS(self.root, depth_limit)
            if result != 'cutoff':
                # the puzzle has either been solved or found to be unsolvable
                self.run_time = time.time() - self.run_time
                return result
            # increase the depth and try again
            depth_limit += 1


    def RecursiveDFTS(self, node, depth_limit):
        """
        Performs Depth First Tree Search using recution

        OUTPUT: 'fail', 'cutoff', or a solution
        solution contains a list of nodes with the last item being the final state
        """
        if VerifyFinal(node) is True:
            return [node]
        elif depth_limit == 0:
            # the depth limit has been reached
            return 'cutoff'
        else:
            cutoff_occurred = False
            # OPTIMIZATION: store the list of final states from the if statement
            # above and pass it to the Action() funtion so it doen't have to
            # check the same thing again
            valid_actions = Action(node, self.num_colors)
            for color_num, action, new_coord in valid_actions:
                self.uniq_ID += 1
                # retulting child state from parent acted on by action
                child_state = Result(node.state, node.path_heads[color_num], action)
                # create the new child node
                child = Node(self.uniq_ID, child_state, action=([color_num] + new_coord), parent_node=node)
                # updated the child's path head
                child.path_heads[color_num] = new_coord
                # perform recursive DFTS on newly created child
                result = self.RecursiveDFTS(child, depth_limit - 1)
                # analize result of recursive call
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result != 'fail':
                    # Recursive call succeded!!!
                    return [node] + result

            # all children have been tested, none were successful :(
            if cutoff_occurred:
                return 'cutoff'
            else:
                return 'fail'

################################################################################
## FUNCTIONS
################################################################################

def OutOfBounds(coord, puzzle_dim):
    """
    Returns true if coordinats are out of bounds of the puzzle
    Returs false otherwise
    """
    new_row, new_col = coord
    LOWER_BOUND = 0
    UPPER_BOUND = puzzle_dim

    if new_col < LOWER_BOUND or new_col >= UPPER_BOUND:
        return True
    if new_row < LOWER_BOUND or new_row >= UPPER_BOUND:
        return True

    return False


def FindColorStart(puzzle, num_colors):
    """
    Given the puzzle and the number of colors to find, function will
    return a dict with the FIRST occurance of the number as the key and its
    coordinates as the value

    OUTPUT: dictionary in the format: {0:[r0,c0], 1:[r1,c1],...}
    """
    coordinates = {}  # format: {0:[r0,c0], 1:[r1,c1],...} where r = row, c = col
    dim = len(puzzle)
    # list of all color numbers
    color_nums = range(num_colors)
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

    # error checking to make sure correct number of colors were found
    if len(coordinates) != num_colors:
        print 'ERROR: PROBLEMS FINDING COLORS'
        print 'COORDINATES: %r' % coordinates
        print 'START COLORS TO BE FOUND: %r' % range(num_colors)
        exit(1)

    return coordinates


def FindColorEnd(puzzle, num_colors):
    """
    Given the puzzle and the number of colors to find, function will return
    a dict with the LAST occurance of the number as the key and its
    coordinates as the value

    OUTPUT: dictionary in the format: {0:[r0,c0], 1:[r1,c1],...}
    """
    coordinates = {}  # format: {0:[r0,c0], 1:[r1,c1],...}  where r = row, c = col
    dim = len(puzzle)
    color_nums = range(num_colors)  # list of all color numbers
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
            # if the number no longer exists in color_nums, it is an end number
            else:
                num_found = int(char_found)
                coordinates[num_found] = [row_i, col_i]

    # error checking to make sure correct number of colors were found
    if len(coordinates) != num_colors:
        print 'ERROR: PROBLEMS FINDING COLORS'
        print 'COORDINATES: %r' % coordinates
        print 'END COLORS TO BE FOUND: %r' % range(num_colors)
        exit(1)

    return coordinates


def Action(node, num_colors):
    """
    Given a node, return a shuffled list of valid actions on that node

    VALID MOVE DISQUALIFICATION: if even ONE of the colors has no valid
    moves and is not in a goal state, no valid moves will be returned for
    ANY other colors. Furthermore, ActionOnColor() is called and it further
    limits the amount of actions returned
    OUTPUT: shuffled list of color nums , actions, and new coords
    """
    # shuffled list of valid actions to perform on node
    # format: [[n, [r_, c_], [r', c']], [n, [r_, c_], [r', c']], ...]
    # such that n is the color number, r_ is the row action,
    # c_ is the column action, r' is the new row, c' is the new column
    valid_actions = []

    # find which colors are already connected
    colors_connected = VerifyFinal(node)
    if colors_connected is True:
        return []
    # get a list of colors in puzzle and shuffle it
    color_numbers = range(num_colors)
    # if the color is already connected, no further action needed on color
    for color in color_numbers:
        if color in colors_connected:
            color_numbers.remove(color)

    # iterate through remaining colors, finding actions for each
    for color in color_numbers:
        old_length = len(valid_actions)
        # add actions for this color to the valid actions list
        valid_actions += (ActionOnColor(node, color))
        # if no new actions were added, this color has hit a dead end
        if len(valid_actions) == old_length:
            # since it has hit a dead end and it's not final, no actions returned
            return []

    random.shuffle(valid_actions)
    return valid_actions

def ActionOnColor(node, color):
    """
    Given a node and a color, the function will return a list of all
    valid moves for that color

    VALID MOVE DISQUALIFICATION:
    1) action moves color path out of puzzle's bounds
    2) action moves color path onto a pre-existing path
    3) action moves color path adjacent to itself, aka, the path 'touches' itself
    OUTPUT: returns a list of valid actions as well as the coordinates they
    result in, along with the color the action was performed on
    FORMAT: the 4 possible actions are: [[-1,0], [0,1], [1,0], [0,-1]]
    """
    coord = node.path_heads[color]
    end_coord = node.path_end[color]
    valid_actions = []

    # actions in order: up, right, down, left
    action_options = [[-1,0], [0,1], [1,0], [0,-1]]
    random.shuffle(action_options)

    for action in action_options:
        new_row = coord[0] + action[0]
        new_col = coord[1] + action[1]
        # if new cell is the teh end cell, finish loop on that note
        if [new_row, new_col] == end_coord:
            new_coord = [new_row, new_col]
            valid_actions.append([color, action, new_coord])
            break
        # 1) invalid if action is out-of-bounds
        if OutOfBounds([new_row, new_col], len(node.state)):
            continue
        # 2) invalid if new cell is already occupied
        if node.state[new_row][new_col] != 'e':
            continue
        # 3) invalid if action results in path becoming adjacent to itself
        # check all 4 adjacent cells for same color
        for adj in action_options:
            adj_row = new_row + adj[0]
            adj_col = new_col + adj[1]
            is_adjacent = False
            # check if adjacent cell is out-of-bounds
            if OutOfBounds([adj_row, adj_col], len(node.state)):
                continue
            if node.state[adj_row][adj_col] == str(color):
                # ignore if adjacent cell is the end cell
                if [adj_row, adj_col] != end_coord:
                    # ignore if adjacent cell is the previous path head
                    if [adj_row, adj_col] != coord:
                        is_adjacent = True
                        break
        if is_adjacent:
            continue
        else:
            new_coord = [new_row, new_col]
            valid_actions.append([color, action, new_coord])

    return valid_actions


def VerifyFinal(node):
    """
    Verify that the passed node has a final state

    IF FINAL: return True
    IF NOT FINAL: return a list of those colors who are final
    """
    # Setting SMART_FINAL_DETECT to True reduces the max depth_limit by
    # 2 levels, making the time comlexity O(b^(d-2))
    # Unfortunatly, I am not allowed to use this method for the homework
    SMART_FINAL_DETECT = False
    colors_connected = []

    for color in node.path_end:
        # get path_end and path_head coordinates for color
        end = node.path_end[color]
        head = node.path_heads[color]

        if SMART_FINAL_DETECT:
            # get the difference (offset) betweeen the path_head and path_end
            row_diff = head[0] - end[0]
            col_diff = head[1] - end[1]
            # if the endpoint is adjacent to the path head then state is final
            if [row_diff, col_diff] in [[-1,0], [0,1], [1,0], [0,-1]]:
                colors_connected.append(color)

        # This is the strait-forward, dumb method of detecting a final state
        # It greatly increases the time requred for solution to be found
        else:
            if end == head:
                colors_connected.append(color)

    # if all colors are connected, return true
    if len(colors_connected) == len(node.path_end):
        return True
    # otherwise return a list of the colors who are connected
    else:
        return colors_connected


def Result(p_state, coord, action):
    """
    Return the result of taking action on the coordinate of the given state

    OUTPUT: Puzzle state in the form: [[... row 1 ...], [... row 2 ...], ...]
    """
    new_state = copy.deepcopy(p_state)
    # retrieve the 'color' of the path to be extended
    color_path_to_extend = p_state[coord[0]][coord[1]]
    # find the location to place the extention
    new_row = coord[0] + action[0]
    new_col = coord[1] + action[1]
    # 'color' the new loaction, extending the line
    new_state[new_row][new_col] = color_path_to_extend

    return new_state


def DirPrint(directions):
    """
    Translates list of actiton coordinates into plain english and prints them

    INPUT: [[0,1], [-1,0], etc.]
    OUTPUT: right, up, down, left, etc.
    """
    for direction in directions:
        row_dir = direction[0]
        col_dir = direction[1]

        if row_dir == 0:
            if col_dir == 1:
                print 'right,',
            elif col_dir == -1:
                print 'left,',
            else:
                # this one should never be used
                print 'stay,',
        elif row_dir == 1:
            print 'down,',
        else:
            print 'up,',

    print


################################################################################
# Main
################################################################################

def solve(pzzl_array, num_colors):
    random.seed()

    # build state tree to find solution
    PTree = StateTree(pzzl_array, num_colors)
    solution = PTree.ID_DFTS()

    return (solution, PTree.run_time)
