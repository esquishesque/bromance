from collections import namedtuple

Location = namedtuple('Location', ['x','y'])


class Game:
    """Creates Robot(s), creates a Board"""
    def __init__(self):
        robotList = []
        robot = Robot() # TODO dummy robot to populate the list, get real robots!
        #later the list will be populated by something else but for now it's just a single robot
        robotList.append(robot) #the order of this list should never change (deprecated fact?)
        self.board = Board(robotList)
        print(self.board)

    def play(self):
        self.executePhase()

    def executeTurn(self):

        # for 5:
        # self.executePhase()
        #
        # self.cleanUp()

        pass

    def executePhase(self):
        self.handleCards()

        #boardMoves()
        #lasersFire()
        #touchSquare()

    def handleCards(self):
        tempCard = MoveCard() # TODO get real cards
        tempRobot = self.board.robotList[0] # TODO talk to robots to get cards

        # TODO block that loops through by priority (use LPQ?)

        #execute card
        if isinstance(tempCard, MoveCard):
            self.board.robotMove(tempRobot, tempCard.getNumSteps())
        elif isinstance(tempCard, TurnCard):
            self.board.robotTurn(tempRobot, tempCard.getNumSteps())
        else:
            # TODO should throw exception
            print('trying to execute card of invalid type')

    def touchSquare(self):
        for robot in self.board.robotList:
            #self.board.grid[self.board.robotList[0].getLoc().x][self.board.robotList[0].getLoc().y][0]
            pass

    def deal(self):
        pass

    
        
class Robot:
    """Names the Robot"""
    def __init__(self):
        self.playerName = "Player One"
        #self.appearance = "R"
        self.spawnLoc = Location(0,0) #TODO have this assigned somehow during initialization (randomize, or something)
        self.loc = self.spawnLoc # This SHOULD be okay for initialization, but think about it
        self.orient = 2 # MUST be a value from 0-3; 0 is North, 1 is East, 2 is South, 3 is West
        self.checkpoint = 0 # this is the last flag that the robot touched; starts at 0

    def getLoc(self):
        return self.loc

    def setLoc(self,x,y):
        self.loc = Location(x,y)

    def getOrient(self):
        return self.orient

    # %4 is mod4, so that the robot's orientation is always between 0-3
    def setOrient(self,i):
        self.orient = i%4

    def getSpawnLoc(self):
        return self.spawnLoc

    def setSpawnLoc(self,x,y):
        self.spawnLoc = Location(x,y)

    def __str__(self):
        #this makes the robot's appearance reflect its orientation
        if self.getOrient() == 0:
            return "^"
        elif self.getOrient() == 1:
            return ">"
        elif self.getOrient() == 2:
            return "v"
        elif self.getOrient() == 3:
            return "<"
        else:                           # TODO should throw exception
            print ("Unexpected value in robot.__str__")


class Board:
    def __init__(self, robotList):
        """Creates a grid, and fills it with squares"""
        self.grid = []
        #list of spawn point locations, which will change as robots hit flags
        self.spawnLocList = []
        #list of flag locations, which will never change
        self.flagLocList = []
        #if we don't add robot list into the initializer, we can't use it later
        self.robotList = robotList
        
        #populate list of flag locations; crucially this is [x,y] NOT [row,col]
        tempFlagPoint = Location(9,9) # TODO generate these better with a function later
        self.flagLocList.append(tempFlagPoint)        
        
        # fill a grid representing a 10x10 board with Squares
        numRows = 10
        numCols = 10
        for y in range(numRows):
            self.grid.append([])
            for x in range(numCols):
                self.grid[y].append([Square()])

        self.grid[tempFlagPoint.y][tempFlagPoint.x][0].addProperty(Flag())
        for robot in self.robotList:
            self.grid[robot.spawnLoc.y][robot.spawnLoc.x][0].addProperty(Spawn())

    def updateRoLoc(self,robot,x,y):
        robot.setLoc(x,y)
        print(self)

    def updateRoOrient(self,robot,i):
        robot.setOrient(i)
        print(self)

    def robotTurn(self,robot,numSteps):
        self.updateRoOrient(robot,robot.getOrient() + numSteps)

    def robotMove(self,robot,numSteps):
        if robot.getOrient() == 0: # facing north, subtract from y
            self.updateRoLoc(robot,robot.getLoc().x,robot.getLoc().y-numSteps)
        elif robot.getOrient() == 1: # facing east, add to x
            self.updateRoLoc(robot,robot.getLoc().x+numSteps,robot.getLoc().y)
        elif robot.getOrient() == 2: # facing south, add to y
            self.updateRoLoc(robot,robot.getLoc().x,robot.getLoc().y+numSteps)
        elif robot.getOrient() == 3: # facing west, subtract x
            self.updateRoLoc(robot,robot.getLoc().x-numSteps,robot.getLoc().y)
        else:                               # TODO should throw exception
            print("Unexpected value in robotMove")

    def __str__(self):
        """Prints a properly formatted grid"""
        output = ""
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                for square in range(len(self.grid[row][col])):
                    output = output + str(self.grid[row][col][square])
                for robot in self.robotList:
                    if (col,row) == robot.getLoc():
                        output = output + str(robot)
                output = output + '|'
            output = output + "\n"
        return output


class Square():
    """Creates an appearance for the square"""
    def __init__(self):
        self.appearance = '.'
        self.propertyList = []

    def addProperty(self,property):
        self.propertyList.append(property)

    def __str__(self):
        output = self.appearance
        for property in self.propertyList:
            output = output + property.appearance
        return output


class SquareProperty():
    def __init__(self):
        pass


class Flag(SquareProperty):
    def __init__(self):
        self.appearance = "F"


class Spawn(SquareProperty):
    def __init__(self):
        self.appearance = "S"


class Card():
    def __init__(self):
        self.priority = 600 # TODO make deck
        self.numSteps = 1 # TODO make deck

    def getNumSteps(self):
        return self.numSteps
        
        
class TurnCard(Card):
    #def __init__(self):
    pass



class MoveCard(Card):
    #def __init__(self):
    pass