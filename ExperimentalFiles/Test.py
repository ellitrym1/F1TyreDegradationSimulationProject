import math
import random
import time
from matplotlib import pyplot as plt
from simanneal import Annealer


class Tyre:

    def __init__(self, initialGrip, initialDeg, switchPoint, switchDeg):
        self.initialGrip = initialGrip
        self.initialDeg = initialDeg
        self.switchPoint = switchPoint
        self.switchDeg = switchDeg
        self.currentGrip = initialGrip

        if self.initialGrip == 2.0:
            self.tyreCompound = "soft"
        elif self.initialGrip == 1.6:
            self.tyreCompound = "medium"
        else:
            self.tyreCompound = "hard"

        super().__init__()

    def addLap(self, fuelEffect, gripLossFactor):
        print("Start: ", self.currentGrip)
        print("Fuel effect: ", fuelEffect)

        if self.currentGrip > self.switchPoint:
            self.currentGrip = (self.currentGrip - (self.initialDeg * gripLossFactor * fuelEffect))
        elif self.currentGrip > 0.2:
            self.currentGrip = (self.currentGrip - (self.switchDeg * gripLossFactor * fuelEffect))
        else:
            self.currentGrip = 0.0

        print("End: ", self.currentGrip)

    def __eq__(self, other):
        returnVal = False
        if self.initialGrip == other.initialGrip:
            print("Initial grips are the same!")
            returnVal = True
        if self.initialDeg == other.initialDeg:
            print("Initial grips are the same!")
            returnVal = True
        if self.switchPoint == other.switchPoint:
            print("Initial grips are the same!")
            returnVal = True
        if self.switchDeg == other.switchDeg:
            print("Initial grips are the same!")
            returnVal = True

        return returnVal

    def calculateLapTime(self, fuel, lapTimeFactor, lapBaseTime):
        lapBaseTime = lapBaseTime * lapTimeFactor
        lapTime = lapBaseTime
        if self.currentGrip >= 0.2:
            lapTime = lapTime - self.currentGrip
        else:
            lapTime = lapTime + 2.0
        if fuel == 105.0:
            lapTime = lapTime - 0.0
        elif fuel == 0.0:
            lapTime = lapTime + 2.0
        else:
            lapTime = lapTime - (2.0*((105-fuel)/105))

        return lapTime

    def reset(self):
        self.currentGrip = self.initialGrip

    def getTyreCompound(self):
        return self.tyreCompound


