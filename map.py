import random
import matplotlib.pyplot as plt

FLAT = 0
HILL = 1
FOREST = 2
MAZE = 3

Names = {
    FLAT: "Flat",
    HILL: "Hilly",
    FOREST: "Forested",
    MAZE: "Maze of Caves"

}

class Map:
    def __init__(self):
        self.data = [[random.randrange(0, 4) for i in range(50)] for j in range(50)] #Initialized a map with a terrain

    def display(self):
        cmap = plt.get_cmap('jet', 4)
        cmap.set_under('gray')
        mat = plt.matshow(self.data,cmap=cmap,vmin =-.5, vmax = 3.5)
        cbar = plt.colorbar(ticks=range(0, 4))
        cbar.ax.set_yticklabels(list(Names.values()))
        plt.show()