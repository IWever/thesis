import math
import numpy as np
from AIS_Message import AISMessage
from controller import Controller
import warnings
from matplotlib import patches

class Ship():
    """ The ship class"""
    def __init__(self, name, MMSI, LBP, width, depth,
                 displacement, deadweight, nominalSpeed_kn,
                 turningCoefficient=1, AISEquipment="A", shipType=99, color='blue', maxSpeed_kn=25):

        # Current situation of ship
        self.location = [0, 0]
        self.course = 0
        self.heading = 0
        self.drift = 0

        self.speed = 0
        self.headingChange = 0

        self.acceleration = 0

        self.telegraphSpeed = 0
        self.rudderAngle = 0

        # Memory of the ship on surroundings
        self.waypoints = []
        self.perceivedShips = []
        self.lastUpdate = 0

        # Objects used to store plot details
        self.markerPlot = None
        self.scalarPlot = None
        self.polygon = None
        self.polygonPlot = None
        self.polygonNumber = 0
        self.tag = None
        self.waypointMarker = None

        # Ship registration details
        self.name = name
        self.MMSI = MMSI
        self.shipType = shipType
        self.AISEquipmentType = AISEquipment

        # Ship characteristics
        self.LBP = LBP
        self.B = width
        self.T = depth
        self.displacement = displacement
        self.DWT = deadweight
        self.vmean = nominalSpeed_kn
        self.vmax = maxSpeed_kn
        self.Cb = LBP * width * depth / displacement

        # Relevant Coefficients
        self.turningCoefficient = turningCoefficient

        # Create AIS message
        self.AIS = AISMessage(self)

        # Create controller for ship
        self.controller = Controller(self)

        # Visualisation details
        self.color = color
        self.createPolygon()

        if self.DWT > self.displacement:
            warnings.warn("Deadweigt bigger than displacement of %s" % self.name)

    def __str__(self):
        return ("%s: at %s with a speed of %d m/s and course %d degrees" %
                (self.name, self.location, self.speed, self.course))

    def turningCircle(self):
        """" Steady turning radius in [meter] """
        tc = 3.5 * self.LBP * self.turningCoefficient
        return tc

    def turningSpeed(self):
        """" Steady turning radius in [deg/minute] """
        ts = (10000 / self.LBP) * self.turningCoefficient
        return ts

    def createPolygon(self):
        self.polygon = [(-.5 * self.B, .35 * self.LBP),
                        (0, 0.5 * self.LBP),
                        (.5 * self.B, .35 * self.LBP),
                        (.5 * self.B, -.5 * self.LBP),
                        (-.5 * self.B, -.5 * self.LBP)]

    def patchPolygon(self):
        self.polygonNumber += 1
        polygon_new = []

        loc = self.location
        theta = math.radians(self.heading)

        for point in self.polygon:
            px = point[0]
            py = point[1]

            newx = -math.cos(theta) * px + math.sin(theta) * py + loc[0]
            newy = math.sin(theta) * px + math.cos(theta) * py + loc[1]

            polygon_new.append((newx, newy))

        patch = patches.Polygon(polygon_new)
        patch.set_color(self.color)

        return patch

    def adjustRudder(self):
        locationError = np.asarray(self.waypoints[0]) - np.asarray(self.location)
        distance2waypoint = math.sqrt(locationError[0] ** 2 + locationError[1] ** 2)

        dx = locationError[0]
        dy = locationError[1]

        if dx > 0 and dy > 0:
            angleOfError = math.degrees(np.arctan(dx/dy))
        elif dx > 0 and dy < 0:
            angleOfError = 90 + math.degrees(np.arctan(abs(dy)/dx))
        elif dx < 0 and dy < 0:
            angleOfError = 180 + math.degrees(np.arctan(abs(dy)/abs(dx)))
        elif dx < 0 and dy > 0:
            angleOfError = 360 - math.degrees(np.arctan(abs(dx)/dy))
        elif dx == 0 and dy == 0:
            warnings.warn("Ship exactly at waypoint, rudder angle put at 0")
            self.rudderAngle = 0
            return
        elif dx == 0:
            angleOfError = np.sign(dy) * 180
        elif dy == 0:
            angleOfError = np.sign(dx) * 90
        else:
            warnings.warn("Angle to waypoint not defined %d, %d" % (dx, dy))

        headingError = self.course - angleOfError

        if headingError < -180:
            headingError += 360
        elif headingError > 180:
            headingError -= 360

        if abs(headingError) >= 25:
            self.rudderAngle = -35 * np.sign(headingError)
        elif abs(headingError) >= 10:
            self.rudderAngle = -25 * np.sign(headingError)
        else:
            self.rudderAngle = -8 * headingError/10

        if distance2waypoint < self.LBP + 50:
            self.waypoints.pop(0)

        if self.name == "Gulf Valour":
            print("------")
            print(self.location)
            print(self.waypoints[0])
            print("LocationError:")
            print(locationError[0])
            print(locationError[1])
            print("Course, angleOfError and headingError")
            print(self.course)
            print(angleOfError)
            print(headingError)
            print("Rudder angle:")
            print(self.rudderAngle)

if __name__ == "__main__":
    # Test creating a ship
    shipA = Ship(name="Titia",
                 MMSI=1,
                 LBP=50, width=9,
                 depth=4.5,
                 displacement=50*9*4.5*0.75,
                 deadweight=220,
                 nominalSpeed_kn=13)

    print(shipA)
    print(shipA.turningCircle())
    print(shipA.turningSpeed())
    print(shipA.AIS)

    for point in shipA.polygon:
        print(point)
