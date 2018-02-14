from ship import Ship
from situation import Map

# Initialize situation
test = Map()

# Configuration settings
timestep = 10       # seconds

# Create vessels
shipA = Ship('Own ship', 28, 10, 4.6, 531)
shipB = Ship('Ship B', 320, 58, 20.8, 320438)
shipC = Ship('Ship C', 120, 24, 8, 20000)
shipD = Ship('Ship D', 120, 24, 8, 20000)

# Add vessel to situation
# name, speed, course, location in
test.addShip(shipA, 4, 0, 0, 0)
test.addShip(shipB, 20, 190, 12000, 16000)
test.addShip(shipC, 12, 160, -5000, 7000)
test.addShip(shipD, 4, 15, -2000, 500)

# Calculate CPA and simulate situation
Ship.testCPA(test)
test.runSimulation(timestep, shipA)

