from src.MTexperiment.manoeuvreTests import *
from src.MTexperiment.plotResults import *
from src.MTexperiment.createShips import createShips

import random

# Create ships
[shipList, Tanker, Tug, EmmaMaersk, Astrorunner, CF7200] = createShips()

# Sea-trials to update ship-details
# for ship in shipList:
#     speedList = [ship.vmean]
#     for speed in speedList:
#
#
#     plotPath("Paths from sea-trials", ship.seaTrialResults)


# Running evasive manoeuvres to determine domain for decision making
plotnumber = None # no plot is being made
testResults = {}
tests = ["Rudder-test"]

if "sea-trial" in tests:
    for ship in shipList:
        speed = ship.vmean

        results = seatrial(ship, speed, trials=['zigzag - 10:10', 'zigzag - 20:20'], printResult=True, reduceMemory=False)
        testResults[ship.name] = results
        plotPath("Paths-from-zig-zag-tests", testResults[ship.name])

        results = seatrial(ship, speed, trials=['turning circle - 35'], printResult=True, reduceMemory=False)
        testResults[ship.name] = results
        plotPath("Paths-from-turning-circle", testResults[ship.name])


if "Rudder-test" in tests:
    ship = Astrorunner
    speed = ship.vmean
    angle = 20
    dt = 0.01

    print("Evasive manoeuvre to %d degrees with %s (%d kn)" % (angle, ship.name, speed))
    testResults[ship.name + ("%2d" % angle)] = evasiveManouvre(ship, speed, angle, dt=dt, reduceMemory=False)
    plotLinesOverTime("Evasive-manoeuvre-%d-degrees-%s-(%d-kn)" % (angle, ship.name, speed), testResults, ["course", "heading", "rudder", "rudderReal", "speed"])

    print("Zig-zag 10:10 with %s (%d kn)" % (ship.name, speed))
    results = seatrial(ship, speed, trials=['zigzag - 10:10'], printResult=False, reduceMemory=False)
    plotLinesOverTime("Zig-zag-10-10-%s-(%d-kn)" % (ship.name, speed), results, ["course", "heading", "rudder", "rudderReal", "speed", "acceleration"])

    print("Zig-zag 20:20 with %s (%d kn)" % (ship.name, speed))
    results = seatrial(ship, speed, trials=['zigzag - 20:20'], printResult=False, reduceMemory=False)
    plotLinesOverTime("Zig-zag-20-20-%s-(%d-kn)" % (ship.name, speed), results, ["course", "heading", "rudder", "rudderReal", "speed", "acceleration"])


if "angle" in tests:
    for ship in [Tanker, Tug]:
        speed = ship.vmean
        for angle in [5, 10, 20, 30, 45, 90]:
           testResults[ship.name + (" - %d deg" % angle)] = evasiveManouvre(ship, speed, angle, reduceMemory=False)

    plotPath("Paths for different course change angles", testResults)

if "changetime" in tests:
    for ship in shipList:
        speed = ship.vmean
        angle = 20
        for changetime in [8, 10, 11, 12, 13, 14, 15, 18, 20, 25]:
            result = evasiveManouvre(ship, speed, angle, changetime=changetime, reduceMemory=False)
            if result is None:
                print("%s - test failed, change time: %d" % (ship.name, changetime))
            else:
                testResults[ship.name + (" - %d s" % changetime)] = result

    plotPath("Variable moment to reduce rudder angle", testResults)

if "speed" in tests:
    for ship in [Tanker, Tug]:
        for speed in [5, 10, 15, 20]:
            for angle in [10, 20, 30, 45, 60, 90]:
                testResults[ship.name + (" - startSpeed: %d kn| angle deg: %d" % (speed, angle))] = evasiveManouvre(ship, speed, angle, reduceMemory=False)

    plotPath("Effect of initial speed on path", testResults)

if "speed other" in tests:
    ship = EmmaMaersk
    speed = 12

    for speedOther in [5, 7, 10, 12, 15, 18, 24]:
        for angle in [10, 20, 30, 45, 60, 90]:
            testResults["startSpeed: %d kn| otherSpeed: %d kn| angle deg: %d" % (speed, speedOther, angle)] = evasiveManouvre(ship, speed, angle, speedOther=speedOther)
            print("otherSpeed: %d kn| angle deg: %d" % (speedOther, angle))

    plotScatter("Effect of others speed on time to decide", testResults, "time", "passingDistance", "speedOther")

if "dt" in tests:
    for ship in [Tanker, Tug]:
        speed = ship.vmean
        angle = 20
        for dt in [0.001, 0.01, 0.1, 0.25, 1]:
           testResults[ship.name + (" - %f s" % dt)] = evasiveManouvre(ship, speed, angle, dt=dt, reduceMemory=False)

    plotScatter("Effect of varying dt", testResults, "time", "passingDistance", "timestep")

if "random" in tests:
    generalResult = {"TC": {}}
    generalResult["TC"] = {
        "time": [],
        "distance": [],
        "passingDistance": [],
        "advance": []
    }

    for ship in shipList:
        testResults[ship.name] = {}
        numberOfTests = 1500


        for i in range(1, numberOfTests):
            angle = random.randint(5, 80)
            speed = random.randint(50, 250) / 10

            result_EM = evasiveManouvre(ship, speed, angle)

            if result_EM is None:
                print("%s - Test %d failed - speed: %d kn, course angle: %d deg" % (ship.name, i, speed, angle))
                del result_EM
            else:
                result_TC = turningCirlce(ship, speed)
                result = {**result_EM, **result_TC}

                testResults[ship.name]["%s - Test %d - startSpeed: %d kn| angle deg: %d" % (ship.name, i, speed, angle)] = result
                print("%s - Test %d - startSpeed: %d kn| angle deg: %d" % (ship.name, i, speed, angle))

                del result_EM, result_TC, result

        plotScatter("%s %d time passing distance start speed" % (ship.name, numberOfTests), testResults[ship.name], "time", "passingDistance", "startSpeed")
        plotScatter("%s %d distance passing distance start speed" % (ship.name, numberOfTests), testResults[ship.name], "distance", "passingDistance", "startSpeed")
        plotScatter("%s %d time passing distance course change" % (ship.name, numberOfTests), testResults[ship.name], "time", "passingDistance", "courseChange")
        plotScatter("%s %d distance passing distance course change" % (ship.name, numberOfTests), testResults[ship.name], "distance", "passingDistance", "courseChange")

        plotScatter("%s %d speed passing distance time" % (ship.name, numberOfTests), testResults[ship.name], "startSpeed", "passingDistance", "time")
        plotScatter("%s %d speed passing distance distance travelled" % (ship.name, numberOfTests), testResults[ship.name], "startSpeed", "passingDistance", "distance")

        for test in testResults[ship.name]:
            generalResult["TC"]["time"].append(testResults[ship.name][test]["time"])
            generalResult["TC"]["distance"].append(testResults[ship.name][test]["distance"])
            generalResult["TC"]["passingDistance"].append(testResults[ship.name][test]["passingDistance"])
            generalResult["TC"]["advance"].append(testResults[ship.name][test]["advance"])

        plt.close('all')

    plotScatter("%d distsance passing distance advance" % numberOfTests, generalResult, "distance", "passingDistance", "advance")
    plotScatter("%d time passing distance advance" % numberOfTests, generalResult, "time", "passingDistance", "advance")

# Show plots
plt.show()
