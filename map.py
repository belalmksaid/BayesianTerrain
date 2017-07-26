import random
import matplotlib.pyplot as plt
import math

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
CONSTANT = 1

def manhattan(a, b): # returns manhattan ditance between two cells
    di = abs(b.i - a.i)  # determines the i direction we are moving in since there are no obstacles
    dj = abs(b.j - a.j)  # same for j
    return di + dj

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
        if to.i == self.i and to.j == self.j:
            return 1283712047 # so it wouldn't return itself
        return (manhattan(self, to) + 1) * (1.0 / (self.probFind() * CONSTANT))


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
        heatmap = [[self.belief[j][i].visits for i in range(self.size)] for j in range(self.size)]
        #print(len(heatmap))
        plt.pcolor(heatmap, cmap='OrRd', vmin=0, vmax=max([max(visits) for visits in heatmap]))
        plt.title('Heat Map of Most Visited Cells')
        # set the limits of the plot to the limits of the data
        plt.colorbar()
        plt.show()

    def hasTarget(self, i, j):
        if self.target[0] == i and self.target[1] == j:
            if random.random() > Prob[self.data[self.target[0]][self.target[1]]]:
                return True
            return False
        else:
            return False

    def maxProb(self): # Find the cell with highest probability of having target in the map
        return max([max(sub_belief, key=lambda x: x.prob) for sub_belief in self.belief], key=lambda x: x.prob).indices()

    def maxFind(self): # Find the cell with high probably of finding target there
        return max([max(sub_belief, key=lambda x: x.probFind()) for sub_belief in self.belief], key=lambda x: x.probFind()).indices()

    def minCost(self, current): # Find cell with the lowest possible cost using D/p formula
        m = min([min(sub_belief, key=lambda x: x.cost(self.belief[current[0]][current[1]])) for sub_belief in self.belief], key=lambda x: x.cost(self.belief[current[0]][current[1]]))
        return [m.indices(), m.cost(self.belief[current[0]][current[1]]), manhattan(m, self.belief[current[0]][current[1]])]
    
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
        actionCount = 0
        visits = 0
        current = self.maxProb() # Get index of the highest probability   
        while(True):
            visits += 1
            actionCount += 1
            self.belief[current[0]][current[1]].visits += 1     
            if not self.hasTarget(*current):
                self.updateProb(*current)
                newcell = self.maxFind()
                actionCount += manhattan(self.belief[current[0]][current[1]], self.belief[newcell[0]][newcell[1]])
                current = newcell
            else:
                return [actionCount, visits]


    def bayesianSearchRule2(self):
        actionCount = 0 #For question 4
        visits = 0
        current = self.maxFind() # Get index of the highest probability
        while(True):
            visits += 1
            actionCount += 1
            self.belief[current[0]][current[1]].visits += 1       
            if not self.hasTarget(*current):
                self.updateProb(*current)
                newcell = self.maxFind()
                actionCount += manhattan(self.belief[current[0]][current[1]], self.belief[newcell[0]][newcell[1]])
                current = newcell
            else:
                return [actionCount, visits]
    

    def bayesianSearchQ4(self):
        actionCount= 0
        visits = 0
        current = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)] # start at a random spot
        while(True):
            currentCost = 1.0 / self.belief[current[0]][current[1]].probFind()
            min = self.minCost(current)
            if currentCost <= min[1]: # check if checking the current cell is lower cost than moving
                actionCount += 1
                visits += 1
                self.belief[min[0][0]][min[0][1]].visits += 1 # incerement visisted cell, used for heat maps          
                if not self.hasTarget(*current): # if not target, update probabilities and beliefs
                    self.updateProb(*current)
                else:
                    return [actionCount, visits]
            else: # move
                current = min[0]
                actionCount+= min[2]