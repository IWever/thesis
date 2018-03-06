from ship import Ship
from situation import Map
from calculation import testCPA
import matplotlib.pyplot as plt

# Initialize situation
test = Map()

# Create vessels
shipA = Ship('Own ship', 28, 10, 4.6, 531)
shipB = Ship('Ship B', 320, 58, 20.8, 320438)
shipC = Ship('Ship C', 120, 24, 8, 20000)
shipD = Ship('Ship D', 120, 24, 8, 20000)

# Add vessel to situation
# name, speed, course, location in
test.addShip(shipA, 8, 0, 0, 0)
test.addShip(shipB, 9, 190, 12000, 16000)
test.addShip(shipC, 12, 160, -5000, 7000)
test.addShip(shipD, 8, 15, -5000, -5500)

# Calculate CPA and simulate situation
test.createMap()
testCPA(test)
test.runSimulation(shipA, positionPrediction=True)


# plt.show(block=True)
