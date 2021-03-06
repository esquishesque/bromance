from game import *
# Print the board in a nice ASCII format

# dict of (orient (int), enspinment (int), is_express (bool)) tuples to appearances
conveyorAppearances = {
    # non-turning regular
    (0,0,False): "↑",
    (1,0,False): "→",
    (2,0,False): "↓",
    (3,0,False): "←",

    # right-turning regular
    (0,1,False): "⥜",
    (1,1,False): "⥟",
    (2,1,False): "⥡",
    (3,1,False): "⥚",

    # left-turning regular
    (0,-1,False): "⥠",
    (1,-1,False): "⥛",
    (2,-1,False): "⥝",
    (3,-1,False): "⥞",

    # non-turning express
    (0,0,True): "⤒",
    (1,0,True): "⇥",
    (2,0,True): "⤓",
    (3,0,True): "⇤",

    # right-turning express
    (0,1,True): "⥔",
    (1,1,True): "⥗",
    (2,1,True): "⥙",
    (3,1,True): "⥒",

    # left-turning express
    (0,-1,True): "⥘",
    (1,-1,True): "⥓",
    (2,-1,True): "⥙",
    (3,-1,True): "⥖",
}

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
    no_hammer_there = True
    no_wrench_there = True
    upperRightCorner = " "

    for p in square.componentList:
        if p.__class__.__name__ == 'Laser' and p.orient == 0:
            string += "L"
            no_wall_there = False
        elif p.__class__.__name__ == 'Wall' and p.orient == 0:
            string += "="
            no_wall_there = False

        if p.__class__.__name__ == 'Conveyor':
            upperRightCorner = conveyorAppearances[(p.orient, p.enspinment, False)]
        elif p.__class__.__name__ == 'ExpressConveyor':
            upperRightCorner = conveyorAppearances[(p.orient, p.enspinment, True)]
        elif p.__class__.__name__ == 'Gear':
            if p.enspinment == 1:
                upperRightCorner = "⟳"
            elif p.enspinment == -1:
                upperRightCorner = "⟲"
            else:
                raise Exception("Unknown enspinment for gear ({})".format(p.enspinment))

        if p.__class__.__name__ == 'Hammer':
            upperRightCorner = "H"
            no_hammer_there = False

        if p.__class__.__name__ == 'Wrench':
            upperRightCorner = "W"
            no_wrench_there = False

    if no_wall_there:
        string += " "

    # TODO: make this conveyor belt ("nesw"/"NESW" for regular/express); for no just blank!
    # TODIDN'T: that doesn't allow us to have turns, so we did this instead!
    string += upperRightCorner

    return string

def getLineTwoString(board,row,col):
    """Produce string for second line of an ASCII grid cell"""
    string = ""
    square = board.grid[row][col][0]

    # wall "[" or nothing if 
    # TODO in future: instead make it "L" for laser or "P" for pusher, if it's that instead
    no_wall_there = True
    for p in square.componentList:
        if p.__class__.__name__ == 'Laser' and p.orient == 3:
            string += "L"
            no_wall_there = False
        elif p.__class__.__name__ == 'Wall' and p.orient == 3:
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
    for p in square.componentList:
        if p.__class__.__name__ == 'Laser' and p.orient == 1:
            string += "L"
            no_wall_there = False
        elif p.__class__.__name__ == 'Wall' and p.orient == 1:
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
    for p in square.componentList:
        if p.__class__.__name__ == 'Flag':
            string += "F"
            no_flag_there = False
    if no_flag_there:
        string += " "

    # wall "=" or nothing if 
    # TODO in future: instead make it "L" for laser or "P" for pusher, if it's that instead
    no_wall_there = True
    for p in square.componentList:
        if p.__class__.__name__ == 'Laser' and p.orient == 2:
            string += "L"
            no_wall_there = False
        elif p.__class__.__name__ == 'Wall' and p.orient == 2:
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
