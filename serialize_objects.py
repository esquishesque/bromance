import dill
import grid

def readGridFromFile(name):
    with open (name, 'rb') as f:
        grid = dill.load(f)
    return grid

def writeGridToFile(grid):
    with open('conveyors_testing_factory.pik', 'wb') as f:
        dill.dump(grid, f)



if __name__ == "__main__":
    grid = grid.generateGrid()
    writeGridToFile(grid)

