from collections import namedtuple

Location = namedtuple('Location', ['x','y'])


    # def getOrient(self):
    #     return self._orient
    #
    # # %4 is mod4, so that the robot's orientation is always between 0-3
    # def setOrient(self,i):
    #     self._orient = i%4
    #
    # # every time we set orient, it will go through the function setOrient() instead
    # orient = property(getOrient,setOrient)


class Game:
    """Creates Robot(s), creates a Board"""
    def __init__(self):
        createdRobots = []
        robot = Robot() # TODO dummy robot to populate the list, get real robots!
        #later the list will be populated by something else but for now it's just a single robot
        createdRobots.append(robot) #the order of this list should never change (deprecated fact?)
        self.numPhases = 5 # number of instruction positions (register phases)
        self.board = Board(createdRobots)
        print(self.board)

    def play(self):
        self.executeTurn()
        # self.executePhase()

    def executeTurn(self):
        for phase in range(0,self.numPhases):
            self.executePhase(phase)
        # self.cleanUp()


    def executePhase(self,phase):
        # grab one phase at a time and pass them to handleCards

        self.handleCards(phase)

        #boardMoves()
        #lasersFire()
        #touchSquare()

    def handleCards(self,phase):
        pass

        # tempCard = MoveCard(1) # TODO get real cards
        # tempRobot = self.board.robotList[0] # TODO talk to robots to get cards
        #
        # # TODO block that loops through by priority (use LPQ?)
        #
        # #execute card
        # if isinstance(tempCard, MoveCard):
        #     self.board.robotMove(tempRobot, tempCard.numSteps)
        # elif isinstance(tempCard, TurnCard):
        #     self.board.robotTurn(tempRobot, tempCard.numSteps)
        # else:
        #     # TODO should throw exception
        #     print('trying to execute card of invalid type')


    def touchSquare(self):
        for robot in self.board.robotList:
            if (self.board.grid[robot.loc.y][robot.loc.x][0].hasProperty(Flag)): # TODO also add in wrenches 'n' shit
                print('Old spawn is {},{}.'.format(robot.spawnLoc.x, robot.spawnLoc.y))
                robot.spawnLoc = Location(robot.loc.x,robot.loc.y)
                print('New spawn is {},{}.'.format(robot.spawnLoc.x,robot.spawnLoc.y))
                if self.board.flagLocList[robot.checkpoint] == robot.spawnLoc:
                    robot.checkpoint = robot.checkpoint+1
                    if robot.checkpoint == len(self.board.flagLocList):
                        print("You are Winner! Hahaha")             # TODO make an endGame() function
            else:
                print("Didn't clear a ball!!1")

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
        self._orient = 2 # MUST be a value from 0-3; 0 is North, 1 is East, 2 is South, 3 is West
        self.checkpoint = 0 # this is the last flag that the robot touched; starts at 0
        # These are five dummy cards; later they'll get put in elsewise
        #self.instructions = [None, None, None, None, None]
        self.instructions = [MoveCard(1),TurnCard(3),MoveCard(2),TurnCard(1),MoveCard(4)]

    def getOrient(self):
        return self._orient

    # %4 is mod4, so that the robot's orientation is always between 0-3
    def setOrient(self,i):
        self._orient = i%4

    # every time we set orient, it will go through the function setOrient() instead
    orient = property(getOrient,setOrient)

    def __str__(self):
        #this makes the robot's appearance reflect its orientation
        if self.orient == 0:
            return "^"
        elif self.orient == 1:
            return ">"
        elif self.orient == 2:
            return "v"
        elif self.orient == 3:
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
        tempFlagPoint = Location(5,9) # TODO generate these better with a function later
        self.flagLocList.append(tempFlagPoint)
        tempFlagPointTwo = Location(9,9)
        self.flagLocList.append(tempFlagPointTwo)

        # fill a grid representing a 10x10 board with Squares
        numRows = 10
        numCols = 10
        for y in range(numRows):
            self.grid.append([])
            for x in range(numCols):
                self.grid[y].append([Square()])

        for flag in self.flagLocList:
            self.grid[flag.y][flag.x][0].addProperty(Flag())

        for robot in self.robotList:
            self.grid[robot.spawnLoc.y][robot.spawnLoc.x][0].addProperty(Spawn())

    def updateRoLoc(self,robot,x,y):
        robot.loc=Location(x,y)
        print(self)

    def updateRoOrient(self,robot,i):
        robot.orient = i
        print(self)

    def robotTurn(self,robot,numSteps):
        self.updateRoOrient(robot,robot.orient + numSteps)

    def robotMove(self,robot,numSteps):
        if robot.orient == 0: # facing north, subtract from y
            self.updateRoLoc(robot,robot.loc.x,robot.loc.y-numSteps)
        elif robot.orient == 1: # facing east, add to x
            self.updateRoLoc(robot,robot.loc.x+numSteps,robot.loc.y)
        elif robot.orient == 2: # facing south, add to y
            self.updateRoLoc(robot,robot.loc.x,robot.loc.y+numSteps)
        elif robot.orient == 3: # facing west, subtract x
            self.updateRoLoc(robot,robot.loc.x-numSteps,robot.loc.y)
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
                    if (col,row) == robot.loc:
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

#if we find out that there exists a real function like this, use that instead TODO test for robustness
    def hasProperty(self,propType):
        answer = False
        for property in self.propertyList:
            if isinstance(property, propType):
                answer = True
                break
        return answer

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
    def __init__(self,numSteps):
        self.priority = 600 # TODO make deck
        self.numSteps = numSteps # TODO make deck

    def executeCard(self,board,robot):
        print("This should never happen!")


class TurnCard(Card):
    #def __init__(self):
    def executeCard(self,board,robot):
        board.robotTurn(robot,self.numSteps)


class MoveCard(Card):
    #def __init__(self):
    def executeCard(self,board,robot):
        board.robotMove(robot,self.numSteps)