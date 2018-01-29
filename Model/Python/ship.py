import numpy as np
import math

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

    def __init__(self, name, LBP, width, depth, displacement):
        self.name = name
        self.LBP = LBP
        self.B = width
        self.T = depth
        self.displacement = displacement

    def __str__(self):
        return "%s: at %s with a speed of %d m/s and course %d degrees" % (self.name, self.location, self.speed, self.course * 180 / math.pi)
