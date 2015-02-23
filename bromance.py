from game import *

if __name__ == "__main__":
    createdRobots = []
    #later the list will be populated by something else but for now it's just a single robot
    createdRobots.append(Robot("R", Location(0,0))) #the order of this list should never change (deprecated fact?)
    createdRobots.append(Robot("C", Location(0,4)))
    #createdRobots.append(Robot("E", Location(0,8)))
    game = Game(createdRobots)
    game.play()
