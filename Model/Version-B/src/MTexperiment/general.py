from src.manoeuvringModel import manoeuverShip

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

    return ship

def removeEntriesFromDict(entries, dict):
    for key in entries:
        if key in dict:
            del dict[key]


def setSpeed(ship, speed):
    ship.speed = speed
    ship.telegraphSpeed = (ship.speed / ship.vmax) ** 2
    ship.speedSetting = ship.speed

def resetShip(ship):
    # Reset ship
    ship.location = [0, 0]
    ship.course = 0
    ship.heading = 0
    ship.drift = 0

    ship.headingChange = 0
    ship.rudderAngle = 0
    ship.rudderAngleReal = 0

def manouverStep(ship, dt, result):
    manoeuverShip(ship, dt)
    result["time"] += dt
    result["timestamp"].append(result["time"])
    result["locx"].append(ship.location[0])
    result["locy"].append(ship.location[1])
    result["speed"].append(ship.speed)
    result["acceleration"].append(ship.acceleration)
    result["course"].append(ship.course)
    result["heading"].append(ship.heading)
    result["rudder"].append(ship.rudderAngle)
    result["rudderReal"].append(ship.rudderAngleReal)


    return result