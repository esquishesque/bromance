from collections import namedtuple
import csv
import random

Location = namedtuple("Location", ["x","y"])


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
    def __init__(self, createdRobots,flagLocList=[Location(0,2),Location(0,4)]):  # TODO generate these better with a function later
        self.numPhases = 5 # number of instruction positions (register phases)
        self.board = Board(createdRobots,flagLocList)
        #print(self.board)
        self.deck = Deck()
        self.handSize = 9 # TODO take this from settable user input
        self.gameOverManGameOver = False


    def play(self):
        while(self.gameOverManGameOver==False):
            self.executeTurn()

    def executeTurn(self):

        self.dealHands()


        for robot in self.board.turnedOnRobots:
            print("current board:\n{}".format(self.board))
            robot.selectInstructions()

        for phase in range(0,self.numPhases):
            self.executePhase(phase)



        self.cleanUp()


    def dealHands(self):
    # for each card that should be dealt, give one card to each robot, if they need one
        for i in range(0,self.handSize):
            for robot in self.board.turnedOnRobots:
                # TODO check if they need a card, based on damage; use global variable "handSize"
                    if robot.damage + len(robot.hand) < self.handSize:
                        robot.hand.append(self.deck.draw()) # pop a card from the deck and pass it to each robot's hand


    def executePhase(self,phase):
    # grab one phase at a time and pass them to handleCards

        self.handleCards(phase)
        #boardMoves()
        #lasersFire()
        self.touchSquare()

    def cleanUp(self):
    # take all cards back from hands and instruction sets and put them in the discard pile
        for robot in self.board.robotList:
            for i in range(0,len(robot.hand)):  #discard all cards that were dealt but haven't been assigned to register phases
                self.deck.discard(robot.hand.pop())
            if robot.dead == True:
                robot.dead = False
                robot.orient = 2 #must happen before the respawn so that it prints properly at the end of updateRoLoc #TODO make this user-settable
                self.board.updateRoLoc(robot,robot.spawnLoc.x,robot.spawnLoc.y)
                print("Robot has riiiiised from the deaaaaad!")
        for robot in self.board.turnedOnRobots: #discard all cards that aren't locked into a register phase
            # freeSlots is the number of instructions that are not locked, equal to the hand size minus the damage taken
            freeSlots = self.handSize - robot.damage
            # this if makes sure that you never clean up more than five instructions (so, 5 or number of free slots, whichever is less)
            if freeSlots > robot.numInstructions:
                freeSlots = robot.numInstructions
            for i in range (0,freeSlots):
                self.deck.discard(robot.instructions.pop(i))
                robot.instructions.insert(i,None)

    def handleCards(self,phase):

        for robot in list(set(self.board.functionalRobots).intersection(self.board.functionalRobots)):
            robot.instructions[phase].executeCard(self.board,robot)
            print(self.board)

        # # TODO block that loops through by priority (use LPQ?)
        #
        # #execute card
        # if isinstance(tempCard, MoveCard):
        #     self.board.robotMove(tempRobot, tempCard.numSteps)
        # elif isinstance(tempCard, TurnCard):
        #     self.board.robotTurn(tempRobot, tempCard.numSteps)
        # else:
        #     # TODO should throw exception
        #     print("trying to execute card of invalid type")


    def touchSquare(self):
        for robot in self.board.functionalRobots:
            if (self.board.grid[robot.loc.y][robot.loc.x][0].hasProperty(Flag)): # TODO also add in wrenches 'n' shit
                print("Old spawn is {},{}.".format(robot.spawnLoc.x, robot.spawnLoc.y))
                robot.spawnLoc = Location(robot.loc.x,robot.loc.y) #if you're at a flag, change your spawn to be the square you're on
                print("New spawn is {},{}.".format(robot.spawnLoc.x,robot.spawnLoc.y))
                if robot.checkpoint < len(self.board.flagLocList): #prevents a robot that has won from index erroring the flagLocList
                    if self.board.flagLocList[robot.checkpoint] == robot.spawnLoc: #if the nth flag is where you are (n = checkpoint), increase your checkpoint
                        robot.checkpoint = robot.checkpoint+1
                        if robot.checkpoint == len(self.board.flagLocList):
                            print("You are Winner! Hahaha")             # TODO make an endGame() function
                else:
                    print("Robot has already won; probably needs to be removed from board!")
            else:
                print("Didn't clear a ball!!1")

            pass



