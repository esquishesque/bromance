import dill

def readGridFromFile(name):
    with open (name, 'rb') as f:
        grid = dill.load(f)
    return grid

def writeGridToFile(grid):
    with open('factory.pik', 'wb') as f:
        dill.dump(grid, f)