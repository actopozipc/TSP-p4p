from TravelingSalesman import TS
import math
import numpy as np
import random


class SA:  # SimulatedAnnealing
    def __init__(self, towns, startTemp=1, cycles=100):
        self.startTemp = startTemp
        self.currentTemp = startTemp
        self.stopTemp = 0
        self.currentEnergy = 0
        self.bestEnergy = self.currentEnergy
        self.towns = towns
        self.path = np.random.permutation(len(towns))
        #self.path = np.array([2, 6, 9, 8, 14, 20, 5, 13, 19, 12, 18, 11, 15, 16, 10, 17, 1, 4, 3, 0, 7, 21])
        self.currentPath = np.copy(self.path)
        self.allPaths = []
        self.allEnergies = []
        self.allTemps = []
        self.bestPath = self.path  # bester Pfad ist der erste Pfad
        self.cycles = cycles  # Wie oft Algo wiederholt werden soll
        self.count = math.factorial(len(self.towns))

    def reduceTemperature(self, k, q=1):
        return self.startTemp * k ** (-q)  # Gleichung 6

    # wird nicht verwendet
    '''def Boltzmann(self, towns, T, paths, currentEnergy):
        #Boltzmann-Verteilung
        #-> Gibt die Wahrscheinlichkeit an, ob ein neuer Pfad akzeptiert wird oder nicht
        #-> Sollte von Temperatur (=gegen 0 konvergierende Folge) und Energie abhängen
        #Bin mir nicht 100% sicher dass das richtig gecoded ist

        ts = TS();
        z = np.longdouble(0)
        for i in range(len(self.allTemps)):
            z = z + math.exp(-self.allEnergies[i] / self.allTemps[i])
        if z == 0:
            return 1
        return 1 / z * math.exp(-currentEnergy / T)'''

    def generateNewConfiguration(self, S):
        '''
        Der Zufalls-Algorithmus von der Angabe
        Siehe Gleichung 3,4 auf Seite 2
        Bin mir nicht 100% sicher dass das richtig gecoded ist
        '''
        # Select two Cities C_a and C_b at random with a<b
        # 1 and len-1 so a+1 and a-1 wont be out of range
        a = random.randrange(0, len(S), 1)
        b = random.randrange(0, len(S), 1)
        path = np.copy(S)

        '''amin = a - 1
        bmax = b + 1
        ts = TS()
        if a == 0:
            amin = len(S) - 1
        if b == len(S) - 1:
            bmax = 0

        The corresponding energy difference is rather simple to obtain. For a != 1 and b ! = N ,one finds
        energyDiffernece = ts.energyOfTwoTowns(self.towns[amin], self.towns[b]) + ts.energyOfTwoTowns(
            self.towns[a], self.towns[bmax]) - ts.energyOfTwoTowns(self.towns[amin],
                                                                   self.towns[a]) - ts.energyOfTwoTowns(self.towns[b],
                                                                                                        self.towns[
                                                                                                            bmax])'''

        if a < b:
            tmp = path[a]
            path[a] = path[b]
            path[b] = tmp
        else:
            tmp = a
            a = b
            b = tmp
            tmp = path[a]
            path[a] = path[b]
            path[b] = tmp

        # reverse the order of the towns that are in-between
        while b > a:
            tmp = path[a + 1]
            path[a + 1] = path[b]
            path[b] = tmp
            b = b - 1
        return path

    def update(self):
        '''
        Updatet Energie und Temperatur und Pfad 
        Wenn die neue Energiedifferenz <0 ist, wird sie mit Wahrscheinlichkeit als neue beste Energie genommen
        '''
        ts = TS()
        # Aktuelle Energie
        self.currentEnergy = ts.sumOfEnergies(self.towns, self.path)

        # Bisher besten Zustand speichern
        bestPath = self.path
        for i in range(1, self.cycles, 1):
            if len(self.allPaths) == self.count:  # Falls schon alle Kombinationen generiert, hör auf zu suchen
                return bestPath

            self.path = self.generateNewConfiguration(self.currentPath)
            newEnergy = ts.sumOfEnergies(self.towns, self.path)  # Energie für neuen Pfad
            self.allEnergies.append(newEnergy)  # speichere neue Energie
            self.allPaths.append(self.path.tolist()[:])  # speichere neuen Pfad
            self.allTemps.append(self.currentTemp)  # speichere neue Temperatur

            # Falls neue Energie weniger ist, setze beste Energie und besten Pfad
            if newEnergy < self.bestEnergy:
                self.bestEnergy = newEnergy
                bestPath = self.path
                self.bestPath = self.path
                self.currentPath = self.path
            elif self.acceptanceProbability(newEnergy, self):
                self.bestEnergy = newEnergy
                bestPath = self.path
                self.bestPath = self.path
                self.currentPath = self.path
            self.currentTemp = self.reduceTemperature(i)

        return bestPath

    def acceptanceProbability(self, newEnergy, sa):
        deltaE = newEnergy - sa.currentEnergy  # Energiedifferenz
        r = np.random.rand()
        probability = math.exp(
            -deltaE / sa.currentTemp)
        return r < probability
