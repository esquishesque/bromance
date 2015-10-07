import unittest
from game import *
#import mock

#SSR = subject scenario result

class TestDealHands(unittest.TestCase):
    def setUp(self):
        self.startLoc = Location(0,0)
        self.game = Game([Robot("R", self.startLoc)])
        self.game.board.robotList[0].hand = []

    def test_dealHands_tenHandSizeNoDamage_handHasTenCards(self):
        self.game.handSize = 10
        self.game.board.robotList[0].damage = 0
        self.game.dealHands()
        self.assertEqual(len(self.game.board.robotList[0].hand),10)

    def test_dealHands_zeroHandSizeNoDamage_handHasZeroCards(self):
        self.game.handSize = 0
        self.game.board.robotList[0].damage = 0
        self.game.dealHands()
        self.assertEqual(len(self.game.board.robotList[0].hand),0)

    def test_dealHands_fiveHandSizeSevenDamage_handHasZeroCards(self):
        self.game.handSize = 5
        self.game.board.robotList[0].damage = 7
        self.game.dealHands()
        self.assertEqual(len(self.game.board.robotList[0].hand),0)

    def test_dealHands_fiveHandSizeThreeDamage_handHasTwoCards(self):
        self.game.handSize = 5
        self.game.board.robotList[0].damage = 3
        self.game.dealHands()
        self.assertEqual(len(self.game.board.robotList[0].hand),2)



    def cleanUp(self):
        pass

class TestCleanUp(unittest.TestCase):
    def setUp(self):
        self.startLoc = Location(0,0)
        self.game = Game([Robot("R", self.startLoc),Robot("C", self.startLoc),Robot("E", self.startLoc)])
        for robot in self.game.board.robotList:
            robot.hand = []
        self.game.handSize = 9


    def test_allRobots_handHasNoCards(self):
        self.game.board.robotList[0].turnedOff = True
        self.game.board.robotList[1].dead = True
        self.game.dealHands()
        self.game.cleanUp()
        for robot in self.game.board.robotList:
            self.assertEqual(len(robot.hand),0)

    def test_discardPile_threeFullRobotHandsDiscarded_twentySevenCardsAddedToDiscardPile(self):
        self.game.dealHands()
        for robot in self.game.board.robotList:
            for i in range(self.game.numPhases):
                robot.instructions[i]=(robot.hand.pop()) #give the top n cards to each robots instructions

        self.game.cleanUp()
        self.assertEqual(len(self.game.deck.discardPile),27)


        self.game.dealHands()
        for robot in self.game.board.robotList:
            for i in range(self.game.numPhases):
                robot.instructions[i]=(robot.hand.pop()) #give the top n cards to each robots instructions

        self.game.cleanUp()
        self.assertEqual(len(self.game.deck.discardPile),54)


    def test_deadRobot_cleanUp_robotReborn(self):
        self.game.board.robotList[0].dead = True
        self.game.cleanUp()
        self.assertFalse(self.game.board.robotList[0].dead)

    def test_damagedRobot_fiveDamage_oneCardLocked(self):
        robot = self.game.board.robotList[0]
        for i in range(robot.numInstructions):
            robot.instructions.append(self.game.deck.draw())
        robot.damage = self.game.handSize - robot.numInstructions + 1 # should be enough damage to lock one instruction card
        cardBeforeCleanUp = robot.instructions[-1]
        self.game.cleanUp()
        self.assertIs(cardBeforeCleanUp,robot.instructions[-1]) # locked card from before cleanUp() has stuck around

class TestRobotTurn(unittest.TestCase):
    def setUp(self):
        self.game = Game([Robot("R", Location(0,0))])
        self.robot = self.game.board.robotList[0]
        self.robot.orient = 0

    def test_robotFacingNorth_turnOne_robotFacingEast(self):
        self.game.board.robotTurn(self.robot,1)
        self.assertEqual(self.robot.orient,1)

    def test_robotFacingNorth_turnMinusOne_robotFacingWest(self):
        self.game.board.robotTurn(self.robot,-1)
        self.assertEqual(self.robot.orient,3)

    def test_robotFacingNorth_turnTen_robotFacingSouth(self):
        self.game.board.robotTurn(self.robot,10)
        self.assertEqual(self.robot.orient,2)

    #make sure it's modded and shit

