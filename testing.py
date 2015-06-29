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


if __name__ == '__main__':
    unittest.main()