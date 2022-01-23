from Car import Car
from Tyre import Tyre
import math
from matplotlib import pyplot as plt

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

print("~~MERCEDES~~")
print(mercedes.simulateRace())
print("~~FERRARI~~")
print(ferrari.simulateRace())
print("~~REDBULL~~")
print(redbull.simulateRace())

print("Total race time (mercedes) : ", math.floor(mercedes.getTotalRaceTime() / 60), " minutes ", math.floor(mercedes.getTotalRaceTime() % 60), " seconds")
print("Total race time (ferrari) : ", math.floor(ferrari.getTotalRaceTime() / 60), " minutes ", math.floor(ferrari.getTotalRaceTime() % 60), " seconds")
print("Total race time (redbull) : ", math.floor(redbull.getTotalRaceTime() / 60), " minutes ", math.floor(redbull.getTotalRaceTime() % 60), " seconds")

plt.plot(mercedes.getLapNumbers(), mercedes.getLapTimes(), '-x', markersize=2, color='green', alpha=0.5, label="Mercedes")
plt.plot(ferrari.getLapNumbers(), ferrari.getLapTimes(), '-x', markersize=2, color='red', alpha=0.5, label="Ferrari")
plt.plot(redbull.getLapNumbers(), redbull.getLapTimes(), '-x', markersize=2, color='blue', alpha=0.5, label="Red Bull")
# plt.plot(mercedes.getLapNumbers(), mercedes.getGripLevels(), '-x', markersize=2, color='green', alpha=0.5, label="Soft")
# plt.plot(ferrari.getLapNumbers(), ferrari.getGripLevels(), '-x', markersize=2, color='red', alpha=0.5, label="Medium")
# plt.plot(redbull.getLapNumbers(), redbull.getGripLevels(), '-x', markersize=2, color='blue', alpha=0.5, label="Hard")

plt.xlabel("Lap numbers")
plt.ylabel("Lap times")
plt.legend()
plt.title("F1 lap times")
plt.show()

