import numpy as np
import math
import matplotlib.pyplot as plt


def courseCrossing(shipA, shipB):
    """ Calculate the point where courses intersect """
    locA = np.transpose(np.matrix(shipA.location))
    locB = np.transpose(np.matrix(shipB.location))
    p = locA - locB

    UA = np.array([[math.sin(shipA.course)], [math.cos(shipA.course)]])
    UB = np.array([[math.sin(shipB.course)], [math.cos(shipB.course)]])

    d = np.concatenate((UB, -UA), axis=1)
    n = np.linalg.inv(d) * p

    crossing = locB + n[0, 0] * UB
    relativeSpeed = n[1, 0] / n[0, 0]

    plt.figure('Map')
    plt.plot(crossing[0, 0], crossing[1, 0], marker='x', color='r')

    return [crossing, relativeSpeed]


def CPA(shipA, shipB):
    """ Calculate the closest point of approach between two vessels """

    if shipA == shipB:
        return

    xA = shipA.location[0]
    yA = shipA.location[1]
    VA = shipA.speed
    UxA = math.sin(shipA.course)
    UyA = math.cos(shipA.course)

    xB = shipB.location[0]
    yB = shipB.location[1]
    VB = shipB.speed
    UxB = math.sin(shipB.course)
    UyB = math.cos(shipB.course)

    if (shipB.course == shipA.course) and (shipB.speed == shipA.speed):
        distance = math.sqrt( (xB-xA)**2 + (yB - yA) ** 2)
        print('%s and %s parallel: %d meter apart' % (shipA.name, shipB.name, distance))
        return [distance, 0]

    distance = math.sqrt((
                         yA * VA * UxA - VA * yB * UxA - yA * VB * UxB + VB * UxB * yB - xA * VA * UyA + xB * VA * UyA + xA * VB * UyB - xB * VB * UyB) ** 2 / (
                         UxA ** 2 * VA ** 2 - 2 * UxA * UxB * VA * VB + UxB ** 2 * VB ** 2 + UyA ** 2 * VA ** 2 - 2 * UyA * UyB * VA * VB + UyB ** 2 * VB ** 2))
    time_s = (((-xA + xB) * UxA - UyA * (yA - yB)) * VA + VB * ((xA - xB) * UxB + UyB * (yA - yB))) / (
    (UxA ** 2 + UyA ** 2) * VA ** 2 - 2 * VB * (UxA * UxB + UyA * UyB) * VA + VB ** 2 * (UxB ** 2 + UyB ** 2))

    print('CPA between %s and %s: %d meter after %d minutes' % (shipA.name, shipB.name, distance, time_s / 60))

    return [distance, time_s]
