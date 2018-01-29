import numpy as np
import math

class Situation(object):
    """ The default settings for a ship which is used:

    Attributes:
        vessels: list of vessels relevant for situation
    """

    vessels = []

    def __init__(self):
        pass

    def courseCrossing(self, shipA, shipB):
        locA = np.transpose(np.matrix(shipA.location))
        locB = np.transpose(np.matrix(shipB.location))
        p = locA - locB

        dA = np.array([[math.sin(shipA.course)], [math.cos(shipA.course)]])
        dB = np.array([[math.sin(shipB.course)], [math.cos(shipB.course)]])
        d = np.concatenate((-dA, dB), axis=1)

        n1 = (np.linalg.inv(d) * p)[0,0]
        n2 = (np.linalg.inv(d) * p)[1,0]

        crossing = locA + n1 * dA
        relativeSpeed = n2/n1

        return crossing, relativeSpeed