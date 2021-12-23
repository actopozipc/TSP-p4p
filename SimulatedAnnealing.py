from TravelingSalesman import TS
import math
import numpy as np
import random


class SA:  # SimulatedAnnealing
    def __init__(self, towns, startTemp=0.8, cycles=100):
        self.startTemp = startTemp
        self.currentTemp = startTemp
        self.stopTemp = 0
        self.currentEnergy = 0
        self.bestEnergy = self.currentEnergy
        self.towns = towns
        self.path = np.random.permutation(len(towns))
        self.currentPath = np.copy(self.path)
        self.allPaths = []
        self.allEnergies = []
        self.allTemps = []
        # Zufälliger Pfad wird als Start generiert
        #for i in range(len(towns)):
        #    self.path.append(i)
        #self.RandomizeList(self.path)
        self.bestPath = self.path  # bester Pfad ist der erste Pfad
        self.cycles = cycles  # Wie oft Algo wiederholt werden soll
        pass

    def ReduceTemperature(self, k, q=1):
        return self.startTemp * k ** (-q) #Gleichung 6

    def Boltzmann(self, towns, T, paths, currentEnergy):
        '''
        Boltzmann-Verteilung
        -> Gibt die Wahrscheinlichkeit an, ob ein neuer Pfad akzeptiert wird oder nicht
        -> Sollte von Temperatur (=gegen 0 konvergierende Folge) und Energie abhängen
        Bin mir nicht 100% sicher dass das richtig gecoded ist
        '''
        ts = TS();
        z = np.longdouble(0)
        for i in range(len(self.allTemps)):
            z = z + math.exp(-self.allEnergies[i] / self.allTemps[i])
        if z == 0:
            return 1
        return 1 / z * math.exp(-currentEnergy / T)

    def UpdatePath(self):
        '''
        Updadet die aktuelle Path Property mit einem neuen Random Path
        '''
        self.path = self.GenerateNewConfiguration(self.currentPath)
        # self.path = self.GenerateNewConfiguration(self.path);
        return self.path

    def RandomizeList(self, S):
        random.shuffle(S)
        return S

    def GenerateNewConfiguration(self, S):
        '''
        Der Zufalls-Algorithmus von der Angabe
        Siehe Gleichung 3,4 auf Seite 2
        Bin mir nicht 100% sicher dass das richtig gecoded ist
        '''
        # Select two Cities C_a and C_b at random with a<b
        # 1 and len-1 so a+1 and a-1 wont be out of range
        a = random.randrange(0, len(S), 1)
        b = random.randrange(0, len(S), 1)
        amin = a - 1
        bmax = b + 1
        path = np.copy(S)
        ts = TS()
        if a == 0:
            amin = len(S) - 1
        if b == len(S) - 1:
            bmax = 0

        # The corresponding energy difference is rather simple to obtain. For a != 1 and b ! = N ,one finds
        #energyDiffernece = ts.energyOfTwoTowns(self.towns[amin], self.towns[b]) + ts.energyOfTwoTowns(
        #    self.towns[a], self.towns[bmax]) - ts.energyOfTwoTowns(self.towns[amin],
        #                                                           self.towns[a]) - ts.energyOfTwoTowns(self.towns[b],
        #                                                                                                self.towns[
        #                                                                                                    bmax])
        # Exchange their positions in the path+
        #if energyDiffernece>0:
        if (a < b):  # b<a unterschied? hilfe
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
            # and reverse the order of the towns that are in-between
        while b > a:
            tmp = path[a + 1]
            path[a + 1] = path[b]
            path[b] = tmp
            b = b - 1
        return path

    def Update(self):
        '''
        Updatet Energie und Temperatur und Pfad 
        Wenn die neue Energiedifferenz <0 ist, wird sie mit Wahrscheinlichkeit als neue beste Energie genommen
        '''
        ts = TS()
        # Aktuelle Energie
        self.currentEnergy = ts.sumOfEnergies(self.towns, self.path)
        # Bisher besten Zustand speichern
        bestPath = self.path
        bestEnergy = self.currentEnergy
        self.currentTemp = self.startTemp
        for i in range(1, self.cycles, 1):
            if len(self.allPaths) == math.factorial(
                    len(self.towns)):  # Falls schon alle Kombinationen generiert, hör auf zu suchen
                return bestPath;
            oldConfiguration = self.path;  # speicher bisherigen Pfad
            newConfiguration = self.UpdatePath();  # update Pfad
            newEnergy = ts.sumOfEnergies(self.towns, newConfiguration)  # Energie für neuen Pfad
            b = True
            #if False not in np.isin(newConfiguration, self.allPaths):  # falls neuer Pfad noch nicht generiert wurde
            #for h in self.allPaths:
             #   if newConfiguration.all() == h.all():
              #      b = False
            #if b:
            self.allEnergies.append(newEnergy)  # speichere neue Energie
            self.allPaths.append(newConfiguration.tolist()[:])  # speichere neuen Pfad
            self.allTemps.append(self.currentTemp)  # speichere neue Temperatur
            # Falls neue Energie weniger ist, setze beste Energie und besten Pfad
            if newEnergy < bestEnergy:  # falls neue energie besser ist, speichern
                self.bestEnergy = newEnergy
                bestPath = newConfiguration
                self.bestPath = newConfiguration
                self.currentPath = self.path
            elif self.AcceptanceProbability(newEnergy, self, newConfiguration,
                                            oldConfiguration):  # falls wahrscheinlichkeit zutrifft, übernimm schlechtere energie
                self.bestEnergy = newEnergy
                bestPath = newConfiguration
                self.bestPath = newConfiguration
                self.currentPath = self.path
            self.currentTemp = self.ReduceTemperature(i)  # aktualisiere temperatur -> ist das so gedacht? I guess

        # self.currentEnergy = bestEnergy;
        # self.path = bestPath;
        return bestPath;

    def AcceptanceProbability(self, newEnergy, sa, newConfiguration, oldConfiguration):
        deltaE = newEnergy - sa.currentEnergy  # Energiedifferenz
        probability = math.exp(
            -deltaE / sa.currentTemp)  ##self.Boltzmann(self.towns, self.currentTemp, self.path, deltaE);
        acceptanceProbability = sa.Boltzmann(sa.towns, sa.currentTemp, newConfiguration, newEnergy) / sa.Boltzmann(
            sa.towns, sa.currentTemp, oldConfiguration, sa.currentEnergy)
        return probability > 1 or probability > acceptanceProbability
