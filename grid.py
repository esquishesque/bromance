from collections import namedtuple
from squares import *

# Location = namedtuple("Location", ["x","y"]) # named tuple for coordinates only
# Position = namedtuple("Position", ["loc","orient"]) # named tuple for Loc + orient


class Location:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other,Location):
            return (self.x, self.y) == (other.x, other.y)
        elif isinstance(other,tuple):
            return (self.x, self.y) == other
        else:
            return False



class Position:
    def __init__(self,loc,orient):
        self.loc = loc
        self.orient = orient

    def __eq__(self, other):
        if isinstance(other,Position):
            return (self.loc, self.orient) == (other.loc, other.orient)
        elif isinstance(other,tuple):
            print("huh, i didn't expect this to happen...  (hint: look in Position equality function)")
            return ((self.loc.x, self.loc.y),self.orient) == other
        else:
            return False



class Grid(list):
    def __init__(self,numRows,numCols):
        for y in range(numRows):
            self.append([])
            for x in range(numCols):
                self[y].append([Square()])
        self.laserPosList = []



def generateGrid():
    numRows = 10
    numCols = 10
    wallList = [[8,4,2]] #[[5,5,2],[5,5,3]] #TODO probably repackage these to be ((x,y),o) rather than [x,y,o]
    laserList = [[9,6,1]] #[[6,6,3],[0,8,2],[1,3,0],[2,2,1]]
    conveyorList = [[5,0,3,0],
                    [6,0,3,0],
                    [6,2,0,0],
                    [6,3,0,0],
                    [8,3,2,0],
                    [8,4,2,0],
                    [2,5,2,0],
                    [2,6,2,0],
                    [2,7,2,-1],
                    [3,7,1,0],
                    [8,6,2,0],
                    [9,7,2,0],
                    [9,8,2,0],
                    [9,9,2,0]]

    expressConveyorList = [[4,5,1,0],
                           [5,5,1,0],
                           [6,5,1,1],
                           [6,6,2,0],
                           [6,7,1,0],
                           [7,7,1,0],
                           [8,7,1,0],
                           [7,9,1,0]]

    gearList = [[6,1,1],
                [4,3,-1],
                [3,3,1]]


    grid = Grid(numRows, numCols)

    for wall in wallList:
        grid[wall[1]][wall[0]][0].addComponent(Wall(wall[2]))

    for laser in laserList:
        grid[laser[1]][laser[0]][0].addComponent(Laser(laser[2]))
        grid.laserPosList.append(Position(Location(laser[0],laser[1]),laser[2]))

    for gear in gearList:
            grid[gear[1]][gear[0]][0].addComponent(Gear(gear[2]))

    for conveyor in conveyorList:
            grid[conveyor[1]][conveyor[0]][0].addComponent(Conveyor(conveyor[2],conveyor[3]))

    for expressConveyor in expressConveyorList:
            grid[expressConveyor[1]][expressConveyor[0]][0].addComponent(ExpressConveyor(expressConveyor[2],expressConveyor[3]))

    #hacky shit
    grid[2][4][0].addComponent(Wrench())
    grid[3][1][0].addComponent(Hammer())

    return grid


    #pickle grid

#     with open('data.pickle', 'wb') as f:
#     # Pickle the 'data' dictionary using the highest protocol available.
#     pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
# The following example reads the resulting pickled data.
#
# import pickle
#
# with open('data.pickle', 'rb') as f:
#     # The protocol version used is detected automatically, so we do not
#     # have to specify it.
#     data = pickle.load(f)