class Car:

    def __init__(self, initialTyre, numberOfPitstops, pitStops, pitTyres, gripLossFactor, lapTimeFactor):

        self.initialTyre = initialTyre
        self.numberOfPitstops = numberOfPitstops
        self.pitStops = pitStops
        self.pitTyres = pitTyres
        self.gripLossFactor = gripLossFactor
        self.lapTimeFactor = lapTimeFactor
        self.maxLapsForRace = 70
        self.currentTyre = None
        self.currentLap = 0
        self.startingFuel = 105.0
        self.currentFuel = self.startingFuel
        self.currentLapTime = 0.0
        self.fuelEffect = 0.0
        self.pitStopCounter = 0
        self.totalRaceTime = 5.0
        self.lapTimes = []
        self.lapNumbers = []

        super().__init__()

    def chooseRandomTyre(self):
        randomNum = random.randint(0, 2)
        if randomNum == 0:
            tyre = Tyre(2.0, 0.03, 1.8, 1.2)
        elif randomNum == 1:
            tyre = Tyre(1.6, 0.02, 1.3, 1.2)
        else:
            tyre = Tyre(1.1, 0.01, 0.85, 1.2)

        return tyre

    def isValidStrategy(self):
        returnVal = True
        if self.numberOfPitstops < 2:
            returnVal = False
        if self.numberOfPitstops > len(self.pitTyres):
            returnVal = False
        if self.initialTyre.getTyreCompound() == self.pitTyres[0].getTyreCompound():
            returnVal = False
        elif self.initialTyre.getTyreCompound() == self.pitTyres[1].getTyreCompound():
            returnVal = False
        elif self.pitTyres[1].getTyreCompound() == self.pitTyres[0].getTyreCompound():
            returnVal = False
        if self.pitStops[0] >= self.pitStops[1]:
            returnVal = False
        if self.pitStops[0] <= 0:
            returnVal = False
        if self.pitStops[1] >= self.maxLapsForRace:
            returnVal = False

        return returnVal

    def simulateRace(self):
        if self.isValidStrategy():
            self.resetTyres()
            self.currentTyre = self.initialTyre
            self.currentLap = 0
            while self.currentLap != self.maxLapsForRace:
                if self.pitStopCounter < len(self.pitStops) and self.currentLap == self.pitStops[self.pitStopCounter]:
                    self.currentTyre = self.pitTyres[self.pitStopCounter]
                    self.currentLapTime += 30
                    print("------")
                    print("Pitstop entered!")
                    print("Tyre changed to ", self.currentTyre)
                    print("Pitstop exited")
                    print("------")
                    self.pitStopCounter += 1

                self.currentLapTime += self.currentTyre.calculateLapTime(self.currentFuel, self.lapTimeFactor, 76)
                self.totalRaceTime += self.currentLapTime
                print("Lap number : ", self.currentLap + 1)
                print("Lap time : ", self.currentLapTime)
                print("Started lap with : ", self.currentFuel)
                self.lapTimes.append(self.currentLapTime)
                self.lapNumbers.append(self.currentLap + 1)
                self.currentLapTime = 0
                self.currentLap += 1
                self.fuelEffect = (self.currentFuel / (6 * self.startingFuel)) + 0.83
                self.currentTyre.addLap(self.fuelEffect, self.gripLossFactor)
                self.currentFuel -= 1.5
                print("")
        else:
            print("Invalid!")
            return False

    # NEEDS PITSTOP USAGE


    def resetTyres(self):
        self.initialTyre.reset()
        self.pitTyres[0].reset()
        self.pitTyres[1].reset()

    def getLapTimes(self):
        return self.lapTimes

    def getTotalRaceTime(self):
        return self.totalRaceTime

    def getLapNumbers(self):
        return self.lapNumbers

    #
    #
    # FOR SIMULATED ANNEALING
    #
    #

    def changeCompound(self):
        # halfway = int(self.maxLapsForRace / 2)
        # randomPit1 = random.randint(1, halfway)
        # randomPit2 = random.randint(halfway, self.maxLapsForRace)
        # self.pitStops[0] = randomPit1
        # self.pitStops[1] = randomPit2
        # tyres = [Tyre(2.0, 0.03, 1.8, 1.2), Tyre(1.6, 0.02, 1.3, 1.2), Tyre(1.1, 0.01, 0.85, 1.2)]
        # if(self.in)
        self.currentTyre = self.chooseRandomTyre()

    def changeLap(self):
        randomNum = random.randint(0, 1)
        coinToss = random.randint(0, 1)
        if randomNum == 0:
            if coinToss == 0:
                self.pitStops[0] += 1
            else:
                self.pitStops[1] -= 1
        else:
            if coinToss == 0:
                self.pitStops[0] += 1
            else:
                self.pitStops[1] -= 1

    def move(self):
        coinToss = random.randint(0, 1)
        if coinToss == 0:
            # print("Change compound")
            self.changeCompound()
        else:
            # print("Change lap")
            self.changeLap()

    def energy(self):
        return self.totalRaceTime


tyre1 = Tyre(2.0, 0.03, 1.8, 1.2)
tyre2 = Tyre(1.6, 0.02, 1.3, 1.2)
tyre3 = Tyre(1.1, 0.01, 0.85, 1.2)

pits1 = [40, 50]
pits2 = [25, 55]
pits3 = [30, 60]
tyres1 = [tyre2, tyre3]
tyres2 = [tyre1, tyre3]
tyres3 = [tyre1, tyre2]

mercedes = Car(tyre1, 2, pits1, tyres1, 0.996, 0.987)
ferrari = Car(tyre2, 2, pits2, tyres2, 0.99, 0.99)
redbull = Car(tyre3, 2, pits3, tyres3, 0.982, 0.991)
cars = [mercedes, ferrari, redbull]

print(mercedes.simulateRace())
print(ferrari.simulateRace())
print(redbull.simulateRace())

print("Total race time (mercedes) : ", math.floor(mercedes.getTotalRaceTime() / 60), " minutes ", math.floor(mercedes.getTotalRaceTime() % 60), " seconds")
print("Total race time (ferrari) : ", math.floor(ferrari.getTotalRaceTime() / 60), " minutes ", math.floor(ferrari.getTotalRaceTime() % 60), " seconds")
print("Total race time (redbull) : ", math.floor(redbull.getTotalRaceTime() / 60), " minutes ", math.floor(redbull.getTotalRaceTime() % 60), " seconds")

plt.plot(mercedes.getLapNumbers(), mercedes.getLapTimes(), '-x', markersize=2, color='green', alpha=0.5, label="Mercedes")
plt.plot(ferrari.getLapNumbers(), ferrari.getLapTimes(), '-x', markersize=2, color='red', alpha=0.5, label="Ferrari")
plt.plot(redbull.getLapNumbers(), redbull.getLapTimes(), '-x', markersize=2, color='blue', alpha=0.5, label="Red Bull")

plt.xlabel("Lap numbers")
plt.ylabel("Lap times")
plt.legend()
plt.title("F1 Tyre degradation")
plt.show()