class TestRobotMove(unittest.TestCase):
    def setUp(self):
        self.game = Game([Robot("R", Location(1,1))])
        self.robot = self.game.board.robotList[0]
        self.robot.orient = 1

    def test_robotFacingEast_moveOne_movedOne(self):
        self.game.board.robotMove(self.robot,1)
        self.assertEqual(self.robot.loc,Location(2,1))

    def test_robotFacingEast_moveThree_movedThree(self):
        self.game.board.robotMove(self.robot,3)
        self.assertEqual(self.robot.loc,Location(4,1))

    def test_robotFacingEast_moveBackwardOne_movedBackwardOne(self):
        self.game.board.robotMove(self.robot,-1)
        self.assertEqual(self.robot.loc,Location(0,1))

    def test_robotFacingEastWallOnSameSquare_moveForwardOne_staysPut(self):
        self.game.board.grid[1][1][0].addProperty(Wall(1))
        self.game.board.robotMove(self.robot,1)
        self.assertEqual(self.robot.loc, Location(1,1))

    def test_robotFacingEastWall_moveBackwardOne_movesBack(self):
        self.game.board.grid[1][1][0].addProperty(Wall(1))
        self.game.board.robotMove(self.robot,-1)
        self.assertEqual(self.robot.loc, Location(0,1))

    def test_robotFacingWestWallOnNextSquare_moveForwardOne_staysPut(self):
        self.game.board.grid[1][2][0].addProperty(Wall(3))
        #print(self.game.board)
        self.game.board.robotMove(self.robot,1)
        self.assertEqual(self.robot.loc, Location(1,1))

    def test_robotFacingWestWallOnNextSquare_moveForwardThree_staysPut(self):
        self.game.board.grid[1][2][0].addProperty(Wall(3))
        #print(self.game.board)
        self.game.board.robotMove(self.robot,3)
        self.assertEqual(self.robot.loc, Location(1,1))

    def test_robotFacingEastWallOneSquareAway_moveOne_movesOne(self):
        self.game.board.grid[1][2][0].addProperty(Wall(1))
        self.game.board.robotMove(self.robot,1)
        self.assertEqual(self.robot.loc, Location(2,1))

    def test_robotFacingEastWallOneSquareAway_moveTwo_movesOne(self):
        self.game.board.grid[1][2][0].addProperty(Wall(1))
        self.game.board.robotMove(self.robot,2)
        self.assertEqual(self.robot.loc, Location(2,1))

    def test_robotFacingParallelWall_moveTwo_movesTwo(self):
        self.game.board.grid[1][2][0].addProperty(Wall(2))
        #print(self.game.board)
        self.game.board.robotMove(self.robot,2)
        self.assertEqual(self.robot.loc, Location(3,1))




class TestRobotPush(unittest.TestCase):
    def setUp(self):
        self.game = Game([Robot("R", Location(1,1)), Robot("C", Location(2,1)), Robot("E",Location(4,1))])
        self.robotR = self.game.board.robotList[0]
        self.robotR.orient = 1
        self.robotC = self.game.board.robotList[1]
        self.robotC.orient = 1
        self.robotE = self.game.board.robotList[2]
        self.robotE.orient = 1

    def test_twoConsecutiveRobots_pushOneRobotForwardIntoAir_robotPushed(self):
        self.game.board.robotMove(self.robotR,1)
        self.assertEqual(self.robotC.loc,Location(3,1))

    def test_twoConsecutiveRobots_pushOneRobotBackwardIntoAir_robotPushed(self):
        self.game.board.robotMove(self.robotC,-1)
        self.assertEqual(self.robotR.loc,Location(0,1))

    def test_threeConsecutiveRobots_pushTwoRobotsForwardIntoAir_robotsPushed(self):
        self.game.board.robotMove(self.robotR,2)
        self.assertEqual(self.robotC.loc,Location(4,1))
        self.assertEqual(self.robotE.loc,Location(5,1))

    def test_threeConsecutiveRobots_pushTwoRobotsBackwardIntoAir_robotsPushed(self):
        self.game.board.robotMove(self.robotE,-2)
        self.assertEqual(self.robotC.loc,Location(1,1))
        self.assertEqual(self.robotR.loc,Location(0,1))

    def test_twoConsecutiveRobots_pushRobotBackwardOffBoard_robotDead(self):
        self.game.board.robotMove(self.robotC,-2)
        self.assertTrue(self.robotR.dead)
        self.assertEqual(self.robotC.loc,Location(0,1))

    def test_twoConsecutiveRobotsWallBetween_pushRobot_robotsStayPut(self):
        self.game.board.grid[1][1][0].addProperty(Wall(1))
        self.game.board.robotMove(self.robotR,1)
        self.assertEqual(self.robotC.loc,Location(2,1))
        self.assertEqual(self.robotR.loc,Location(1,1))

    def test_twoConsecutiveRobotsWallAtEnd_pushRobot_robotsStayPut(self):
        self.game.board.grid[1][2][0].addProperty(Wall(1))
        self.game.board.robotMove(self.robotR,1)
        self.assertEqual(self.robotC.loc,Location(2,1))
        self.assertEqual(self.robotR.loc,Location(1,1))



class TestTouchSquare(unittest.TestCase):
    def setUp(self):
        self.spawnLoc = Location(0,0)
        self.flagLoc = Location(0,1)
        self.game = Game([Robot("R", self.spawnLoc)],flagLocList=[self.flagLoc])
        self.robot = self.game.board.robotList[0]
        #  self.grid[flag.y][flag.x][0].addProperty(Flag())


    def test_robot_touchFlag_spawnAndCheckpointUpdate(self):
        originalCheckpoint = self.robot.checkpoint
        self.game.board.robotMove(self.robot,1,2)
        self.game.touchSquare()
        self.assertEqual(originalCheckpoint+1,self.robot.checkpoint)
        self.assertEqual(self.robot.spawnLoc,self.flagLoc)



class TestHandleCards(unittest.TestCase):
    def setUp(self):
        self.game = Game([Robot("R", Location(1,1)), Robot("C", Location(2,1)))])
        self.robotR = self.game.board.robotList[0]
        self.robotR.orient = 1
        self.robotC = self.game.board.robotList[1]
        self.robotC.orient = 1
    def test_firstRobot_hasHigherPriority_movesFirst(self):
        pass
    def test_firstRobot_hasLowerPriority_movesSecond(self):
        pass

if __name__ == '__main__':
    unittest.main()