class Robot:
    """Names the Robot"""

    def __init__(self, name, spawnLoc):
        self.playerName = name
        #self.appearance = "R"
        self.spawnLoc = spawnLoc
        self.loc = self.spawnLoc # This SHOULD be okay for initialization, but think about it
        self._orient = 2 # MUST be a value from 0-3; 0 is North, 1 is East, 2 is South, 3 is West
        self.checkpoint = 0 # this is the last flag that the robot touched; starts at 0
        # These are five dummy cards; later they'll get put in elsewise
        self.instructions = [None, None, None, None, None] # TODO add Nones in a loop
        self.numInstructions = 5
        #self.hand = [TurnCard(3,600),MoveCard(5,600),TurnCard(2,600),MoveCard(-4,600),MoveCard(1,600),TurnCard(3,600),MoveCard(2,600),MoveCard(1,600),TurnCard(3,600),MoveCard(2,600)]
        self.hand = []
        self.damage = 0
        self.dead = False
        self.turnedOff = False

    def selectInstructions(self):
        instructionsAdded = 0 #this is counting how many Nones we've replaced so that we know which instruction we're on
        while(None in self.instructions): #this loops through so long as there are any Nones left in the list
            for cardIndex in range (len(self.hand)): #this loops through all the cards in the hand in order to print them
                print("{}: {}".format(cardIndex,self.hand[cardIndex]))
            while True:
                raw_choice = input("robot {}! pick a card, any card! (enter 'q' quit being so loopy): ".format(self.playerName))
                if raw_choice == "q":
                   quit()
                try:
                    choice = int(raw_choice)
                    break
                except ValueError:
                    continue
            if 0<=choice<len(self.hand): #this checks whether the user input is in the valid range #TODO should also guarantee that input is a valid int
                self.instructions[instructionsAdded]=self.hand.pop(choice)
                instructionsAdded=instructionsAdded+1
            else:
                print("not a valid choice ><")


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
    def __init__(self, robotList, flagLocList):
        """Creates a grid, and fills it with squares"""
        self.grid = []
        #list of spawn point locations, which will change as robots hit flags
        self.spawnLocList = []
        #list of flag locations, which will never change
        self.flagLocList = flagLocList
        #if we don't add robot list into the initializer, we can't use it later
        self.robotList = robotList
        self.numRows = 10
        self.numCols = 10
        self._livingRobots = []
        self._turnedOnRobots = []
        self._functionalRobots = []

        # #populate list of flag locations; crucially this is [x,y] NOT [row,col]
        # tempFlagPoint = Location(0,2) # TODO generate these better with a function later
        # self.flagLocList.append(tempFlagPoint)
        # tempFlagPointTwo = Location(0,4)
        # self.flagLocList.append(tempFlagPointTwo)

        # fill a grid representing a 10x10 board with Squares
        for y in range(self.numRows):
            self.grid.append([])
            for x in range(self.numCols):
                self.grid[y].append([Square()])

        # add walls to board
        self.grid[5][5][0].addProperty(Wall(2))
        self.grid[5][5][0].addProperty(Wall(3))

        for flag in self.flagLocList:
            self.grid[flag.y][flag.x][0].addProperty(Flag())

