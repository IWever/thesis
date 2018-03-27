import math

class Simulation:
    """ The class in which the simulation is created """

    activeShips = {}

    def __init__(self, world):
        self.world = world
        self.env = world.env

        self.initialPositionObjects()

        print("Created environment for simulation")

        self.env.process(self.runSimulation())
        self.env.process(self.updateGUI())

    def runSimulation(self):
        while True:
            for shipname in self.activeShips:
                self.moveShip(shipname)

            self.world.viewer.updatePlot()
            yield self.env.timeout(self.world.secondsPerStep/self.world.updateFrequency)

    def updateGUI(self):
        while True:
            self.world.root.update()
            yield self.env.timeout(1/50)

    def addDynamicObject(self, objectName, location, course_deg, speed=None):
        ship = self.world.do[objectName]

        ship.location = location
        ship.course = course_deg

        if speed is None:
            ship.speed = ship.vmean
        else:
            ship.speed = speed

        ship.AIS.update(ship, time=self.env.now)

        self.activeShips[objectName] = ship

    def moveShip(self, objectName):
        ship = self.activeShips[objectName]

        dt = self.env.now - ship.lastUpdate
        ship.lastUpdate = self.env.now

        s = dt * ship.speed * 1852/3600

        ship.location[0] += s * math.sin(math.radians(ship.course))
        ship.location[1] += s * math.cos(math.radians(ship.course))

    def initialPositionObjects(self):
        self.addDynamicObject("Tanker", [0, 0], 0)
        self.addDynamicObject("Bibby", [3000, 1000], 220)
        self.addDynamicObject("Bulk", [-2000, 5000], 120)