from collections import namedtuple
import csv
import random
import asciiboard

Location = namedtuple("Location", ["x","y"]) # named tuple for coordinates only
Position = namedtuple("Position", ["loc","orient"]) # named tuple for Loc + orient

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
    def __init__(self, createdRobots,
                 flagLocList=[Location(0,2),Location(0,4)],
                 wallPosList=[Position(Location(5,5),2),Position(Location(5,5),3)],
                 laserPosList=[Position(Location(6,6),3),Position(Location(0,8),2),Position(Location(1,3),0),Position(Location(2,2),1)]):  # TODO generate these better with a function later
        self.numPhases = 5 # number of instruction positions (register phases)
        #print(self.board)
        self.deck = Deck()
        self.handSize = 9 # TODO take this from settable user input
        self.board = Board(createdRobots,flagLocList,wallPosList,laserPosList,self.handSize)
        self.gameOverManGameOver = False
        self.numFlags = len(flagLocList)


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
        self.board.fireLasers()
        self.touchSquare()

    def cleanUp(self):
        for robot in self.board.functionalRobots:
            if (self.board.grid[robot.y][robot.x][0].hasComponent(Wrench)):
                self.board.healRobot()
                print("Old spawn is {},{}.".format(robot.spawnLoc.x, robot.spawnLoc.y))
                robot.spawnLoc = Location(robot.x,robot.y) #if you're at a wrench, change your spawn to be the square you're on
                print("New spawn is {},{}.".format(robot.spawnLoc.x,robot.spawnLoc.y))

            if (self.board.grid[robot.y][robot.x][0].hasComponent(Hammer)):
                pass

    # take all cards back from hands and instruction sets and put them in the discard pile
        for robot in self.board.robotList:
            for i in range(0,len(robot.hand)):  #discard all cards that were dealt but haven't been assigned to register phases
                self.deck.discard(robot.hand.pop())
            if robot.dead == True:
                robot.dead = False
                robot.orient = 2 #must happen before the respawn so that it prints properly at the end of updateRoLoc #TODO make this user-settable
                self.board.updateRoLoc(robot,robot.spawnLoc.x,robot.spawnLoc.y)
                print("Robot {} has riiiiised from the deaaaaad!".format(robot.playerName))
        for robot in self.board.turnedOnRobots: #discard all cards that aren't locked into a register phase
            # freeSlots is the number of instructions that are not locked, equal to the hand size minus the damage taken
            freeSlots = min(self.handSize - robot.damage, robot.numInstructions) # this if makes sure that you never clean up more than five instructions (so, 5 or number of free slots, whichever is less)
            for i in range (0,freeSlots):
                self.deck.discard(robot.instructions.pop(i))
                robot.instructions.insert(i,None)

    def handleCards(self, phase):

        #TODO why the fuck is this the instersection of functionalRobots and functionalRobots...one is supposed to be living???!?
        #print(list(set(self.board.functionalRobots).intersection(self.board.functionalRobots)))
        #print(list(set(self.board.functionalRobots).intersection(self.board.functionalRobots))[0].instructions[phase].priority)

        for robot in sorted(list(set(self.board.functionalRobots)), key=lambda robot: robot.instructions[phase].priority, reverse=True):
        #for robot in list(set(self.board.functionalRobots).intersection(self.board.functionalRobots)):
            robot.instructions[phase].executeCard(self.board, robot)
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
            if (self.board.grid[robot.y][robot.x][0].hasComponent(Flag)): # TODO also add in wrenches 'n' shit
                print("Old spawn is {},{}.".format(robot.spawnLoc.x, robot.spawnLoc.y))
                robot.spawnLoc = Location(robot.x,robot.y) #if you're at a flag, change your spawn to be the square you're on
                print("New spawn is {},{}.".format(robot.spawnLoc.x,robot.spawnLoc.y))
                if robot.checkpoint < self.numFlags: #prevents a robot that has won from index erroring the flagLocList
                    print(self.board.grid[robot.y][robot.x][0].componentList)

#                    if next(c for c in self.board.grid[robot.y][robot.x][0].componentList if type(c) is Flag).id == robot.checkpoint:

                    if self.board.flagLocList[robot.checkpoint] == robot.spawnLoc: #if the nth flag is where you are (n = checkpoint), increase your checkpoint
                        robot.checkpoint = robot.checkpoint+1
                        if robot.checkpoint == self.numFlags:
                            print("You are Winner! Hahaha")             # TODO make an endGame() function
                else:
                    print("Robot has already won; probably needs to be removed from board! (ERROR)")
            else:
                print("Didn't clear a ball!!1")

            pass