#        for robot in self.robotList:
#            self.grid[robot.spawnLoc.y][robot.spawnLoc.x][0].addProperty(Spawn())

    def getLivingRobots(self): # return only robots that are not dead (i.e., alive)
        self._livingRobots = []
        for robot in self.robotList:
            if robot.dead == False:
                self._livingRobots.append(robot)
        return self._livingRobots

    # every time we get living robots, it will go through the function getLivingRobots() instead
    livingRobots = property(getLivingRobots)

    def getTurnedOnRobots(self):
        self._turnedOnRobots = [] #empty the list of turned on robots
        for robot in self.robotList:
            if robot.turnedOff == False:
                self._turnedOnRobots.append(robot)
        return self._turnedOnRobots

    # every time we get robots that are turned on, it will go through the function getTurnedOnRobots() instead
    turnedOnRobots = property(getTurnedOnRobots)

    def getFunctionalRobots(self):
        self._functionalRobots = []
        for robot in self.robotList:
            if robot.turnedOff == False and robot.dead == False:
                self._functionalRobots.append(robot)
        return self._functionalRobots

    # every time we get robots that are turned on AND alive, it will go through the function getFunctionalRobots() instead
    functionalRobots = property(getFunctionalRobots)


    # Does calculus to figure out coordinates of next square given direction you want to move
    def getNextLoc(self,x,y,orient):


        if orient == 0: # facing north, subtract from y
            y=y-1
        elif orient == 1: # facing east, add to x
            x=x+1
        elif orient == 2: # facing south, add to y
            y=y+1
        elif orient == 3: # facing west, subtract x
            x=x-1
        else:                               # TODO should throw exception
            print("Unexpected value in getNextLoc")

        return Location(x,y)


    def getNextObst(self,x,y,orient):
        # if, on my square, there is a wall with matching alignment, return 1 (1 means wall)
        #if self.grid[y][x][0].hasProperty(Wall):
        for property in self.grid[y][x][0].propertyList:
            if isinstance(property,Wall):
                if property.orient == orient:
                    return 1

        #if, on the next square (gotten from getNextLoc
        # (which might give None in which case we should return None probably?), presumably), there is a wall with opposite alignment ((i+2)%4), return 1
        #if self.getNextLoc(x,y,orient) == None:
        #    return None


        nextLoc = self.getNextLoc(x,y,orient)

        if not(self.numCols>nextLoc.x>=0 and self.numRows>nextLoc.y>=0):
            return None

        for property in self.grid[nextLoc.y][nextLoc.x][0].propertyList:
            if isinstance(property,Wall):
                if (property.orient + 2) % 4 == orient:
                    return 1

        # if, on the next square, there is a robot, return the robot
        for robot in self.getLivingRobots():
            if robot.loc.x == nextLoc.x and robot.loc.y == nextLoc.y:
                return robot

        # return 0
        return 0

    def updateRoLoc(self,robot,x,y):
        robot.loc=Location(x,y)
        #print(self)

    def updateRoOrient(self,robot,i):
        robot.orient = i
        #print(self)

    def robotTurn(self,robot,numSteps):
        self.updateRoOrient(robot,robot.orient + numSteps)


    def robotMove(self,robot,numSteps=1,moveDirection=None):
        if moveDirection == None: # moveDirection can be a direction other than the robot's orientation because you can get pushed e.g., sideways, which will use robotMove()
            moveDirection = robot.orient

        # If we're moving backwards, flip the move direction and make numSteps positive so the for loop below works
        if numSteps < 0:
            numSteps = numSteps * -1
            moveDirection = (moveDirection + 2) % 4

        for step in range(numSteps):
            nextObst = self.getNextObst(robot.loc.x,robot.loc.y,moveDirection)
            nextLoc = self.getNextLoc(robot.loc.x,robot.loc.y,moveDirection)
            if nextObst == 0:
                self.updateRoLoc(robot,nextLoc.x,nextLoc.y)
                return True
            elif nextObst == 1: # TODO remove this; because it's debugging code
                print("You hit a wall!")
                return False
            elif isinstance(nextObst,Robot): # if there's a robot in the way, move that robot
                if (self.robotMove(nextObst,1,moveDirection)): #this moves the obstacle robot
                    self.updateRoLoc(robot,nextLoc.x,nextLoc.y) #if that obstacle robot move returns True (meaning obstacle robot is now out of the way)
                    return True
            elif nextObst == None:
                self.killRobot(robot)
                return True
                break #if the robot dies mid move-2 (or move-3 or move>1) this will break out of the step loop, preventing looking for the nextObst when the robot has a location of None,None


            #for robot in [x for x in self.grid[robot.loc.y][robot.loc.x] if isinstance(x,Square)]:
                #any(isinstance(x,Square) for x in game.board.grid[-100][-100]) TODO continue being pleased that we figured this out even though we're not using it

    def killRobot(self,robot):
        self.updateRoLoc(robot,None,None) # (None,None) is Robot Hell
        robot.damage = 2 #TODO czech that this is the right amount of damage
        robot.dead = True
        print("I tell you robot {} dead".format(robot))
        #TODO implement lives
        #TODO when robots take damage, have the damage taking function check whether they've taken too much and if so kill them

    def __str__(self):
        """Prints a properly formatted grid"""
        output = ""
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                for square in range(len(self.grid[row][col])):
                    output = output + str(self.grid[row][col][square])
                for robot in self.livingRobots:
                    if (col,row) == robot.loc:
                        output = output + str(robot) + robot.playerName
                    if (col,row) == robot.spawnLoc:
                        output = output + "s" + robot.playerName
                output = output + "|"
            output = output + "\n"
        return output


