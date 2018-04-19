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
        ship.heading = course_deg

        if speed is None:
            ship.speed = ship.vmean
        else:
            ship.speed = speed

        ship.AIS.update(ship, time=self.env.now)

        self.activeShips[objectName] = ship

    def removeDynamicObject(self, objectName):
        ship = self.world.do[objectName]

        ship.location = [0, 0]
        ship.course = 0
        ship.heading = 0
        ship.speed = 0

        del self.activeShips[objectName]

        try:
            ship.markerPlot.remove()
        except AttributeError:
            pass

        try:
            ship.scalarPlot.remove()
        except AttributeError:
            pass
        except ValueError:
            pass

        try:
            ship.polygonPlot.remove()
        except AttributeError:
            pass

        try:
            ship.tag.remove()
        except AttributeError:
            pass

    def moveShip(self, objectName):
        ship = self.activeShips[objectName]

        # Update timestamp and get time since last update
        dt = self.env.now - ship.lastUpdate
        ship.lastUpdate = self.env.now

        # Convert to useful parameters
        speed_ms = dt * ship.speed * 1852/3600




        ship.location[0] += speed_ms * math.sin(math.radians(ship.course))
        ship.location[1] += speed_ms * math.cos(math.radians(ship.course))

    def initialPositionObjects(self):
        self.addDynamicObject("Tanker", [0, 0], 0)
        self.addDynamicObject("Bibby", [3000, 1000], 220)
        self.addDynamicObject("Bulk", [-2000, 5000], 120)

