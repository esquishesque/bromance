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