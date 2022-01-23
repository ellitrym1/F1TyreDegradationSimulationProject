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
        # print("Start: ", self.currentGrip)
        # print("Fuel effect: ", fuelEffect)

        if self.currentGrip > self.switchPoint:
            self.currentGrip = (self.currentGrip - (self.initialDeg * gripLossFactor * fuelEffect))
        elif self.currentGrip > 0.2:
            self.currentGrip = (self.currentGrip - (self.switchDeg * gripLossFactor * fuelEffect))
        else:
            self.currentGrip = 0.0

        # print("End: ", self.currentGrip)
        return self.currentGrip

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
