import warnings


class AISMessage:
    """ Contains all information which a normal AIS message also contains:"""

    def __init__(self, ship, time=0):
        self.MMSI = ship.MMSI
        self.callSign = ship.name
        self.name = ship.name
        self.shipType = ship.shipType
        self.length = ship.LBP
        self.breadth = ship.B
        self.depth = ship.T
        self.equipmentType = ship.AISEquipmentType

        self.speed = ship.speed
        self.location = ship.location
        self.courseOverGround = ship.course
        self.heading = ship.course
        self.time = time

        if self.equipmentType == "A":
            self.freqBig = 360
            self.freqSmall = 10

        elif self.equipmentType == "B":
            self.freqBig = 360
            self.freqSmall = 30

        else:
            self.freqBig = 360
            self.freqSmall = 120
            warnings.warn("Unknown equipment type for AIS system")

    def __str__(self):
        return ("%s last update at %d s: %d m/s, [%d, %d], %d degrees" %
                (self.name, self.time, self.speed, self.location[0], self.location[1], self.courseOverGround))

    def update(self, ship, time=0):
        self.speed = ship.speed
        self.location = ship.location
        self.courseOverGround = ship.course
        self.heading = ship.course
        self.time = 0
