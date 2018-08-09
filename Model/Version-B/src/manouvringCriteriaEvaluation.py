from src.ship import Ship
from src.manoeuvring import manoeuverShip
import matplotlib.pyplot as plt
import numpy as np


# Functions
def addDynamicObject(ship, location, course_deg, speed=None, rudderAngle=0, firstWaypoint=None):
    ship.location = location
    ship.course = course_deg
    ship.heading = course_deg
    ship.rudderAngle = rudderAngle

    if speed is None:
        ship.speed = ship.vmean
        ship.telegraphSpeed = (ship.speed / ship.vmax) ** 2
        ship.speedSetting = ship.speed
    else:
        ship.speed = speed
        ship.telegraphSpeed = (ship.speed / ship.vmax) ** 2
        ship.speedSetting = ship.speed

    if firstWaypoint is None:
        pass
    else:
        ship.waypoints.append(firstWaypoint)

def evasiveManouvre(ship, courseChange, dt):
    t = 0

    # Start of manouvre
    ship.rudderAngle = -35
    print("---- Rudder angle = %d ----" % ship.rudderAngle)
    print(ship.course)
    print(t)

    manoeuverShip(ship, dt)
    t += dt

    while ship.course > -courseChange:
        manoeuverShip(ship, dt)
        t += dt

    ship.rudderAngle = 35
    print("---- Rudder angle = %d ----" % ship.rudderAngle)
    print(ship.course)
    print(t)


    while ship.course < -6:
        manoeuverShip(ship, dt)
        t += dt

    ship.rudderAngle = 0
    print("---- Rudder angle = %d ----" % ship.rudderAngle)
    print(ship.course)
    print(t)

    while ship.course < 0:
        manoeuverShip(ship, dt)
        t += dt

    print("---- Rudder angle = %d ----" % ship.rudderAngle)
    print(ship.course)
    print(t)

    return t

# Define ship
deadweight2displacement = 1.25

Tanker = Ship(name="Gulf Valour",
              MMSI=311072100,
              LBP=249,
              width=48,
              depth=13.2,
              displacement=114900 * deadweight2displacement,
              deadweight=114900,
              nominalSpeed_kn=10.5,
              color='green')

Tug = Ship(name="DAMEN ASD2411",
           MMSI=710030460,
           LBP=24.47,
           width=11.33,
           depth=5.61,
           displacement=492,
           deadweight=150,
           nominalSpeed_kn=13,
           color='black')

addDynamicObject(Tanker, [0, 0], 0, speed=10.5)
addDynamicObject(Tug, [0, 0], 0, speed=10.3)

# Create axis for plot

# Sail ship for x seconds
timeTanker = evasiveManouvre(Tanker, 20, .5)
timeTug = evasiveManouvre(Tug, 20, .5)

# Determine dy and dt
print("--- Final location and time Tanker ------")
print(Tanker.location)
print(timeTanker)

print("--- Final location and time Tug ------")
print(Tug.location)
print(timeTug)
