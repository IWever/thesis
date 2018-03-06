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

    Other parameters:
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
        return ("%s: at %s with a speed of %d m/s and course %d degrees" %
                (self.name, self.location, self.speed, self.course * 180 / math.pi))

    def updateLocation(self, timestep, ownship):
        self.location[0] += (timestep * self.speed * math.sin(self.course)
                             - timestep * ownship.speed * math.sin(ownship.course))
        self.location[1] += (timestep * self.speed * math.cos(self.course)
                             - timestep * ownship.speed * math.cos(ownship.course))

    def possiblePositions(self, time, precision=500):
        x = np.zeros(precision)
        y = np.zeros(precision)

        for i in range(0, len(x)):
            # new speed
            speed = self.possibleSpeeds()

            # new course
            course = self.possibleCourse()

            # calculate possible position
            x[i] = self.location[0] + time * speed * math.sin(course)
            y[i] = self.location[1] + time * speed * math.cos(course)

        return x, y

    def possibleSpeeds(self):
        randomSpeed = np.random.normal(scale=2)
        speed = self.speed * (1 + randomSpeed/10) - randomSpeed

        return speed

    def possibleCourse(self):
        randomCourse = np.random.normal(scale=5)
        course = self.course + randomCourse * math.pi / 180

        return course