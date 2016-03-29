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
        self.game.board.grid[1][1][0].addComponent(Wall(1))
        self.game.board.robotMove(self.robot,1)
        self.assertEqual(self.robot.loc, Location(1,1))

    def test_robotFacingEastWall_moveBackwardOne_movesBack(self):
        self.game.board.grid[1][1][0].addComponent(Wall(1))
        self.game.board.robotMove(self.robot,-1)
        self.assertEqual(self.robot.loc, Location(0,1))

    def test_robotFacingWestWallOnNextSquare_moveForwardOne_staysPut(self):
        self.game.board.grid[1][2][0].addComponent(Wall(3))
        #print(self.game.board)
        self.game.board.robotMove(self.robot,1)
        self.assertEqual(self.robot.loc, Location(1,1))

    def test_robotFacingWestWallOnNextSquare_moveForwardThree_staysPut(self):
        self.game.board.grid[1][2][0].addComponent(Wall(3))
        #print(self.game.board)
        self.game.board.robotMove(self.robot,3)
        self.assertEqual(self.robot.loc, Location(1,1))

    def test_robotFacingEastWallOneSquareAway_moveOne_movesOne(self):
        self.game.board.grid[1][2][0].addComponent(Wall(1))
        self.game.board.robotMove(self.robot,1)
        self.assertEqual(self.robot.loc, Location(2,1))

    def test_robotFacingEastWallOneSquareAway_moveTwo_movesOne(self):
        self.game.board.grid[1][2][0].addComponent(Wall(1))
        self.game.board.robotMove(self.robot,2)
        self.assertEqual(self.robot.loc, Location(2,1))

    def test_robotFacingParallelWall_moveTwo_movesTwo(self):
        self.game.board.grid[1][2][0].addComponent(Wall(2))
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
        self.game.board.grid[1][1][0].addComponent(Wall(1))
        self.game.board.robotMove(self.robotR,1)
        self.assertEqual(self.robotC.loc,Location(2,1))
        self.assertEqual(self.robotR.loc,Location(1,1))

    def test_twoConsecutiveRobotsWallAtEnd_pushRobot_robotsStayPut(self):
        self.game.board.grid[1][2][0].addComponent(Wall(1))
        self.game.board.robotMove(self.robotR,1)
        self.assertEqual(self.robotC.loc,Location(2,1))
        self.assertEqual(self.robotR.loc,Location(1,1))

class TestTouchSquare(unittest.TestCase):
    def setUp(self):
        self.spawnLoc = Location(0,0)
        self.flagOne = Location(0,1)
        self.flagTwo = Location(2,2)
        self.game = Game([Robot("R", self.spawnLoc)],flagLocList=[self.flagOne,self.flagTwo])
        self.robotR = self.game.board.robotList[0]
        #  self.grid[flag.y][flag.x][0].addComponent(Flag())

    def test_robot_touchFlagOne_spawnAndCheckpointUpdate(self):
        originalCheckpoint = self.robotR.checkpoint
        self.robotR.loc = Location(0,1)
        self.game.touchSquare()
        self.assertEqual(originalCheckpoint+1,self.robotR.checkpoint)
        self.assertEqual(self.robotR.spawnLoc,self.flagOne)
    def test_robot_touchFlagTwo_spawnButNotCheckpointUpdate(self):
        originalCheckpoint = self.robotR.checkpoint
        self.robotR.loc = Location(2,2)
        self.game.touchSquare()
        self.assertEqual(originalCheckpoint,self.robotR.checkpoint)
        self.assertEqual(self.robotR.spawnLoc,self.flagTwo)

class TestHandleCards(unittest.TestCase):
    def setUp(self):
        self.game = Game([Robot("R", Location(2,1)), Robot("C", Location(1,1))])
        self.robotR = self.game.board.robotList[0]
        self.robotR.orient = 1
        self.robotC = self.game.board.robotList[1]
        self.robotC.orient = 1
    def test_firstRobot_hasHigherPriority_movesFirst(self):
        self.robotR.instructions=[MoveCard(1,600)]
        self.robotC.instructions=[MoveCard(1,400)]
        self.game.executePhase(0)
        #print(self.robotR.loc)
        self.assertEqual(self.robotR.loc,Location(3,1))
    def test_firstRobot_hasLowerPriority_movesSecond(self):
        self.robotR.instructions=[MoveCard(1,400)]
        self.robotC.instructions=[MoveCard(1,600)]
        self.game.executePhase(0)
        #print(self.robotR.loc)
        self.assertEqual(self.robotR.loc,Location(4,1))

