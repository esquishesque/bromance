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


if __name__ == '__main__':
    unittest.main()