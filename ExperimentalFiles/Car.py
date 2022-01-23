import random
from .Tyre import Tyre


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
        self.currentGrips = []

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
                    # print("------")
                    # print("Pitstop entered!")
                    # print("Tyre changed to ", self.currentTyre.getTyreCompound())
                    # print("Pitstop exited")
                    # print("------")
                    self.pitStopCounter += 1

                self.currentLapTime += self.currentTyre.calculateLapTime(self.currentFuel, self.lapTimeFactor, 76)
                self.totalRaceTime += self.currentLapTime
                # print("Lap number : ", self.currentLap + 1)
                # print("Lap time : ", self.currentLapTime)
                # print("Started lap with : ", self.currentFuel)
                self.lapTimes.append(self.currentLapTime)
                self.lapNumbers.append(self.currentLap + 1)
                self.currentLapTime = 0
                self.currentLap += 1
                self.fuelEffect = (self.currentFuel / (6 * self.startingFuel)) + 0.83
                self.currentGrips.append(self.currentTyre.addLap(self.fuelEffect, self.gripLossFactor))
                # self.currentGrip.append(self.currentTyre.addLap(self.fuelEffect, self.gripLossFactor))
                self.currentFuel -= 1.5
                # print("")
        else:
            print("Invalid!")
            return False

    def energy(self):
        return self.totalRaceTime

    # NEEDS PITSTOP USAGE
    def changeCompound(self):
        randomPit = random.randint(1, self.maxLapsForRace)
        self.currentTyre = self.chooseRandomTyre()

    def changeLap(self):
        randomPit = random.randint(1, self.maxLapsForRace)
        randomNum = random.randint(0, 1)
        if randomNum == 0:
            randomPit += 1
        else:
            randomPit -= 1

    def move(self):
        coinToss = random.randint(0, 1)
        if coinToss == 0:
            print("Change compound")
            self.changeCompound()
        else:
            print("Change lap")
            self.changeLap()

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

    def getGripLevels(self):
        return self.currentGrips