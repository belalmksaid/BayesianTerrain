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
    MAZE: "Maze of Caves",

}
Prob = {
    FLAT: 0.2,
    HILL: 0.4,
    FOREST: 0.6,
    MAZE: 0.9,
}

class Map:
    def __init__(self, size):
        self.data = [[random.randrange(0, 4) for i in range(size)] for j in range(size)] #Initialized a map with a terrain
        self.target = [random.randrange(0, size), random.randrange(0, size)]
        self.prob = 1 / (size **2)

    def display(self):
        cmap = plt.get_cmap('GnBu', 4)
        cmap.set_under('gray')
        mat = plt.matshow(self.data,cmap=cmap,vmin =-.5, vmax = 3.5)
        cbar = plt.colorbar(ticks=range(0, 4))
        cbar.ax.set_yticklabels(list(Names.values()))
        plt.plot(self.target[0], self.target[1], 'r.', label='Target', ms=4)
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.1))
        plt.show()

    def hasTarget(self, i, j):
        if self.target[0] == i and self.target[1] == j:
            return True
        else:
            return False