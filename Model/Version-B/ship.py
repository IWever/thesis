import math
from AIS_Message import AISMessage
import warnings
from matplotlib import patches


class Ship():
    """ The ship class"""

    location = [0, 0]
    speed = 0
    course = 0

    waypoints = []
    perceivedShips = []
    lastUpdate = 0

    # Objects used to store plot details
    markerPlot = None
    scalarPlot = None
    polygon = None
    polygonPlot = None
    tag = None

    def __init__(self, name, MMSI, LBP, width, depth,
                 displacement, deadweight, nominalSpeed_kn,
                 turningCoefficient=1, AISEquipment="A", shipType=99, color='blue', maxSpeed_kn=30):

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

        # Relevant Coefficients
        self.turningCoefficient = turningCoefficient

        # Create AIS message
        self.AIS = AISMessage(self)

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
        polygon_new = []

        loc = self.location
        theta = math.radians(self.course)

        for point in self.polygon:
            px = point[0]
            py = point[1]

            newx = -math.cos(theta) * px + math.sin(theta) * py + loc[0]
            newy = math.sin(theta) * px + math.cos(theta) * py + loc[1]

            polygon_new.append((newx, newy))

        patch = patches.Polygon(polygon_new)
        patch.set_color(self.color)

        return patch


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