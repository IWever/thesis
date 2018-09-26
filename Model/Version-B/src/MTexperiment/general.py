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

def removeListsFromDict(dict):
    entries = []
    for key in dict:
        if isinstance(dict[key], list):
            entries.append(key)
    removeEntriesFromDict(entries, dict)

def setSpeed(ship, speed):
    ship.speed = speed
    ship.telegraphSpeed = (ship.speed / ship.vmax) ** 2
    ship.acceleration = 0

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
    result["Time"] += dt
    result["Timestamp"].append(result["Time"])
    result["locx"].append(ship.location[0])
    result["locy"].append(ship.location[1])
    result["Speed"].append(ship.speed)
    result["Acceleration*100"].append(ship.acceleration*100)
    result["Course"].append(ship.course)
    result["Heading"].append(ship.heading)
    result["Drift"].append(ship.drift)
    result["Rudder"].append(ship.rudderAngle)
    result["Rudder real"].append(ship.rudderAngleReal)


    return result