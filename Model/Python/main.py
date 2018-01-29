from ship import Ship
from situation import Situation
import math
import numpy as np

test = Situation()

shipA = Ship("Ship A", 28, 10, 4.6, 531)
shipB = Ship("Ship B", 320, 58, 20.8, 320438)

shipA.speed = 5
shipA.course = .5 * math.pi
shipA.location = [-250, 500]

shipB.speed = 5
shipB.course = 0
shipB.location = [0, 0]

[crossingPoint, relativeSpeed] = test.courseCrossing(shipA, shipB)

print(relativeSpeed)
print(np.transpose(crossingPoint))
print(shipA)
print(shipB)