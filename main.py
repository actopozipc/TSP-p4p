import numpy as np
import matplotlib.pyplot as plt
import math
from TravelingSalesman import TS
from SimulatedAnnealing import SA

'''
Ziel: Alle Punkte in einem Koordinatensystem mit minimalen Kosten besuchen
Kosten = Metrik im 2d Raum
Monte-Carlo-Ansatz: Zufällige Pfade werden generiert
    ->Algorithmus ist in der Angabe
        ->Gleichungen 3 und 4 auf Seite 2
Neuer Pfad wird mit einer Wahrscheinlichkeit als bester Pfad übernommen
    ->Wahrscheinlichkeitsverteilung hängt von T und E ab
        ->T: Gegen 0 konvergierende Folge
            ->Gleichung 6
        ->E: Abhängig von der Effektivität des Pfads
        ->Auf Seite 2 gegeben in Gleichung 3

'''
def DrawTowns(towns, plt):
    for t in towns:
        plt.scatter(t.x, t.y)
def DrawPath(bestP):
    x = []
    y = []
    DrawTowns(towns, plt)
    bestP = np.append(bestP, bestP[0], axis=None)
    for t in bestP:
        x.append(sa.towns[t].x)
        y.append(sa.towns[t].y)

    plt.plot(x, y)
    fig.canvas.draw()
    plt.pause(0.05)
    plt.clf()
ts = TS();  # Klasse in der Methoden zum Erstellen der Städte sind
allEnergies = []
allPaths = []
avgVarianz = []
avgEnergies = []
temps = []
# Seed the numpy-RNG to 223
np.random.seed(223)
towns = ts.createNTowns(N=10);  # Erstelle N Städte
np.random.seed()  # unseed

# Zeichne x,y Koordinaten als Punkte
x = []
y = []
fig = plt.figure()
ax = fig.gca()
fig.show()
DrawTowns(towns, plt)
plt.ion
# Probier 100 mal neue update
cycles = 200
sa = SA(towns)
i = 0
# Super hohe Standardkosten. Falls Kosten von einem Pfad nach einem update geringer sind, speichere als minimalste
cost = 500
minimalCost = cost
bestPath = []
allTemps = []
while i < cycles:
    bestP = sa.update()
    
    if i == 0:
        allTemps = sa.allTemps
    i = i + 1
    print(i, " Zyklus durchlaufen von", cycles)

    sumE = 0
    sumVarianz = 0
    count = len(sa.allEnergies)
    for j in sa.allEnergies:
        sumE += j
    avgE = sumE / count
    avgEnergies.append(avgE)

    for k in sa.allEnergies:
        sumVarianz += math.pow(k, 2)
    avgVarianz.append(sumVarianz / count - avgE ** 2)

    '''for p in sa.allPaths:
        currentE = ts.sumOfEnergies(sa.towns, p)
        if currentE == minimalCost:
            bestPath = p'''
    if i == 0 or i % (cycles / 100) == 0:
        DrawPath(bestP)
        plt.title(ts.sumOfEnergies(sa.towns, bestP))


realLowestE = np.min(sa.allEnergies)  # minimalst generierter Weg -> Kann sein dass ein besserer Weg existiert,
    # dieser aber nicht wegen Wahrscheinlichkeit übernommen wurde
    # Find the path with the energy of the lowest energy
lowestE = ts.sumOfEnergies(sa.towns, sa.allPaths[0])
for p in sa.allPaths:
    currentE = ts.sumOfEnergies(sa.towns, p)
    if currentE == realLowestE:
        bestPath = p
        lowestE = ts.sumOfEnergies(sa.towns, p)
        minimalCost = currentE
    #Zeichne Striche in der Reihenfolge von Path

bestPath.append(bestPath[0])
for t in bestPath:
    x.append(sa.towns[t].x)
    y.append(sa.towns[t].y)

print("Anzahl der gefundenen Pfade:", len(sa.allPaths), "/", math.factorial(len(sa.towns)))  # Wie viele verschiedene
# Pfade generiert wurden von theoretisch möglichen
print("Best path generated:", realLowestE)
#print("Path selected:", minimalCost)
print("Path returned:", ts.sumOfEnergies(sa.towns, bestP))
print(bestPath)
plt.clf()
DrawTowns(towns, plt)
x = []
y = []
for t in bestPath:
    x.append(sa.towns[t].x)
    y.append(sa.towns[t].y)

plt.plot(x, y)
# Schreibe Koordinaten und Pfadkosten auf den Graphen drauf
for t in range(1, len(bestPath)):
    plt.text(sa.towns[bestPath[t - 1]].x - 0.01, sa.towns[bestPath[t - 1]].y - 0.01,
             ts.energyOfTwoTowns(sa.towns[bestPath[t - 1]], sa.towns[bestPath[t]]), fontsize=8)
    plt.text(sa.towns[bestPath[t - 1]].x + 0.01, sa.towns[bestPath[t - 1]].y + 0.01,
             str((round(x[t - 1], 2), round(y[t - 1], 2))), fontsize=8)
plt.title(ts.sumOfEnergies(sa.towns, bestPath))
plt.figure()
plt.show()
for i in range(len(allTemps)):
    allTemps[i] = 1/allTemps[i]
plt.plot(avgVarianz, allTemps)
plt.show()
'''sumE = 0
sumVarianz = 0

count = len(sa.allEnergies)
for i in sa.allEnergies:
    sumE += i

avgE = sumE/count

for i in sa.allEnergies:
    sumVarianz += math.pow(i, 2)

varianz = sumVarianz/count - avgE**2

print("avg Energie:", avgE)
print("varianz:", varianz)'''



#print(avgVarianz)
#print(avgEnergies)
#print(sa.allTemps)
