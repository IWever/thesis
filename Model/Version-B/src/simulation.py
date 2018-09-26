from src.manoeuvringModel import manoeuverShip
import math
from matplotlib import patches


class Simulation:
    """ The class in which the simulation is created """

    activeShips = {}

    def __init__(self, world):
        self.world = world
        self.env = world.env

        module = __import__("Scenarios.%s" % self.world.experimentName, globals(), locals(), ['object'], 1)
        initial = getattr(module, "initial")

        initial(self)

        print("Created environment for simulation")

        self.env.process(self.runSimulation())
        # self.env.process(self.updateRadio())
        self.env.process(self.updateGUI())

    def runSimulation(self):
        self.world.log("Simulation started")
        while True:
            for shipname in self.activeShips:
                self.moveShip(shipname)

            for shipname in self.activeShips:
                self.updateStatistics(shipname)

            self.world.viewer.updatePlot()
            yield self.env.timeout(self.world.secondsPerStep/self.world.updateFrequency)

    def updateGUI(self):
        while True:
            self.world.root.update()
            yield self.env.timeout(1/30)

    def updateRadio(self):
        while True:
            for shipname in self.activeShips:
                self.activeShips[shipname].AIS.sendMessage(self.env.now)

    def addDynamicObject(self, objectName, location, course_deg, speed=None, rudderAngle=0, firstWaypoint=None):
        ship = self.world.do[objectName]

        ship.location = location
        ship.course = course_deg
        ship.heading = course_deg
        ship.rudderAngle = rudderAngle

        if speed is None:
            ship.speed = ship.vmean
            ship.telegraphSpeed = (ship.speed / ship.vmax) ** 2
            ship.acceleration = 0
        else:
            ship.speed = speed
            ship.telegraphSpeed = (ship.speed / ship.vmax) ** 2
            ship.acceleration = 0

        if firstWaypoint is None:
            pass
        else:
            ship.waypoints.append(firstWaypoint)

        ship.AIS.update(ship, time=self.env.now)

        self.activeShips[objectName] = ship

    def removeDynamicObject(self, objectName):
        ship = self.world.do[objectName]

        ship.location = [0, 0]
        ship.course = 0
        ship.heading = 0
        ship.drift = 0

        ship.speed = 0
        ship.acceleration = 0
        ship.headingChange = 0
        ship.telegraphSpeed = 0
        ship.rudderAngle = 0

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

        # Use model to move ship
        if ship.speed != 0:
            manoeuverShip(ship, dt)
            if ship.waypoints:
                ship.adjustRudder()

    def updateStatistics(self, objectName):
        shipA = self.activeShips[objectName]

        # Calculate closest point of approach
        for shipname in self.activeShips:
            if shipA is not self.activeShips[shipname]:
                shipB = self.activeShips[shipname]
                d = math.hypot(shipA.location[0]-shipB.location[0], shipA.location[1]-shipB.location[1])
                try:
                    shipA.perceivedShipCPA[shipB] = min(shipA.perceivedShipCPA[shipB], d)
                except KeyError:
                    shipA.perceivedShipCPA[shipB] = d

                if d < shipA.LBP:
                    self.world.log("%s and %s are too close (%d meter)" % (shipA.name, shipB.name, d))

    @staticmethod
    def createLandPatch(polygon):
        patch = patches.Polygon(polygon)
        patch.set_color("olive")
        patch.set_alpha(0.8)

        return patch

    @staticmethod
    def createDangerPatch(polygon):
        patch = patches.Polygon(polygon)
        patch.set_color("crimson")
        patch.set_alpha(0.2)

        return patch

    @staticmethod
    def createDangerLinePatch(polygon):
        patch = patches.Polygon(polygon)
        patch.set_linestyle("dashed")
        patch.set_edgecolor("crimson")

        return patch
