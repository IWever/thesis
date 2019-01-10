import math
import numpy as np
from src.AIS_Message import AISMessage
import warnings
from matplotlib import patches

class Ship():
    """ The ship class"""
    def __init__(self, name, MMSI, LBP, width, depth,
                 displacement, deadweight, nominalSpeed_kn,
                 AISEquipment="A", shipType=99, color='blue', maxSpeed_kn=25):

        # Current situation of ship
        self.location = [0, 0]
        self.course = 0
        self.heading = 0
        self.drift = 0

        self.speed = 0
        self.acceleration = 0
        self.headingChange = 0

        self.telegraphSpeed = 0
        self.rudderAngle = 0
        self.rudderAngleReal = 0

        # Memory of the ship on surroundings
        self.waypoints = []
        self.perceivedShipCPA = {}
        self.lastUpdate = 0
        self.waypointUpdateNeeded = False

        # Objects used to store plot details
        self.markerPlot = None
        self.scalarPlot = None
        self.polygon = None
        self.polygonPlot = None
        self.polygonNumber = 0
        self.tag = None
        self.waypointMarker = None
        self.safetyDomain = None

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
        self.rudderAmplificationFactor = 2.5

        # Sea-trial
        self.seaTrialResults = None

        # Create AIS message
        self.AIS = AISMessage(self)

        # Visualisation details
        self.color = color
        self.createPolygon()

        if self.DWT > self.displacement:
            warnings.warn("Deadweigt bigger than displacement of %s" % self.name)

    def __str__(self):
        return (self.name)

    # Functions for plotting
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

    def safetyDomainEllipse(self):
        # Based on coldwell's domains
        a = math.radians(self.heading)

        cx = self.location[0] + math.cos(a) * 0.75 * self.LBP + math.sin(a) * 1.1 * self.LBP
        cy = self.location[1] - math.sin(a) * 0.75 * self.LBP + math.cos(a) * 1.1 * self.LBP
        center = (cx, cy)

        width = 5 * self.LBP
        height = 10 * self.LBP

        ellipse = patches.Ellipse(center, width, height, angle=-self.course, color=self.color, fill=False)

        return ellipse

    def safetyDomainCircle(self):
        # Based on expert feedback for busy area's
        cx = self.location[0]
        cy = self.location[1]
        center = (cx, cy)

        diameter = 2 * 370

        circle = patches.Ellipse(center, diameter, diameter, color=self.color, fill=False)

        return circle

    # Functions to automatically steer vessel
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
            angleOfError = 180 + math.degrees(np.arctan(dx/dy))
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
            angleOfError = self.course
            warnings.warn("Angle to waypoint not defined %d, %d" % (dx, dy))

        headingError = self.course - angleOfError

        if headingError < -180:
            headingError += 360
        elif headingError > 180:
            headingError -= 360

        if (abs(headingError) >= 25) and (distance2waypoint > 1500):
            self.rudderAngle = -35 * np.sign(headingError)
        elif abs(headingError) >= 15:
            self.rudderAngle = -25 * np.sign(headingError)
        else:
            self.rudderAngle = - 8 * headingError/10

        if distance2waypoint < self.LBP + 50:
            self.waypoints.pop(0)
            self.rudderAngle = 0
            self.waypointUpdateNeeded = True


if __name__ == "__main__":
    # Test creating a ship
    pass

    # shipA = Ship(name="Titia",
    #              MMSI=1,
    #              LBP=50, width=9,
    #              depth=4.5,
    #              displacement=50*9*4.5*0.75,
    #              deadweight=220,
    #              nominalSpeed_kn=13)
    #
    # print(shipA)
    # print(shipA.turningCircle())
    # print(shipA.turningSpeed())
    # print(shipA.AIS)
    #
    # for point in shipA.polygon:
    #     print(point)