class Square():
    """Creates an appearance for the square"""
    def __init__(self):
        self.appearance = "."
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

class Wall(SquareProperty):
    def __init__(self,orient):
        self.orient = orient
        #create appearnce for wall based on orientation
        if self.orient == 0:
            self.appearance = "-"
        elif self.orient == 1:
            self.appearance = "]"
        elif self.orient == 2:
            self.appearance = "_"
        elif self.orient == 3:
            self.appearance = "["
        else:                           # TODO should throw exception
            print ("Unexpected value in Wall.appearance")


class Laser(Wall):
    pass

class Pusher(Wall):
    pass

#class Spawn(SquareProperty):
#    def __init__(self):
#        self.appearance = "S"


class Card():
    def __init__(self,numSteps,priority):
        self.priority = priority # TODO make deck
        self.numSteps = numSteps # TODO make deck

    def executeCard(self,board,robot):
        print("This should never happen!")

    #def __str__(self):
    #    print()


class TurnCard(Card):
    #def __init__(self):
    def executeCard(self,board,robot):
        board.robotTurn(robot,self.numSteps)

    def __str__(self):
        return "turn {}; priority: {}".format(self.numSteps, self.priority)


class MoveCard(Card):
    #def __init__(self):
    def executeCard(self,board,robot):
        board.robotMove(robot,self.numSteps)

    def __str__(self):
        return "move {}; priority: {}".format(self.numSteps, self.priority)


class Deck():
    def __init__(self):
        self.drawPile = []
        self.discardPile = []
        with open("deck.csv", newline="") as csvfile:
            cardreader = csv.reader(csvfile, delimiter=",")
            for row in cardreader:
                if row[0] == "turn":
                    self.drawPile.append(TurnCard(int(row[1]),int(row[2])))
                elif row[0] == "move":
                    self.drawPile.append(MoveCard(int(row[1]),int(row[2])))
                else:
                    print("error: found invalid card type in deck file!")
        random.shuffle(self.drawPile)

    def draw(self):
        """returns a single card from the draw pile, and reshuffles discardPile into drawPile if necessary"""
        if len(self.drawPile)<=0: #if the draw pile is empty...
            if len(self.discardPile)<=0: #(except if the discard pile is also empty then be sad) #TODO this should throw a real exception
                print("nooooooo draw pile and discard pile are both empty :(")
            for i in range(0,len(self.discardPile)): #loop through the cards in the discard pile
                self.drawPile.append(self.discardPile.pop()) # and move them to the draw pile
            random.shuffle(self.drawPile) #then shuffle
        return self.drawPile.pop()

    def discard(self,card):
        self.discardPile.append(card)

    # def __str__(self): #this would have to be changed if we want it because self.contents is no longer a thing
    #     output = ""
    #     for card in self.contents:
    #         output = output+str(card)+"\n"
    #     return output
