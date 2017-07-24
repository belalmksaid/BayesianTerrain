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

def modastar(a, b): # a modified version of A* used to find minimum cost to go from one cell to another with eucladian heuristic
    di = abs(b.i - a.i)  # determines the i direction we are moving in since there are no obstacles
    dj = abs(b.j - a.j)  # same for j

    #normalize step size
    if di != 0:
        di /= (b.i - a.i)

    if dj != 0:
        dj /= (b.j - a.j)

    ci = a.i
    cj = a.j

    cost = 0

    while not (ci == b.i and cj == b.j):
        cost += 1
        dx = 1323124
        dy = 1323124
        if di != 0:
            dx = (b.i - (ci + di)) **2 + (b.j - (cj)) **2 # no need to take the square root
        if dj != 0:
            dy = (b.i - (ci)) **2 + (b.j - (cj + dj)) **2
        
        if dy < dx:
            cj += dj
        else:
            ci += di
    
    return cost

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

    def cost(self, to): # calculate cost to get here, for question 4
        return modastar(self, to) * (1.0 - self.prob)


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

    def minCost(self, current):
        m = min([min(sub_belief, key=lambda x: x.cost(self.belief[current[0]][current[1]])) for sub_belief in self.belief], key=lambda x: x.prob)
        return [m.indices(), m.cost(self.belief[current[0]][current[1]])]
    
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
    
    def bayesianSearchQ4(self):
        searchCount = 0
        current = [self.size // 2, self.size // 2] # start in the middle of the map, // is integer division in Python > 3.0
        while(True):
            currentCost = 1.0 - self.belief[current[0]][current[1]].prob
            min = self.minCost(current)
            if currentCost < min[1]: # check if checking the current cell is lower cost than moving
                searchCount += currentCost
                if not self.hasTarget(*current): # if not target update probability
                    self.updateProb(*current)
                else:
                    return searchCount
            else: # move
                current = min[0]
                searchCount += min[1]