import numpy as np
import math

from calculation import CPA

class Ship(object):
    """ The default settings for a ship which is used:

    Attributes:
        name: name of the vessel (string)
        LBP: length between perpendiculars (meter)
        B: width of vessel (meter)
        T: depth of vessel (meter)
        displacement: current displacement (tons)

        speed: speed over ground (m/s)
        course: course over ground (radians), where 0 is course of own vessel
        location: vector of int with current location of vessel

    """

    name = ""
    LBP = 0
    B = 0
    T = 0
    displacement = 0

    speed = 0.0
    course = 0
    location = np.empty(2)

    sixMinuteMap = np.zeros((50, 50))

    def __init__(self, name, LBP, width, depth, displacement):
        self.name = name
        self.LBP = LBP
        self.B = width
        self.T = depth
        self.displacement = displacement

    def __str__(self):
        return "%s: at %s with a speed of %d m/s and course %d degrees" % (self.name, self.location, self.speed, self.course * 180 / math.pi)

    def updateLocation(self, timestep, ownship):
        self.location[0] += timestep * self.speed * math.sin(self.course) - timestep * ownship.speed * math.sin(ownship.course)
        self.location[1] += timestep * self.speed * math.cos(self.course) - timestep * ownship.speed * math.cos(ownship.course)

    @staticmethod
    def testCPA(situation):
        shipsToTest = list(situation.vessels)

        while len(shipsToTest) > 0:
            ship1 = shipsToTest.pop(0)
            for ship2 in shipsToTest:
                CPA(ship1, ship2)