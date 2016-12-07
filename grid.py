from collections import namedtuple
from squares import *
import serialize_objects as so


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
    wallList = [] #[[5,5,2],[5,5,3]] #TODO probably repackage these to be ((x,y),o) rather than [x,y,o]
    laserList = [] #[[6,6,3],[0,8,2],[1,3,0],[2,2,1]]


    grid = Grid(numRows, numCols)

    for wall in wallList:
        grid[wall[1]][wall[0]][0].addComponent(Wall(wall[2]))

    for laser in laserList:
        grid[laser[1]][laser[0]][0].addComponent(Laser(laser[2]))
        grid.laserPosList.append(Position(Location(laser[0],laser[1]),laser[2]))

    #hacky shit
    grid[2][4][0].addComponent(Wrench())
    grid[3][1][0].addComponent(Hammer())

    return grid


if __name__ == "__main__":
    grid = generateGrid()
    so.writeGridToFile(grid)


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