"""
Solves Color Connect Puzzle as per AI Puzzle 1 requirement

AI - CS 5400 - Sec 1A
Puzzle Assignmet 1 - Phase 1

Trevor Ross
01/27/2016
"""

import sys
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

        if parent_node is None:
            self.p_ID = None
            self.path_cost = None
            self.path_start = None
            self.path_heads = None
            self.path_end = None
        else:
            # parent_node = copy.deepcopy(parent_node)
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
                    elif [r, c] == head_coord:
                        # trail heads are bolded
                        style = BOLD + style
                    # print the cell with style
                    print style + char + ENDC, '|',
            # horizontal divider
            print '\n%s%s' % (('+---' * len(row)), '+')


class StateTree(object):
    """Creates a State Tree for all possible states of Puzzle"""
    def __init__(self, initial_puzzle, number_of_colors):
        # a globla ID index for creating unique node IDs
        self.ID = 0
        # create a root node
        self.root = Node(self.ID, state=initial_puzzle)
        self.num_colors = number_of_colors
        # find start and end locations of puzzle colors
        self.color_start = FindColorStart(self.root.state, self.num_colors)
        self.root.path_start = self.color_start
        self.root.path_heads = self.color_start
        self.color_end = FindColorEnd(self.root.state, self.num_colors)
        self.root.path_end = self.color_end
        self.root.path_cost = 0
        # dictionary of nodes indexed by their ID
        # self.node_dict = {self.root.ID: self.root}

        # TIMING VARIABLE
        self.run_time = time.time()


    def ID_DFTS(self):
        """
        Iterative Depening - Depth First Tree search
        """
        self.run_time = time.time()
        depth_limit = 0

        while True:
            print '=== RUNNING DFTS WITH L = %d ===' % depth_limit
            result = self.DFTS(depth_limit)
            if result != 'cutoff':
                self.run_time = time.time() - self.run_time
                return result
            depth_limit += 1


    def DFTS(self, depth_limit):
        """
        Depth Limited - Depth First Tree Search

        OUTPUT: 'fail', 'cutoff', or solution
        """
        return self.RecursiveDFTS(self.root, depth_limit)


    def RecursiveDFTS(self, node, depth_limit):
        """
        Performs Depth First Tree Search using recution

        OUTPUT: 'fail', 'cutoff', or a solution
        """
        if self.VerifyFinal(node) is True:
            return [node]
        elif depth_limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            valid_actions = self.Action(node)
            # node.state_info()
            # node.visualize()
            # print 'VALID ACTIONS:'
            # for c_i, action_i, coord_i in valid_actions:
            #     print '%d:' % c_i,
            #     DirPrint([action_i])

            for action_set in valid_actions:
                color_num = action_set[0]
                action = action_set[1]
                action_coord = action_set[2]

                self.ID += 1
                # retulting child node state from parent acted on by action
                c_state = Result(node.state, node.path_heads[color_num], action)
                # CREATE NEW NODE
                # alther action coord for color context
                # action_coord.insert(0, color_num)
                # TODO: merge node.action and node.path_heads?
                child = Node(self.ID, c_state, action=([color_num] + action_coord), parent_node=node)
                # updated the child's path head
                child.path_heads[color_num] = action_coord
                # add child to the dict
                # self.node_dict[child.ID] = child
                result = self.RecursiveDFTS(child, depth_limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result != 'fail':
                    return [node] + result
                # check if child is Goal State
                # colors_connected = self.VerifyFinal(child.state)
                # if colors_connected is True:
                #     # a goal state has been found
                #     # return the final state and it's ancestors
                #     self.run_time = time.time() - self.run_time
                #     return self.TraceBack(child)
                # push child onto queue
                # self.stack.append(child.ID)
            if cutoff_occurred:
                return 'cutoff'
            else:
                return 'fail'

    def Action(self, node):
        """
        Given a node, return a dict of valid actions for each color

        VALID MOVE DISQUALIFICATION: if one of the colors hits a dead end
        A.K.A. it has no valid moves, no valid moves will be returned for any color
        OUTPUT: shuffled list of color nums , actions, and new coords
        """
        # shuffled list of valid actions to perform on node
        # format: [[n, [r_, c_], [r', c']], [n, [r_, c_], [r', c']], ...]
        # such that n is the color number, r_ is the row action,
        # c_ is the column action, r' is the new row, c' is the new column
        valid_actions = []

        # find which colors are already connected
        colors_connected = self.VerifyFinal(node)
        # get a list of colors in puzzle and shuffle it
        color_numbers = range(self.num_colors)
        # trim down the list of numbers to colors action on
        # if the color is already connected, no further action needed on color
        for color in color_numbers:
            if color in colors_connected:
                color_numbers.remove(color)

        # iterate through remaining colors, finding actions for each
        for color in color_numbers:
            old_length = len(valid_actions)
            # add actions for this color to the valid actions list
            valid_actions += (self.ActionOnColor(node, color))
            # if no new actions were added, this color has hit a dead end
            if len(valid_actions) == old_length:
                # since it has hit a dead end and it's not final no actions returned
                return []

        random.shuffle(valid_actions)
        return valid_actions

    def ActionOnColor(self, node, color):
        """
        Given a state, and a color, the function will return a list of all
        valid moves for that color

        VALID MOVE DISQUALIFICATION:
        1) moves out of puzzle's bounds
        2) moves onto a pre-existing line
        3) path moves adjacent to itself, aka, the path 'touches' itself
        OUTPUT: returns a list of valid actions as well as the coordinates they result in
        FORMAT: the 4 possible moves are: [[-1,0], [0,1], [1,0], [0,-1]]
        Function returns a dict with 'action' being the key to the list of
        valid actions. 'coord' is the key for valid coordinates
        """
        coord = node.path_heads[color]
        end_coord = node.path_end[color]
        valid_actions = []

        # actions in order: down, right, up, left
        action_options = [[-1,0], [0,1], [1,0], [0,-1]]
        random.shuffle(action_options)
        for action in action_options:
            new_row = coord[0] + action[0]
            new_col = coord[1] + action[1]
            # check if move is out-of-bounds
            if OutOfBounds([new_row, new_col], len(node.state)):
                continue
            # check if space is already occupied
            if node.state[new_row][new_col] != 'e':
                continue
            # check if move results in path becoming adjacent to itself
            adj_itself = 0
            for adj in action_options:
                adj_row = new_row + adj[0]
                adj_col = new_col + adj[1]
                # check if adjacent square is out-of-bounds
                if OutOfBounds([adj_row, adj_col], len(node.state)):
                    continue
                if node.state[adj_row][adj_col] == str(color):
                    if [adj_row, adj_col] != end_coord:
                        adj_itself += 1
            if adj_itself > 1:
                continue
            # if move is in-bounds, space is not occupied, and path isn't
            # adjacent to itself, it is a valid move
            new_coord = [new_row, new_col]
            valid_actions.append([color, action, new_coord])

        return valid_actions

    def VerifyFinal(self, node):
        """
        Verify that the passed state is a final state

        IF FINAL: return True
        IF NOT FINAL: return a list of those colors who are final
        """
        colors_connected = []

        for color in node.path_end:
            # get path_end and path_head coordinates for color
            end = node.path_end[color]
            head = node.path_heads[color]
            # get the difference (offset) betweeen the path_head and path_end
            row_diff = head[0] - end[0]
            col_diff = head[1] - end[1]
            # if the endpoint is adjacent to the path head then state is final
            if [row_diff, col_diff] in [[-1,0], [0,1], [1,0], [0,-1]]:
                colors_connected.append(color)

        if len(colors_connected) == len(node.path_end):
            # if all colors are connected, return true
            return True
        else:
            # otherwise return a list of the colors who are connected
            return colors_connected


    def node_lookup(self):
        """
        Allows user to enter a state's ID and see the state

        LOOP: loops infinatly until user enters anything but a number
        """
        print 'Enter Desired State ID to look up State'
        user_in = int(raw_input('>'))
        while True:
            node = self.node_dict[user_in]
            print 'State ID:', node.ID, 'Parent ID:', node.p_ID
            node.visualize()
            user_in = int(raw_input('>'))


################################################################################
## FUNCTIONS
################################################################################

def ReadInput(pzzl_file):
    """
    Reads in a puzzle file and parses the data for solving

    INPUT: first line: # rows/columns, # of colors
    the input puzzle will follow as a square matrix
    OUTPUT: returns a tuple with the number of colors and the puzzle as a 2D array
    """
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


def OutOfBounds(coord, puzzle_dim):
    """
    Returns true if coordinats are out of bounds of the puzzle returs false otherwise
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
    color_nums = range(num_colors)  # list of all color numbers
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
    try:
        new_state[new_row][new_col] = color_path_to_extend
    except IndexError:
        print 'COORD:', coord
        print 'ACTION:', action
        raise IndexError

    return new_state

# def move_coord(coord, action):
#     """
#     Returns the resulting coord after the action has taken place on the coord
#
#     INPUT: coord in the form [r, c] and action in the form [r_, c_]
#     OUTPUT: returns the new coordinate in form [r', c']
#     """


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


def UglyPrint(PTree, sol_nodes, num_colors):
    """
    Prints out action sequence and final array to command line (as well as solution file)

    INPUT: list of nodes from root to final for solution path and number of colors
    OUTPUT: action format: color col_moved_to row_moved_to, color col_moved_to etc.
    """
    root_state = sol_nodes[0].state
    final_state = sol_nodes[-1].state
    in_file_name = sys.argv[1]
    out_file_name = 'p%s_solution.txt' % in_file_name[7]
    out_file = open(out_file_name, 'w')

    # time in microseconds
    print int(PTree.run_time * 1000000)
    out_file.write(str(int(PTree.run_time * 1000000)))
    out_file.write('\n')
    # path cost of solution
    print sol_nodes[-1].path_cost + num_colors
    out_file.write(str(sol_nodes[-1].path_cost + num_colors))
    out_file.write('\n')
    # print actions and final state

    # find all actions stored by states
    actions = []
    for node in sol_nodes:
        if node.action is None:
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
        if i + 1 < len(actions):
            comma = ','
        else:
            comma = ''
        output = '%d %d %d%s' % (action[0], action[2], action[1], comma)
        print output,
        out_file.write(output)
    print
    out_file.write('\n')

    # print final state
    for row in final_state:
        for char in row:
            print char,
            out_file.write(char + ' ')
        print
        out_file.write('\n')

    out_file.close()

################################################################################
## Main
################################################################################

def main():
    random.seed()
    appreciation_4_beauty = False

    ## READ IN PUZZLE FROM FILE ##
    if len(sys.argv) > 1:
        p_file = sys.argv[1]
        # parse the input file
        (num_colors, pzzl_array) = ReadInput(p_file)
        # check for a second extra argumanet
        if len(sys.argv) > 2:
            if sys.argv[2] == 'pretty':
                appreciation_4_beauty = True
    else:
        print 'ERROR: you must include the file name in argument list'
        print 'EXAMPLE: "python solver.py input_p1.txt"'
        exit(1)

    ## BUILD TREE AND BFTS FOR SOLUTION ##
    PTree = StateTree(pzzl_array, num_colors)
    solution = PTree.ID_DFTS()

    ## PRINT SOLUTION ##
    # if puzzle is impossible, say so
    if solution is False:
        print '== NO SOLUTION POSSIBLE! =='
    # UGLY SOLUTION
    elif not appreciation_4_beauty:
        UglyPrint(PTree, solution, num_colors)
    # PRETTY SOLUTION
    else:
        for node in solution:
            print '== STATE %d LEVEL %d ==' % (node.ID, node.path_cost)
            node.state_info()
            node.visualize()
            # Visualize(node.state)
        print '== FINISHED IN %4.4f SECONDS ==' % PTree.run_time


if __name__ == "__main__":
    main()
