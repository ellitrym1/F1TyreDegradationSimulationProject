import math
from ExperimentalFiles.Car import Car
from ExperimentalFiles.Tyre import Tyre
import random


class SimulatedAnnealing:
    def __init__(self):
        self.pitstops = []
        self.bestTime = 0
        self.idealPitstops = []
        self.raceTime = 0
        super().__init__()

    def randomPitstops(self):
        self.pitstop1 = random.randint(1, 35)
        self.pitstop2 = random.randint(36, 69)

        return [self.pitstop1, self.pitstop2]

    def checkForBestTime(self, currentTotalTime, counter):
        if counter == 1:
            self.bestTime = currentTotalTime
        else:
            if self.bestTime > currentTotalTime:
                self.bestTime = currentTotalTime
                self.idealPitstops = self.pitstops

    def chooseRandomTyre(self):
        randomNum = random.randint(0, 2)
        if randomNum == 0:
            tyre = Tyre(2.0, 0.03, 1.8, 1.2)
        elif randomNum == 1:
            tyre = Tyre(1.6, 0.02, 1.3, 1.2)
        else:
            tyre = Tyre(1.1, 0.01, 0.85, 1.2)

        return tyre

    def getPitTyres(self, initialTyre):
        satisfied = False
        pit1tyre = None
        pit2tyre = None
        pittyres = []
        while not satisfied:
            pit1tyre = self.chooseRandomTyre()
            pit2tyre = self.chooseRandomTyre()
            if pit1tyre.getTyreCompound() != initialTyre.getTyreCompound() and pit2tyre.getTyreCompound() != initialTyre.getTyreCompound():
                if pit1tyre.getTyreCompound() != pit2tyre.getTyreCompound():
                    pittyres.append(pit1tyre)
                    pittyres.append(pit2tyre)
#                    print(pittyres[0].getTyreCompound(), pittyres[1].getTyreCompound())
                    satisfied = True
            else:
                satisfied = False

        return pittyres

    def start(self, gripLossFactor, lapTimeFactor):
        counter = 1
        tyre1 = Tyre(2.0, 0.03, 1.8, 1.2)
        tyre2 = Tyre(1.6, 0.02, 1.3, 1.2)
        tyre3 = Tyre(1.1, 0.01, 0.85, 1.2)
        self.initialTyre = self.chooseRandomTyre()
        pitTyres = self.getPitTyres(self.initialTyre)
        self.tyres = [self.initialTyre.getTyreCompound(), pitTyres[0].getTyreCompound(), pitTyres[1].getTyreCompound()]
        # print(tyres)

        # print(self.pitstops)
        # self.car.simulateRace()
        # print("Total race time (car) : ", math.floor(self.car.getTotalRaceTime() / 60), " minutes ", math.floor(self.car.getTotalRaceTime() % 60), " seconds")

        while counter != 10000:
            self.pitstops = self.randomPitstops()
            car = Car(self.initialTyre, 2, self.pitstops, pitTyres, gripLossFactor, lapTimeFactor)
            car.simulateRace()
            self.raceTime = car.getTotalRaceTime()
            print(self.pitstops, self.raceTime)
            self.checkForBestTime(self.raceTime, counter)
            counter += 1

        print()
        print("Best lap time possible: ", math.floor(self.bestTime / 60), " minutes ", math.floor(self.bestTime % 60), " seconds")
        print("Pitstop configuration: ", self.idealPitstops)
        print("Tyre configuration: ", self.tyres)


sa = SimulatedAnnealing()

# Uncomment one of the sections below to find the best configuration
# for the specific car

print()
print("~~Mercedes~~")
sa.start(0.996, 0.987)
# print()
# print("~~Ferrari~~")
# sa.start(0.999, 0.99)
# print()
# print("~~Redbull~~")
# sa.start(0.982, 0.991)