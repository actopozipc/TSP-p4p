from Town import town
import math
import numpy as np


class TS:
    '''
    Hilfsklasse zum Generieren von Städten und zum Berechnen des Abstandes
    '''

    def __init__(self):
        pass

    def createNTowns(self, N=22):
        townsCoordinates = np.random.rand(N, 2);  # create towns
        towns = []
        for i in townsCoordinates:
            towns.append(town(i[0], i[1]))
        return towns;

    def energyOfTwoTowns(self, a, b):
        x_diff = a.x - b.x;
        y_diff = a.y - b.y;
        return math.sqrt(x_diff ** 2 + y_diff ** 2);

    oldpath = []
    oldsum = 0;

    def SumOfEnergies(self, towns, path):
        sum = 0;
        for i in range(0, len(towns) - 1, 1):
            sum += self.energyOfTwoTowns(towns[path[i + 1]], towns[path[i]])
        oldpath = path;
        oldsum = sum;
        if path == oldpath and oldsum != sum:
            print("Fuck")
        return sum;
