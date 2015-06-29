from game import *
# Print the board in a nice ASCII format

def rowSepString(board):
    return "+---" * len(board.grid) + "+" + "\n"

def getLineOneString(board,row,col):
    """Produce string for first line of an ASCII grid cell"""
    string = ""
    square = board.grid[row][col][0]

    # first char of player name or nothing in upper-left corner of square
    no_robot_there = True
    for robot in board.livingRobots:
        if (col,row) == robot.loc:
            string += robot.playerName[0]
            no_robot_there = False
    if no_robot_there:
        string += " "

    # wall "=" or nothing if 
    # TODO in future: instead make it "L" for laser or "P" for pusher, if it's that instead
    no_wall_there = True
    for p in square.propertyList:
        if p.__class__.__name__ == 'Wall' and p.orient == 0:
            string += "="
            no_wall_there = False
    if no_wall_there:
        string += " "

    # TODO: make this conveyor belt ("nesw"/"NESW" for regular/express); for no just blank!
    string += " "

    return string

def getLineTwoString(board,row,col):
    """Produce string for second line of an ASCII grid cell"""
    string = ""
    square = board.grid[row][col][0]

    # wall "[" or nothing if 
    # TODO in future: instead make it "L" for laser or "P" for pusher, if it's that instead
    no_wall_there = True
    for p in square.propertyList:
        if p.__class__.__name__ == 'Wall' and p.orient == 3:
            string += "["
            no_wall_there = False
    if no_wall_there:
        string += " "

    # robot's orientation appearance "^>v<"
    no_robot_there = True
    for robot in board.livingRobots:
        if (col,row) == robot.loc:
            if robot.orient == 0:
                orient_string = "^"
            elif robot.orient == 1:
                orient_string = ">"
            elif robot.orient == 2:
                orient_string = "v"
            elif robot.orient == 3:
                orient_string = "<"

            string += orient_string
            no_robot_there = False
    if no_robot_there:
        string += " "

    # wall "[" or nothing if 
    # TODO in future: instead make it "L" for laser or "P" for pusher, if it's that instead
    no_wall_there = True
    for p in square.propertyList:
        if p.__class__.__name__ == 'Wall' and p.orient == 1:
            string += "]"
            no_wall_there = False
    if no_wall_there:
        string += " "

    return string

def getLineThreeString(board,row,col):
    """Produce string for third line of an ASCII grid cell"""
    string = ""
    square = board.grid[row][col][0]
    
    # add "f" if there's a flag there
    # TODO make it be the NUMBER of the flag, instead (figure out how best to access this; loop through flagLocList?)
    no_flag_there = True
    for p in square.propertyList:
        if p.__class__.__name__ == 'Flag':
            string += "F"
            no_flag_there = False
    if no_flag_there:
        string += " "

    # wall "=" or nothing if 
    # TODO in future: instead make it "L" for laser or "P" for pusher, if it's that instead
    no_wall_there = True
    for p in square.propertyList:
        if p.__class__.__name__ == 'Wall' and p.orient == 2:
            string += "="
            no_wall_there = False
    if no_wall_there:
        string += " "

    # TODO something about spawnLoc could go here; figure out formatting to use!
    # first char of player name or nothing in upper-left corner of square
    no_spawnloc_there = True
    for robot in board.livingRobots:
        if (col,row) == robot.spawnLoc:
            string += robot.playerName[0]
            no_spawnloc_there = False
    if no_spawnloc_there:
        string += " "

    return string

# FIXME I want this to do the three lines, but I need to make sure those lines are getting passed
# the right row and looping through all the columns
def doRow(board,row):
    """Return string for a row worth of ASCII board cells"""
    string = "|"
    for col in range(len(board.grid[row])):
        string += getLineOneString(board,row,col)
        string += "|"
    string += "\n|"

    for col in range(len(board.grid[row])):
        string += getLineTwoString(board,row,col)
        string += "|"
    string += "\n|"

    for col in range(len(board.grid[row])):
        string += getLineThreeString(board,row,col)
        string += "|"
    string += "\n"

    return string

def printAsciiBoard(board):
    """Return string for an ASCII-formatted board"""
    output = ""
    output += rowSepString(board)
    for row in range(len(board.grid)):
        output += doRow(board,row)
        output += rowSepString(board)

    return output
