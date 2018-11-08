from src.MTexperiment.general import *
import math

# Performing a standard sea-trial
def seatrial(ship, speed, trialsList=None, dt=0.01, printResult=False, reduceMemory=True):
    implementedTrials = ['zigzag - 10:10', 'zigzag - 20:20', 'turning circle - 35']

    # Select trials
    if trialsList is None:
        trials = implementedTrials
    else:
        trials = trialsList
        for trial in trialsList:
            if trial not in implementedTrials:
                print("%s not implemented" % trial)

    # Dict to store results for each trial
    tests = {}

    if printResult:
        print("----- Sea-trial: %s (%2.1f kn) -----" % (ship.name, speed))

    for test in trials:
        # Check if chosen trials exist
        if test not in ['zigzag - 10:10', 'zigzag - 20:20', 'turning circle - 35']:
            print("%s is not known as a test")
            break

    # Run selected trials
    if 'zigzag - 10:10' in trials:
        testName = '%s | zigzag - 10:10 | speed: %d' % (ship.name, speed)
        tests[testName] = zigzag(ship, speed, 10, dt=dt, printResult=printResult, reduceMemory=reduceMemory)

    if 'zigzag - 20:20' in trials:
        testName = '%s | zigzag - 20:20 | speed: %d' % (ship.name, speed)
        tests[testName] = zigzag(ship, speed, 20, dt=dt, printResult=printResult, reduceMemory=reduceMemory)

    if 'turning circle - 35' in trials:
        testName = '%s | turning circle - 35 | speed: %d' % (ship.name, speed)
        tests[testName] = turningCirlce(ship, speed, 35, dt=dt, printResult=printResult, reduceMemory=reduceMemory)

    return tests


# Zigzag manoeuvre test with similar rudder and change of course angle
def zigzag(ship, speed, angle, dt, printResult, reduceMemory):
    # Set ship speed, location, angle and inertia
    setSpeed(ship, speed)
    resetShip(ship)

    # Result dictionary
    result = {
        "Shipname": ship.name,
        "test": ("Zigzag %d:%d| dt: %f" % (angle, angle, dt)),
        "Start speed [knots]": ship.speed,
        "Time [seconds]": 0,
        "Timestamp": [],
        "locx": [],
        "locy": [],
        "Speed [knots]": [],
        "Acceleration*100 [m/s^2]":[],
        "Course [degrees]": [],
        "Heading [degrees]": [],
        "Drift [degrees]": [],
        "Rudder [degrees]": [],
        "Rudder real [degrees]": [],
        "minOvershoot [degrees]": 0,
        "maxOvershoot [degrees]": 0
    }

    # Start of manoeuvrer and change rudder
    result = manouverStep(ship, dt, result)

    ship.rudderAngle = -angle
    while ship.course > -angle:
        result = manouverStep(ship, dt, result)

    ship.rudderAngle = angle
    while ship.course < angle:
        result = manouverStep(ship, dt, result)

    ship.rudderAngle = -angle
    while ship.course > -angle:
        result = manouverStep(ship, dt, result)

    ship.rudderAngle = angle
    while ship.course < angle:
        result = manouverStep(ship, dt, result)

    ship.rudderAngle = -angle
    while ship.course > -angle:
        result = manouverStep(ship, dt, result)

    ship.rudderAngle = angle
    while ship.course < angle:
        result = manouverStep(ship, dt, result)

    # Calculations
    result["minOvershoot [degrees]"] = min(result["Course [degrees]"]) + angle
    result["maxOvershoot [degrees]"] = max(result["Course [degrees]"]) - angle

    # Print results
    if printResult:
        print(result["test"])
        print("Overshoot is %f and %f" % (result["minOvershoot [degrees]"], result["maxOvershoot [degrees]"]))
        print("")

    # Reduce stored data by removing part of test result
    if reduceMemory:
        removeListsFromDict(result)

    return result


# Turning circle test for specified rudder angle
def turningCirlce(ship, speed, rudderAngle=35, dt=0.01, printResult=False, reduceMemory=True):
    # Set ship speed, location, angle and inertia
    setSpeed(ship, speed)
    resetShip(ship)

    # Result dictionary
    result = {
        "Shipname": ship.name,
        "test": ("Turning circle | rudder angle: %d | dt: %f" % (rudderAngle, dt)),
        "Start speed [knots]": ship.speed,
        "Time [seconds]": 0,
        "Timestamp": [],
        "locx": [],
        "locy": [],
        "Speed [knots]": [],
        "Acceleration*100 [m/s^2]": [],
        "Course [degrees]": [],
        "Heading [degrees]": [],
        "Drift [degrees]": [],
        "Rudder [degrees]": [],
        "Rudder real [degrees]": [],
        "Advance distance [meter]": 0,
        "Tactical diameter [meter]": 0,
        "Steady turning diameter [meter]": 0,
        "Final speed [knots]": 0,
        "Steady drift angle [degrees]": 0
    }

    # Start of manoeuvrer and change rudder
    circle = 0
    testflag = 0
    maxSteadyTurn = 0
    minSteadyTurn = 0

    result = manouverStep(ship, dt, result)
    ship.rudderAngle = rudderAngle

    while circle <= 3:
        result = manouverStep(ship, dt, result)

        if (result["Course [degrees]"][-1] > 5 * 180) and testflag == 0:
            maxSteadyTurn = result["locx"][-1]
            testflag = 1

        if result["Course [degrees]"][-1] > 3*360:
            minSteadyTurn = result["locx"][-1]
            circle += 3

    # Calculations
    result["Advance distance [meter]"] = max(result["locy"])
    result["Tactical diameter [meter]"] = max(result["locx"])
    result["Steady turning diameter [meter]"] = maxSteadyTurn - minSteadyTurn
    result["Final speed [knots]"] = result["Speed [knots]"][-1]
    result["Steady drift angle [degrees]"] = result["Drift [degrees]"][-1]

    # Print results
    if printResult:
        print(result["test"])
        print("Tactical diameter: %d" % result["Tactical diameter [meter]"])
        print("Advance: %d" % result["Advance distance [meter]"])
        print("Steady turning diameter: %d" % result["Steady turning diameter [meter]"])
        print("Final speed: %2.1f" % result["Final speed [knots]"])
        print("Steady drift angle: %2.1f degrees" % result["Steady drift angle [degrees]"])
        print("")

    if reduceMemory:
        removeListsFromDict(result)

    return result


