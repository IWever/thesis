from src.MTexperiment.general import *


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
        "Start speed": ship.speed,
        "Time": 0,
        "Timestamp": [],
        "locx": [],
        "locy": [],
        "Speed": [],
        "Acceleration*100":[],
        "Course": [],
        "Heading": [],
        "Drift": [],
        "Rudder": [],
        "Rudder real": [],
        "minOvershoot": 0,
        "maxOvershoot": 0
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
    result["minOvershoot"] = min(result["Course"]) + angle
    result["maxOvershoot"] = max(result["Course"]) - angle

    # Print results
    if printResult:
        print(result["test"])
        print("Overshoot is %f and %f" % (result["minOvershoot"], result["maxOvershoot"]))
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
        "Start speed": ship.speed,
        "Time": 0,
        "Timestamp": [],
        "locx": [],
        "locy": [],
        "Speed": [],
        "Acceleration*100": [],
        "Course": [],
        "Heading": [],
        "Drift": [],
        "Rudder": [],
        "Rudder real": [],
        "Advance": 0,
        "Tactical diameter": 0,
        "Steady turning diameter": 0,
        "Final speed": 0,
        "Steady drift angle": 0
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

        if (result["Course"][-1] > 5 * 180) and testflag == 0:
            maxSteadyTurn = result["locx"][-1]
            testflag = 1

        if result["Course"][-1] > 3*360:
            minSteadyTurn = result["locx"][-1]
            circle += 3

    # Calculations
    result["Advance"] = max(result["locy"])
    result["Tactical diameter"] = max(result["locx"])
    result["Steady turning diameter"] = maxSteadyTurn - minSteadyTurn
    result["Final speed"] = result["Speed"][-1]
    result["Steady drift angle"] = result["Drift"][-1]

    # Print results
    if printResult:
        print(result["test"])
        print("Tactical diameter: %d" % result["tactical diameter"])
        print("Advance: %d" % result["advance"])
        print("Steady turning diameter: %d" % result["steady turning diameter"])
        print("Final speed: %2.1f" % result["final speed"])
        print("Steady drift angle: %2.1f degrees" % result["steady drift angle"])
        print("")

    if reduceMemory:
        removeListsFromDict(result)

    return result


def evasiveManouvre(ship, speed, courseChange, dt = 0.01, changetime = 19, speedOther = 14, printResult=False, reduceMemory=True):
    # Set ship speed, location, angle and inertia
    setSpeed(ship, speed)
    resetShip(ship)

    # Result dictionary
    result = {
        "Shipname": ship.name,
        "test": ("Evasive manouvre | Course change: %d degrees | dt = %s s | changetime: %d s" % (courseChange, str(dt), changetime)),
        "Course change": courseChange,
        "Start speed": ship.speed,
        "Time": 0,
        "Speed other": speedOther,
        "Timestep": dt,
        "Timestamp": [],
        "locx": [],
        "locy": [],
        "Speed": [],
        "Acceleration*100": [],
        "Course": [],
        "Heading": [],
        "Drift": [],
        "Rudder": [],
        "Rudder real": [],
        "Distance": 0,
        "Extra time": 0,
        "Passing distance": 0
    }

    # Start of manouvre
    result = manouverStep(ship, dt, result)
    ship.rudderAngle = -35

    # Reduce rudder angle
    while changetime * ship.headingChange > - courseChange - ship.heading:
        result = manouverStep(ship, dt, result)
        if result["Time"] >= 2000:
            return None
    ship.rudderAngle = 0

    # Sail till angle of desired course change
    while ship.course > -courseChange:
        result = manouverStep(ship, dt, result)
        if result["Time"] >= 2000:
            return None
    ship.rudderAngle = 35

    # Return rudder to 0 position
    while changetime * ship.headingChange < - ship.course:
        result = manouverStep(ship, dt, result)
        if result["Time"] >= 2000:
            return None
    ship.rudderAngle = 0

    # Stop test
    while ship.course < 0:
        result = manouverStep(ship, dt, result)
        if result["Time"] >= 2000:
            return None

    # Calculate measures
    timeWhenStraight = ship.location[1] / (result["Start speed"] * 1852/3600)
    result["Extra time"] = result["Time"] - timeWhenStraight

    result["Passing distance"] = abs(ship.location[0]) + result["Extra time"] * speedOther * 1852 / 3600
    result["Distance"] = ship.location[1]

    # Print result
    if printResult:
        print("----- Trial: %s (%2.1f kn) -----" % (ship.name, speed))
        print(result["test"])
        print("Time: %d s | extra time gained: %d" % (result["time"], result["extraTime"]))
        print("Distance to side: %d | Distance forward: %d" % (abs(ship.location[0]), ship.location[1]))
        print("Passing distance behind ship with speed (%d kn): %d" % (speedOther, result["passingDistance"]))

    if reduceMemory:
        removeListsFromDict(result)

    return result
