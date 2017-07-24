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
Prob = { # Prob of not there
    FLAT: 0.2,
    HILL: 0.4,
    FOREST: 0.6,
    MAZE: 0.9,
}

class Cell:
    def __init__(self, i, j, type, prob):
        self.visits = 0
        self.prob = prob
        self.i = i
        self.j = j
        self.type = type

    def indices(self):
        return [self.i, self.j]

    def probFind(self):
        return self.prob * (1.0 - Prob[self.type])

class Map:
    def __init__(self, size):
        self.prob = 1 / (size **2) # Base probability that a cell has the target
        self.size = size
        self.resetMap()
        self.resetBelief()
        self.resetTarget()

    def resetBelief(self):
        self.belief = [[Cell(j, i, self.data[j][i], self.prob) for i in range(self.size)] for j in range(self.size)] # Belief map
    
    def resetMap(self):
        self.data = [[random.randrange(0, 4) for i in range(self.size)] for j in range(self.size)] # Initialized a map with a terrain
    
    def resetTarget(self):
        self.target = [random.randrange(0, self.size), random.randrange(0, self.size)]

    def display(self):
        cmap = plt.get_cmap('GnBu', 4)
        cmap.set_under('gray')
        mat = plt.matshow(self.data,cmap=cmap,vmin =-.5, vmax = 3.5)
        cbar = plt.colorbar(ticks=range(0, 4))
        cbar.ax.set_yticklabels(list(Names.values()))
        plt.plot(self.target[1], self.target[0], 'r.', label='Target', ms=4)
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.1))
        plt.show()

    def displayHeatMap(self):
        heatmap = [[self.belief[j][i].prob for i in range(self.size)] for j in range(self.size)]
        #print(len(heatmap))
        plt.imshow(heatmap, cmap='hot', interpolation='nearest')
        plt.show()

    def hasTarget(self, i, j):
        if self.target[0] == i and self.target[1] == j:
            if random.random() > Prob[self.data[self.target[0]][self.target[1]]]:
                return True
            return False
        else:
            return False

    def maxProb(self): # Find biggest probability in the map
        return max([max(sub_belief, key=lambda x: x.prob) for sub_belief in self.belief], key=lambda x: x.prob).indices()

    def maxFind(self):
        return max([max(sub_belief, key=lambda x: x.probFind()) for sub_belief in self.belief], key=lambda x: x.prob).indices()
    
    def updateProb(self, x, y):
        q = 1 - Prob[self.data[x][y]]
        p = self.belief[x][y].prob
        self.belief[x][y].prob = p * (1.0 - q) / (1.0 - p * q)
        p = self.belief[x][y].prob
        for j in range(0, self.size):
            for i in range(0, self.size):
                if x != i or y != j:
                    self.belief[i][j].prob = (self.belief[i][j].prob / (1.0 - p * q))

    def bayesianSearchRule1(self):
        searchCount = 0
        current = self.maxProb() # Get index of the highest probability
        while(True):
            searchCount += 1
            if not self.hasTarget(*current):
                self.updateProb(*current)
                current = self.maxProb()
            else:
                return searchCount


    def bayesianSearchRule2(self):
        searchCount = 0
        current = self.maxFind() # Get index of the highest probability
        while(True):
            searchCount += 1
            if not self.hasTarget(*current):
                self.updateProb(*current)
                current = self.maxFind()
            else:
                return searchCount
