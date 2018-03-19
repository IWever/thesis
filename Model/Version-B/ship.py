import math
from AIS_Message import AISMessage
import warnings


class Ship():
    """ The ship class"""

    location = [0, 0]
    speed = 0
    course = 0

    waypoints = []
    perceivedShips = []

    def __init__(self, name, MMSI, LBP, width, depth,
                 displacement, deadweight, nominalSpeed_kn,
                 turningCoefficient=1, AISEquipment="A", shipType=99):

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

        # Relevant Coefficients
        self.turningCoefficient = turningCoefficient

        # Create AIS message
        self.AIS = AISMessage(self)

        if self.DWT > self.displacement:
            warnings.warn("Deadweigt bigger than displacement of %s" % self.name)

    def __str__(self):
        return ("%s: at %s with a speed of %d m/s and course %d degrees" %
                (self.name, self.location, self.speed, self.course * 180 / math.pi))

    def turningCircle(self):
        """" Steady turning radius in [meter] """
        tc = 3.5 * self.LBP * self.turningCoefficient
        return tc

    def turningSpeed(self):
        """" Steady turning radius in [deg/minute] """
        ts = (10000 / self.LBP) * self.turningCoefficient
        return ts


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