def evasiveManouvre(ship, speed, courseChange, dt=0.01, changetime=0, speedOther=14, maxRudder=35, printResult=False, reduceMemory=True):
    # Set ship speed, location, angle and inertia
    setSpeed(ship, speed)
    resetShip(ship)

    if changetime != 0:
        print("WARNING: Change time turned off")

    # Result dictionary
    result = {
        "Shipname": ship.name,
        "test": ("Evasive manouvre | Course change: %d degrees | dt = %s s | changetime: %d s" % (courseChange, str(dt), changetime)),
        "Start speed [knots]": ship.speed,
        "Speed other [knots]": speedOther,
        "Time [seconds]": 0,
        "Timestep [seconds]": dt,
        "Timestamp": [],
        "locx": [],
        "locy": [],
        "Speed [knots]": [],
        "Acceleration*100 [m/s^2]": [],
        "Course [degrees]": [],
        "Heading [degrees]": [],
        "Drift [degrees]": [],
        "Rudder [degrees]": [],
        "Rudder real [degrees]": [],
        "Distance till initial CPA": 0,
        "Extra time [seconds]": 0,
        "Passing distance [meter]": 0,
        "CPA [meter]": 0,
        "Overshoot [degrees]": 0,
        "Max course [degrees]": 0,
        "Max rudder [degrees]": maxRudder
    }

    # Start of manouvre
    result = manouverStep(ship, dt, result)
    ship.rudderAngle = -maxRudder

    # Reduce rudder angle
    while courseChange > - ship.heading:
        result = manouverStep(ship, dt, result)
        if result["Time [seconds]"] >= 1200:
            return None
    ship.rudderAngle = 0

    # Sail till angle of desired course change
    while ship.course > -courseChange:
        result = manouverStep(ship, dt, result)
        if result["Time [seconds]"] >= 3600:
            return None
    ship.rudderAngle = maxRudder

    # Return rudder to 0 position
    while changetime * ship.headingChange < - ship.course:
        result = manouverStep(ship, dt, result)
        if result["Time [seconds]"] >= 3600:
            return None
    ship.rudderAngle = 0

    # Stop test
    while ship.course < 0:
        result = manouverStep(ship, dt, result)
        if result["Time [seconds]"] >= 3600:
            return None


    # Calculate measures
    timeWhenStraight = ship.location[1] / (result["Start speed [knots]"] * 1852 / 3600)
    result["Extra time [seconds]"] = result["Time [seconds]"] - timeWhenStraight
    result["Distance till initial CPA [meter]"] = ship.location[1]
    result["Overshoot [degrees]"] = -min(result["Course [degrees]"]) - courseChange
    result["Max course [degrees]"] = -min(result["Course [degrees]"])
    result["Passing distance [meter]"] = abs(ship.location[0]) + result["Extra time [seconds]"] * speedOther * 1852 / 3600

    CPA = 10000000
    xStartShipB = -timeWhenStraight * speedOther * 1852/3600
    for i in range(0, len(result["Timestamp"])):
        xlocShipB = xStartShipB + result["Timestamp"][i] * speedOther * 1852 / 3600
        distance = math.hypot(result["locx"][i] - xlocShipB, result["locy"][i] - result["Distance till initial CPA [meter]"])
        CPA = min(CPA, distance)

    result["CPA [meter]"] = CPA

    # Print result
    if printResult:
        print("----- Trial: %s (%2.1f kn) -----" % (ship.name, speed))
        print(result["test"])
        print("Time: %d s | extra time gained: %d | Overshoot: %2.1f" % (result["Time [seconds]"], result["Extra time [seconds]"], result["Overshoot [degrees]"]))
        print("Distance to side: %d | Distance forward: %d" % (abs(ship.location[0]), ship.location[1]))
        print("Passing distance behind ship with speed (%d kn): %d meter and CPA: %d meter" % (speedOther, result["Passing distance [meter]"], result["CPA [meter]"]))

    if reduceMemory:
        removeListsFromDict(result)

    return result

