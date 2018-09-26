from src.MTexperiment.manoeuvreTests import *
from src.MTexperiment.plotResults import *
from src.MTexperiment.createShips import createShips

import random

# Create ships
[shipList, Tanker, Tug, EmmaMaersk, Astrorunner, CF7200, Anglia] = createShips()

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
tests = ["random"]

if "sea-trial" in tests:
    for ship in shipList:
        speed = ship.vmean

        results = seatrial(ship, speed, trialsList=['zigzag - 10:10', 'zigzag - 20:20'], printResult=True, reduceMemory=False)
        testResults[ship.name] = results
        plotPath("Paths-from-zig-zag-tests", testResults[ship.name])

        results = seatrial(ship, speed, trialsList=['turning circle - 35'], printResult=True, reduceMemory=False)
        testResults[ship.name] = results
        plotPath("Paths-from-turning-circle", testResults[ship.name])

if "turning-circle" in tests:
    for ship in [Tanker]:
        speed = ship.vmean

        results = seatrial(ship, speed, trialsList=['turning circle - 35'], printResult=True, reduceMemory=False)
        testResults[ship.name] = results
        plotPath("Paths-from-turning-circle", testResults[ship.name])
        plotLinesOverTime("Tug", results,
                          ["Rudder real", "Speed", "Acceleration*100", "Drift"])


if "Rudder-test" in tests:
    for ship in [Astrorunner]:#, CF7200, EmmaMaersk, Astrorunner]:
        speed = ship.vmean
        angle = 20
        dt = 0.01

        print("Evasive manoeuvre to %d degrees with %s (%d kn)" % (angle, ship.name, speed))
        testResults[ship.name + ("%2d" % angle)] = evasiveManouvre(ship, speed, angle, dt=dt, reduceMemory=False)
        plotLinesOverTime("Evasive-manoeuvre-%d-degrees-%s-(%d-kn)" % (angle, ship.name, speed), testResults, ["Course", "Heading", "Rudder", "Rudder real", "Speed", "Acceleration*100", "Drift"])

        print("Zig-zag 10:10 with %s (%d kn)" % (ship.name, speed))
        results = seatrial(ship, speed, trialsList=['zigzag - 10:10'], printResult=False, reduceMemory=False)
        plotLinesOverTime("Zig-zag-10-10-%s-(%d-kn)" % (ship.name, speed), results, ["Course", "Heading", "Rudder", "Rudder real", "Speed", "Acceleration*100", "Drift"])

        print("Zig-zag 20:20 with %s (%d kn)" % (ship.name, speed))
        results = seatrial(ship, speed, trialsList=['zigzag - 20:20'], printResult=False, reduceMemory=False)
        plotLinesOverTime("Zig-zag-20-20-%s-(%d-kn)" % (ship.name, speed), results, ["course", "heading", "rudder", "rudderReal", "speed", "acceleration*100", "drift"])

        print("Turning cirlce with %s (%d kn)" % (ship.name, speed))
        results = seatrial(ship, speed, trialsList=['turning circle - 35'], printResult=False, reduceMemory=False)
        plotLinesOverTime("Turning-circle-%s-(%d-kn)" % (ship.name, speed), results, ["Rudder", "Rudder real", "Speed", "Acceleration*100", "Drift"])

if "angle" in tests:
    for ship in [Tanker, Tug]:
        speed = ship.vmean
        for angle in [5, 10, 20, 30, 45, 90]:
           testResults[ship.name + (" - %d deg" % angle)] = evasiveManouvre(ship, speed, angle, reduceMemory=False)

    plotPath("Paths for different course change angles", testResults)

if "changetime" in tests:
    createPlot("Changetime-test")
    for changetime in [10, 12, 15, 17, 18, 19, 20, 21, 22, 24]:
        criteria = []
        time = []

        for ship in [Astrorunner, Tanker, EmmaMaersk]:
            speed = ship.vmean
            angle = 20

            result = evasiveManouvre(ship, speed, angle, changetime=changetime, reduceMemory=False)
            if result is None:
                print("%s - test failed, change time: %d" % (ship.name, changetime))
            else:
                testResults[ship.name + (" - %d s" % changetime)] = result

                criteria.append(-min(result["locx"]) / max(result["locy"]))
                time.append(result["Time"])

                print("%s with changetime: %d s. The max course is: %2.2f and heading: %2.2f. Manoeuvrer takes %d s (%d, %d)" % (ship.name, changetime, -min(result["Course"]), -min(result["Heading"]), result["Time"], -min(result["locx"]), max(result["locy"])))

        plt.scatter(time, criteria, label="%d seconds" % changetime)

    plt.legend()
    plt.xlabel("Time (seconds)")
    plt.ylabel("X/Y")
    storePlot("Changetime-test")


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

    plotScatter("Effect of others speed on time to decide", testResults, "Time", "Passing distance", "Speed other")

if "dt" in tests:
    for ship in [Tanker, Tug]:
        speed = ship.vmean
        angle = 20
        for dt in [0.001, 0.01, 0.1, 0.25, 1]:
           testResults[ship.name + (" - %f s" % dt)] = evasiveManouvre(ship, speed, angle, dt=dt, reduceMemory=False)

    plotScatter("Effect of varying dt", testResults, "Time", "Passing distance", "Timestep")

if "random" in tests:
    numberOfTests = 150
    generalResult = {"TC": {}}
    generalResult["TC"] = {
        "Time": [],
        "Distance": [],
        "Passing distance": [],
        "Advance": []
    }

    for ship in [Astrorunner]:
        testResults[ship.name] = {}

        for i in range(1, numberOfTests):
            angle = random.randint(5, 85)
            speed = random.randint(50, ship.vmax*10) / 10

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

        plotScatter("%s %d time passing distance start speed" % (ship.name, numberOfTests), testResults[ship.name], "Time", "Passing distance", "Start speed")
        plotScatter("%s %d distance passing distance start speed" % (ship.name, numberOfTests), testResults[ship.name], "Distance", "Passing distance", "Start speed")
        plotScatter("%s %d time passing distance course change" % (ship.name, numberOfTests), testResults[ship.name], "Time", "Passing distance", "Course change")
        plotScatter("%s %d distance passing distance course change" % (ship.name, numberOfTests), testResults[ship.name], "Distance", "Passing distance", "Course change")

        plotScatter("%s %d speed passing distance time" % (ship.name, numberOfTests), testResults[ship.name], "Start speed", "Passing distance", "Time")
        plotScatter("%s %d speed passing distance distance travelled" % (ship.name, numberOfTests), testResults[ship.name], "Start speed", "Passing distance", "Distance")

        for test in testResults[ship.name]:
            generalResult["TC"]["Time"].append(testResults[ship.name][test]["Time"])
            generalResult["TC"]["Distance"].append(testResults[ship.name][test]["Distance"])
            generalResult["TC"]["Passing distance"].append(testResults[ship.name][test]["Passing distance"])
            generalResult["TC"]["Advance"].append(testResults[ship.name][test]["Advance"])

        plt.close('all')

    plotScatter("%d distsance passing distance advance" % numberOfTests, generalResult, "Distance", "Passing distance", "Advance")
    plotScatter("%d time passing distance advance" % numberOfTests, generalResult, "Time", "Passing distance", "Advance")

# Show plots
plt.show()