class Robot:
    """Names the Robot"""

    def __init__(self, name, spawnLoc, spawnOrient=2):
        self.playerName = name
        #self.appearance = "R"
        self.spawnLoc = spawnLoc
        self._loc = self.spawnLoc # This SHOULD be okay for initialization, but think about it
        self._orient = spawnOrient % 4 # MUST be a value from 0-3; 0 is North, 1 is East, 2 is South, 3 is West
        self.pos = Position(self.loc,self.orient)
        self.checkpoint = 0 # this is the last flag that the robot touched; starts at 0
        # These are five dummy cards; later they'll get put in elsewise
        self.instructions = [None, None, None, None, None] # TODO add Nones in a loop
        self.numInstructions = 5
        #self.hand = [TurnCard(3,600),MoveCard(5,600),TurnCard(2,600),MoveCard(-4,600),MoveCard(1,600),TurnCard(3,600),MoveCard(2,600),MoveCard(1,600),TurnCard(3,600),MoveCard(2,600)]
        self.hand = []
        self.damage = 0
        self.laserPower = 1 #amount of damage a laser does
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

    def getX(self):
        return self._loc.x

    def setX(self,i):
        self._loc.x = i

    def getY(self):
        return self._loc.y

    def setY(self,i):
        self._loc.y = i

    x = property(getX,setX)
    y = property(getY,setY)

    def getLoc(self):
        return self._loc

    def setLoc(self,i):
        self._loc = i

    loc = property(getLoc,setLoc)



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
    def __init__(self, robotList, flagLocList, wallPosList, laserPosList, handSize):
        """Creates a grid, and fills it with squares"""
        self.grid = []
        #list of spawn point locations, which will change as robots hit flags
        self.spawnLocList = []
        #list of flag locations, which will never change
        self.flagLocList = flagLocList
        self.wallPosList = wallPosList
        self.laserPosList = laserPosList
        #if we don't add robot list into the initializer, we can't use it later
        self.robotList = robotList
        self.numRows = 10
        self.numCols = 10
        self.handSize = handSize # TODO this is shitty and hacky and we shouldn't do this
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

        for wall in self.wallPosList:
            self.grid[wall.loc.y][wall.loc.x][0].addComponent(Wall(wall.orient))

        for laser in self.laserPosList:
            self.grid[laser.loc.y][laser.loc.x][0].addComponent(Laser(laser.orient))

        for flag in self.flagLocList:
            self.grid[flag.y][flag.x][0].addComponent(Flag())

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
        '''
        :return: 0 if no obstacle, 1 if Wall in the way, robot instance if a Robot, and None if off edge of board
        '''
        # if, on my square, there is a wall with matching alignment, return 1 (1 means wall)
        #if self.grid[y][x][0].hasProperty(Wall):
        for component in self.grid[y][x][0].componentList:
            if isinstance(component,Wall):
                if component.orient == orient:
                    return 1

        #if, on the next square (gotten from getNextLoc
        # (which might give None in which case we should return None probably?), presumably), there is a wall with opposite alignment ((i+2)%4), return 1
        #if self.getNextLoc(x,y,orient) == None:
        #    return None


        nextLoc = self.getNextLoc(x,y,orient)

        # return None if you run off the edge of the board
        if not(self.numCols>nextLoc.x>=0 and self.numRows>nextLoc.y>=0):
            return None

        for component in self.grid[nextLoc.y][nextLoc.x][0].componentList:
            if isinstance(component,Wall):
                if (component.orient + 2) % 4 == orient:
                    return 1

        # if, on the next square, there is a robot, return the robot
        for robot in self.getLivingRobots():
            if robot.x == nextLoc.x and robot.y == nextLoc.y:
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

        # before you take each step, make sure you're still alive; break if you're dead
        for step in range(numSteps):
            if not robot.dead:
                self.robotStep(robot,moveDirection)
            else:
                break

            #for robot in [x for x in self.grid[robot.y][robot.x] if isinstance(x,Square)]:
                #any(isinstance(x,Square) for x in game.board.grid[-100][-100]) TODO continue being pleased that we figured this out even though we're not using it


    def robotStep(self,robot,moveDirection):
        nextObst = self.getNextObst(robot.x,robot.y,moveDirection)
        nextLoc = self.getNextLoc(robot.x,robot.y,moveDirection)
        if nextObst == 0:
            self.updateRoLoc(robot,nextLoc.x,nextLoc.y)
            return True
        elif nextObst == 1: # TODO remove this; because it's debugging code
            print("You hit a wall!")
            return False
        elif isinstance(nextObst,Robot): # if there's a robot in the way, move that robot
            if (self.robotStep(nextObst,moveDirection)): #this moves the obstacle robot
                self.updateRoLoc(robot,nextLoc.x,nextLoc.y) #if that obstacle robot move returns True (meaning obstacle robot is now out of the way)
                return True
        elif nextObst == None:
            self.killRobot(robot)
            return True



    def killRobot(self,robot):
        self.updateRoLoc(robot, None, None) #(None,None) is Robot Hell
        robot.damage = 2 #TODO czech that this is the right amount of damage that you should come back to life with
        robot.dead = True
        print("I tell you robot {} dead".format(robot.playerName))
        #TODO implement lives


    def damageRobot(self,robot,damagePoints=1):
        robot.damage += damagePoints
        print("Yowza! Robot {} got {} damajizz!".format(robot.playerName,damagePoints))
        # if we've taken all the damage we can, kill the robot
        if robot.damage >= self.handSize:
            self.killRobot(robot)

    def healRobot(self,robot,healPoints=1):
        robot.damage -= healPoints


    def fireLasers(self):
        """
        copy list of functional robots
        for robot in that list:
            damage getTarget() unless it's none

        for lasers on board:
            if robot on my square:
                damage it
            else
                damage getTarget() unless it's none

        getTarget()
            so long as getNextObst() returns 0, ask getNextObst() about getNextLoc()
            then if you have a robot, damage it!
            (this will just let the function end naturally if it hit a wall, i think)

        """

        for robot in self.functionalRobots:
            target = self.getTarget(robot.x,robot.y,robot.orient)
            if target is not None:
                self.damageRobot(target,robot.laserPower)

        robotHere = False #check current square to see if there's a robot here (board lasers only)
        for laserPos in self.laserPosList:
            for robot in self.robotList:
                if robot.loc == laserPos.loc:
                    # damage robot!
                    self.damageRobot(robot)
                    robotHere = True
                    break
            if not robotHere:
                target = self.getTarget(laserPos.loc.x,laserPos.loc.y,((laserPos.orient+2) % 4))
                if target is not None:
                    self.damageRobot(target)

    def getTarget(self,x,y,orient):
        nextObst = self.getNextObst(x,y,orient)
        nextLoc = self.getNextLoc(x,y,orient)
        while nextObst == 0:
            nextObst = self.getNextObst(nextLoc.x,nextLoc.y,orient)
            nextLoc = self.getNextLoc(nextLoc.x,nextLoc.y,orient)
        if isinstance(nextObst,Robot):
            return nextObst # this is the robot that should take damage
        else:
            return None # no damageable target


    def __str__(self):
        """Prints a properly formatted grid"""
        return asciiboard.printAsciiBoard(self)


class Square():
    """Creates an appearance for the square"""
    def __init__(self):
        self.appearance = "."
        self.componentList = []

    def addComponent(self,component):
        self.componentList.append(component)

#if we find out that there exists a real function like this, use that instead TODO test for robustness
    def hasComponent(self,compType):
        answer = False
        for component in self.componentList:
            if isinstance(component, compType):
                answer = True
                break
        return answer

    def __str__(self):
        output = self.appearance
        for component in self.componentList:
            output = output + component.appearance
        return output


class SquareComponent():
    def __init__(self):
        pass

class Flag(SquareComponent):
    counter = 0
    def __init__(self):
        self.appearance = "F"
        self.id = Flag.counter
        Flag.counter += 1

class Wrench(SquareComponent):
    def __init__(self):
        self.appearance = "W"

class Hammer(SquareComponent):
    def __init__(self):
        self.appearance = "H"

class Wall(SquareComponent):
    def __init__(self,orient):
        self.orient = orient
        #create appearance for wall based on orientation
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
    def __init__(self,orient):
        self.orient = orient
#        self.numBeams = beams
#        self.numDamage = damage
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
        print("This should never happen because that would mean that there's a card type without its own execute function!")

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