class TestFireLasers(unittest.TestCase):
    def setUp(self):
        self.game = Game([Robot("R", Location(0,0),2),Robot("C", Location(2,0),0),Robot("E",Location(4,0),3)],laserPosList=[],wallPosList=[])
        self.robotR = self.game.board.robotList[0]
        self.robotC = self.game.board.robotList[1]
        self.robotE = self.game.board.robotList[2]
    # def test_robotOnEmptyBoard_shootsOffBoard_takesNoDamage(self):
    #     self.game.board.fireLasers()
    #     self.assertEqual(self.robotR.damage,0)
    def test_threeRobotsInARow_thirdShootsWest_onlySecondTakesDamage(self):
        self.game.board.fireLasers()
        self.assertEqual(self.robotR.damage,0)
        self.assertEqual(self.robotE.damage,0)
        self.assertEqual(self.robotC.damage,1)
    def test_threeRobotsInARowAllFacingWest_allShootWest_westmostAndMiddleTakeDamage(self):
        self.robotR.orient = 3
        self.robotC.orient = 3
        self.robotE.orient = 3
        self.game.board.fireLasers()
        self.assertEqual(self.robotR.damage,1)
        self.assertEqual(self.robotC.damage,1)
        self.assertEqual(self.robotE.damage,0)
    def test_robotFacingWestAtRobot_westWallOnFiringSquareIntervenes_noDamageTaken(self):
        self.game.board.grid[0][4][0].addComponent(Wall(3))
        self.game.board.fireLasers()
        self.assertEqual(self.robotC.damage,0)
    def test_robotFacingWestAtRobot_eastWallOnInterveningSquareIntervenes_noDamageTaken(self):
        self.game.board.grid[0][3][0].addComponent(Wall(1))
        self.game.board.fireLasers()
        self.assertEqual(self.robotC.damage,0)
    def test_robotFacingWestAtRobot_westWallOnInterveningSquareIntervenes_noDamageTaken(self):
        self.game.board.grid[0][3][0].addComponent(Wall(3))
        self.game.board.fireLasers()
        self.assertEqual(self.robotC.damage,0)
    def test_robotFacingWestAtRobot_eastWallOnTargetSquareIntervenes_noDamageTaken(self):
        self.game.board.grid[0][2][0].addComponent(Wall(1))
        self.game.board.fireLasers()
        self.assertEqual(self.robotC.damage,0)
    def test_robotHasLasersOnBothSidesOnOwnSquare_lasersFire_twoDamageTaken(self):
        self.game.board.grid[0][0][0].addComponent(Laser(1))
        self.game.board.laserPosList.append(Position(Location(0,0),1))
        self.game.board.grid[0][0][0].addComponent(Laser(3))
        self.game.board.laserPosList.append(Position(Location(0,0),3))
        self.game.board.fireLasers()
        self.assertEqual(self.robotR.damage,2)
    def test_laserFacingRobotFromAfar_lasersFire_oneDamageTaken(self):
        self.game.board.grid[2][0][0].addComponent(Laser(2))
        self.game.board.laserPosList.append(Position(Location(0,2),2))
        self.game.board.fireLasers()
        self.assertEqual(self.robotR.damage,1)
    def test_robotHasRobotsFacingFromTwoSides_lasersFire_twoDamageTaken(self):
        self.robotR.orient = 1
        self.game.board.fireLasers()
        self.assertEqual(self.robotC.damage,2)
    def test_robotHasRobotAndWallLaserFacingOnEitherSide_lasersFire_twoDamageTaken(self):
        self.game.board.grid[0][2][0].addComponent(Laser(3))
        self.game.board.laserPosList.append(Position(Location(2,0),3))
        self.game.board.fireLasers()
        print(self.game.board)
        self.assertEqual(self.robotC.damage,2)

class TestDamageRobot(unittest.TestCase):
    def setUp(self):
        self.game = Game([Robot("R", Location(2,1))])
        self.robotR = self.game.board.robotList[0]
    def test_robotWithNoDamage_takesDefaultDamage_robotHasOneDamageAndStillAlive(self):
        self.game.board.damageRobot(self.robotR)
        self.assertEqual(self.robotR.damage,1)
        self.assertFalse(self.robotR.dead)
    def test_robotWithNoDamage_takesOneDamage_robotHasOneDamageAndStillAlive(self):
        self.game.board.damageRobot(self.robotR,1)
        self.assertEqual(self.robotR.damage,1)
        self.assertFalse(self.robotR.dead)
    def test_robotWithNoDamage_takesThreeDamage_robotHasThreeDamageAndStillAlive(self):
        self.game.board.damageRobot(self.robotR,3)
        self.assertEqual(self.robotR.damage,3)
        self.assertFalse(self.robotR.dead)
    def test_robotWithNoDamage_takesHandSizeDamage_robotIsDead(self):
        self.game.board.damageRobot(self.robotR,self.game.board.handSize)
        self.assertTrue(self.robotR.dead)
    def test_robotWithThreeDamage_takesDefaultDamage_robotHasFourDamageAndStillAlive(self):
        self.robotR.damage = 3
        self.game.board.damageRobot(self.robotR)
        self.assertEqual(self.robotR.damage,4)
        self.assertFalse(self.robotR.dead)
    def test_robotWithThreeDamage_takesHandSizeDamage_robotIsDead(self):
        self.robotR.damage = 3
        self.game.board.damageRobot(self.robotR,self.game.board.handSize)
        self.assertTrue(self.robotR.dead)


class TestKillRobot(unittest.TestCase):
    def setUp(self):
        self.game = Game([Robot("R", Location(2,1))])
        self.robotR = self.game.board.robotList[0]
    def test_aliveRobot_killRobot_robotDeadInRobotHellWithTwoDamage(self):
        self.game.board.killRobot(self.robotR)
        self.assertEqual(self.robotR.loc,(None,None))
        self.assertEqual(self.robotR.damage,2)
        self.assertTrue(self.robotR.dead)

class TestSelectInstructions(unittest.TestCase):
    def setUp(self):


if __name__ == '__main__':
    unittest.main()