from src.MTexperiment.manoeuvreTests import *
from src.MTexperiment.plotResults import *
from src.MTexperiment.createShips import createShips
from src.MTexperiment.general import saveResult
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
tests = ["Random"]

for testname in tests:
    print("---------------------------------")
    print(testname)
    print("---------------------------------")

if "sea-trial" in tests:
    for test in [[Astrorunner, 14.7], [Tanker, 15], [EmmaMaersk, 12]]:
        ship = test[0]
        speed = test[1]

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
                          ["Rudder real [degrees]", "Speed [knots]", "Acceleration*100 [m/s^2]", "Drift [degrees]"])


if "Rudder-test" in tests:
    for ship in [Astrorunner]:#, CF7200, EmmaMaersk, Astrorunner]:
        speed = ship.vmean
        evasiveAngle = 20
        dt = 0.01

        print("Evasive manoeuvre to %d degrees with %s (%d kn)" % (evasiveAngle, ship.name, speed))
        testResults[ship.name + ("%2d" % evasiveAngle)] = evasiveManouvre(ship, speed, evasiveAngle, dt=dt, reduceMemory=False)
        plotLinesOverTime("Evasive-manoeuvre-%d-degrees-%s-(%d-kn)" % (evasiveAngle, ship.name, speed), testResults, ["Course [degrees]", "Heading [degrees]", "Rudder [degrees]", "Rudder real [degrees]", "Speed [knots]", "Acceleration*100 [m/s^2]", "Drift [degrees]"])

        print("Zig-zag 10:10 with %s (%d kn)" % (ship.name, speed))
        results = seatrial(ship, speed, trialsList=['zigzag - 10:10'], printResult=False, reduceMemory=False)
        plotLinesOverTime("Zig-zag-10-10-%s-(%d-kn)" % (ship.name, speed), results, ["Course [degrees]", "Heading [degrees]", "Rudder [degrees]", "Rudder real [degrees]"])

        print("Zig-zag 20:20 with %s (%d kn)" % (ship.name, speed))
        results = seatrial(ship, speed, trialsList=['zigzag - 20:20'], printResult=False, reduceMemory=False)
        plotLinesOverTime("Zig-zag-20-20-%s-(%d-kn)" % (ship.name, speed), results, ["Course [degrees]", "Heading [degrees]", "Rudder [degrees]", "Rudder real [degrees]"])

        print("Turning cirlce with %s (%d kn)" % (ship.name, speed))
        results = seatrial(ship, speed, trialsList=['turning circle - 35'], printResult=False, reduceMemory=False)
        plotLinesOverTime("Turning-circle-%s-(%d-kn)" % (ship.name, speed), results, ["Rudder [degrees]", "Rudder real [degrees]", "Speed [knots]", "Acceleration*100 [m/s^2]", "Drift [degrees]"])

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
                time.append(result["Time [seconds]"])

                print("%s with changetime: %d s. The max course is: %2.2f and heading: %2.2f. Manoeuvrer takes %d s (%d, %d)" % (ship.name, changetime, -min(result["Course [degrees]"]), -min(result["Heading [degrees]"]), result["Time [seconds]"], -min(result["locx"]), max(result["locy"])))

        plt.scatter(time, criteria, label="%d seconds" % changetime)

    plt.legend()
    plt.xlabel("Time [seconds]")
    plt.ylabel("Y/X")
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

    plotScatter("Effect of others speed on time to decide", testResults, "Time [seconds]", "Passing distance [meter]", "Speed other [knots]")

if "timestep" in tests:
    for ship in [Tanker, Astrorunner, EmmaMaersk]:
        speed = ship.vmean
        angle = 20
        for dt in [0.00001, 0.001, 0.01, 0.1, 0.25, 1]:
            testResults[ship.name + (" - %f s" % dt)] = evasiveManouvre(ship, speed, angle, dt=dt, reduceMemory=True)
            result = testResults[ship.name + (" - %f s" % dt)]
            print(ship.name + (" - %f s" % dt))
            print(result['Timestep [seconds]'])
            print(result['Time [seconds]'])
            print(result['Passing distance [meter]'])
            print(result['Max course [degrees]'])


    plotScatter("Effect of varying dt", testResults, "Time [seconds]", "Passing distance [meter]", "Timestep [seconds]")

if "Random" in tests:
    numberOfTests = 3000
    changeTimeIn = 0
    generalResult = {"TC": {}}
    generalResult["TC"] = {
        "Simulation": "Random",
        "Time [seconds]": [],
        "Distance till initial CPA [meter]": [],
        "Passing distance [meter]": [],
        "Advance distance [meter]": [],
        "CPA [meter]": [],
        "Max course [degrees]": [],
        "Start speed [knots]": [],
        "Speed other [knots]": [],
        "Shipname": []

    }

    for ship in [Astrorunner, Tanker, EmmaMaersk]:
        testResults[ship.name] = {}

        for i in range(1, numberOfTests):
            angle = random.randint(5, 70)
            speed = random.randint(50, ship.vmax*10) / 10

            result_EM = evasiveManouvre(ship, speed, angle, changetime=changeTimeIn, printResult=False)

            if result_EM is None:
                print("%s - Test %d - Startspeed: %2.1f kn| angle: %d deg | failed " % (ship.name, i, speed, angle))
                del result_EM
            else:
                result_TC = turningCirlce(ship, speed)
                result = {**result_EM, **result_TC}

                testResults[ship.name]["%s - Test %d - startSpeed: %2.1f kn| angle deg: %d" % (ship.name, i, speed, angle)] = result
                print("%s - Test %d - Startspeed: %2.1f kn| angle: %d deg | Max angle: %2.1f deg | Passing distance: %d m" % (ship.name, i, speed, angle, result["Max course [degrees]"], result["Passing distance [meter]"]))

                del result_EM, result_TC, result


        plotScatter("%s %d distance passing distance start speed" % (ship.name, numberOfTests), testResults[ship.name], "Distance till initial CPA [meter]", "Passing distance [meter]", "Start speed [knots]", save=True)
        plotScatter("%s %d distance CPA start speed" % (ship.name, numberOfTests), testResults[ship.name], "Distance till initial CPA [meter]", "CPA [meter]", "Start speed [knots]", save=True)

        for test in testResults[ship.name]:
            generalResult["TC"]["Time [seconds]"].append(testResults[ship.name][test]["Time [seconds]"])
            generalResult["TC"]["Distance till initial CPA [meter]"].append(testResults[ship.name][test]["Distance till initial CPA [meter]"])
            generalResult["TC"]["Passing distance [meter]"].append(testResults[ship.name][test]["Passing distance [meter]"])
            generalResult["TC"]["Advance distance [meter]"].append(testResults[ship.name][test]["Advance distance [meter]"])
            generalResult["TC"]["CPA [meter]"].append(testResults[ship.name][test]["CPA [meter]"])
            generalResult["TC"]["Max course [degrees]"].append(testResults[ship.name][test]["Max course [degrees]"])
            generalResult["TC"]["Start speed [knots]"].append(testResults[ship.name][test]["Start speed [knots]"])
            generalResult["TC"]["Speed other [knots]"].append(testResults[ship.name][test]["Speed other [knots]"])
            generalResult["TC"]["Shipname"].append(testResults[ship.name][test]["Shipname"])

        #plt.close('all')

    plotScatter("%d distance passing distance advance" % numberOfTests, generalResult, "Distance till initial CPA [meter]", "Passing distance [meter]", "Advance distance [meter]")
    plotScatter("%d distance CPA advance" % numberOfTests, generalResult, "Distance till initial CPA [meter]", "CPA [meter]", "Advance distance [meter]")

    # Save result
    saveResult(generalResult)

if "Advance" in tests:
    numberOfTests = 50
    generalResult = {"TC": {}}
    generalResult["TC"] = {
        "Simulation": "Advance",
        "Time [seconds]": [],
        "Distance till initial CPA [meter]": [],
        "Passing distance [meter]": [],
        "Advance distance [meter]": [],
        "CPA [meter]": [],
        "Max course [degrees]": [],
        "Max rudder [degrees]": [],
        "Start speed [knots]": [],
        "Speed other [knots]": [],
        "Shipname": []
    }
    for ship, speed, amplificationFactor in [(EmmaMaersk, 12, 3.5), (EmmaMaersk, 12, 2.5), (Tanker, 15, 3.5), (Tanker, 15, 2.5), (Astrorunner, 14.7, 2.5), (Astrorunner, 14.7, 3.5)]:
        testResults[ship.name] = {}
        ship.rudderAmplificationFactor = amplificationFactor

        for angle in range(5, 65, 2):
            i = angle
            rudder = 35
            result_EM = evasiveManouvre(ship, speed, angle, changetime=0)

            if result_EM is None:
                print("%s - Test %d - AF: %2.1f | Startspeed: %2.1f kn| angle: %d deg | rudder: %d deg | failed " % (ship.name, i, amplificationFactor, speed, angle, rudder))
                del result_EM
            else:
                result_TC = turningCirlce(ship, speed)
                result = {**result_EM, **result_TC}

                testResults[ship.name]["%s - Test %d - startSpeed: %2.1f kn| angle deg: %d" % (ship.name, i, speed, angle)] = result
                print("%s - Test %d - AF: %2.1f | Startspeed: %2.1f kn| angle: %d deg | rudder: %d deg  | Max angle: %2.1f deg | Advance: %d m | Passing distance: %d m | CPA %d m | DTICPA: %d meter" % (ship.name, i, amplificationFactor, speed, angle, rudder, result["Max course [degrees]"], result["Advance distance [meter]"], result["Passing distance [meter]"], result["CPA [meter]"], result["Distance till initial CPA [meter]"]))

                del result_EM, result_TC, result

        plotScatter("%s %d distance CPA start speed" % (ship.name, numberOfTests), testResults[ship.name], "Distance till initial CPA [meter]", "CPA [meter]", "Start speed [knots]", save=True)
        plotScatter("%s %d time CPA course change" % (ship.name, numberOfTests), testResults[ship.name], "Time [seconds]", "CPA [meter]", "Max course [degrees]", save=True)

        for test in testResults[ship.name]:
            generalResult["TC"]["Time [seconds]"].append(testResults[ship.name][test]["Time [seconds]"])
            generalResult["TC"]["Distance till initial CPA [meter]"].append(testResults[ship.name][test]["Distance till initial CPA [meter]"])
            generalResult["TC"]["Passing distance [meter]"].append(testResults[ship.name][test]["Passing distance [meter]"])
            generalResult["TC"]["Advance distance [meter]"].append(testResults[ship.name][test]["Advance distance [meter]"])
            generalResult["TC"]["CPA [meter]"].append(testResults[ship.name][test]["CPA [meter]"])
            generalResult["TC"]["Max course [degrees]"].append(testResults[ship.name][test]["Max course [degrees]"])
            generalResult["TC"]["Start speed [knots]"].append(testResults[ship.name][test]["Start speed [knots]"])
            generalResult["TC"]["Speed other [knots]"].append(testResults[ship.name][test]["Speed other [knots]"])
            generalResult["TC"]["Shipname"].append(testResults[ship.name][test]["Shipname"])
            generalResult["TC"]["Max rudder [degrees]"].append(testResults[ship.name][test]["Max rudder [degrees]"])


    plotScatter("%d distance CPA advance" % numberOfTests, generalResult, "Distance till initial CPA [meter]", "CPA [meter]", "Advance distance [meter]")
    plotScatter("%d distance CPA start speed" % numberOfTests, generalResult, "Distance till initial CPA [meter]", "CPA [meter]", "Start speed [knots]")
    plotScatter("%d time CPA advance" % numberOfTests, generalResult, "Time [seconds]", "CPA [meter]", "Advance distance [meter]")
    plotScatter("%d distance advance start speed" % numberOfTests, generalResult, "Distance till initial CPA [meter]", "Advance distance [meter]", "Start speed [knots]")
    plotScatter("%d distance advance CPA" % numberOfTests, generalResult, "Distance till initial CPA [meter]", "Advance distance [meter]", "CPA [meter]")
    plotScatter("%d distance passing distance advance" % numberOfTests, generalResult, "Distance till initial CPA [meter]", "Passing distance [meter]", "Advance distance [meter]")
    plotScatter("%d time passing distance advance" % numberOfTests, generalResult, "Time [seconds]", "Passing distance [meter]", "Advance distance [meter]")



    # Save result
    saveResult(generalResult)

if "Course" in tests:
    numberOfTests = 50
    generalResult = {"TC": {}}
    generalResult["TC"] = {
        "Simulation": "Speed-other",
        "Time [seconds]": [],
        "Distance till initial CPA [meter]": [],
        "Passing distance [meter]": [],
        "Advance distance [meter]": [],
        "CPA [meter]": [],
        "Max course [degrees]": [],
        "Start speed [knots]": [],
        "Speed other [knots]": [],
        "Shipname": []
    }
    for ship in [Tanker, Astrorunner, EmmaMaersk]:
        testResults[ship.name] = {}
        for i in range(1, numberOfTests+1):
            testSpeedOther = 14#random.triangular(0, 18, 12)

            angle = random.randint(5, 80)
            speed = ship.vmean #random.triangular(50, ship.vmax*10, 9*ship.vmax) / 10

            result_EM = evasiveManouvre(ship, speed, angle, changetime=0, speedOther=testSpeedOther)

            if result_EM is None:
                print("%s - Test %d - Startspeed: %2.1f kn| angle: %d deg | failed " % (ship.name, i, speed, angle))
                del result_EM
            else:
                result_TC = turningCirlce(ship, speed)
                result = {**result_EM, **result_TC}

                testResults[ship.name]["%s - Test %d - startSpeed: %2.1f kn| angle deg: %d" % (ship.name, i, speed, angle)] = result
                print("%s - Test %d - Startspeed: %2.1f kn| angle: %d deg | Max angle: %2.1f deg | Passing distance: %d m | CPA %d m" % (ship.name, i, speed, angle, result["Max course [degrees]"], result["Passing distance [meter]"], result["CPA [meter]"]))

                del result_EM, result_TC, result

        #plotScatter("%s %d distance passing distance start speed" % (ship.name, numberOfTests), testResults[ship.name], "Distance till initial CPA [meter]", "Passing distance [meter]", "Start speed [knots]", save=True)
        plotScatter("%s %d distance CPA angle" % (ship.name, numberOfTests), testResults[ship.name], "Distance till initial CPA [meter]", "CPA [meter]", "Max course [degrees]", save=True)


        for test in testResults[ship.name]:
            generalResult["TC"]["Time [seconds]"].append(testResults[ship.name][test]["Time [seconds]"])
            generalResult["TC"]["Distance till initial CPA [meter]"].append(testResults[ship.name][test]["Distance till initial CPA [meter]"])
            generalResult["TC"]["Passing distance [meter]"].append(testResults[ship.name][test]["Passing distance [meter]"])
            generalResult["TC"]["Advance distance [meter]"].append(testResults[ship.name][test]["Advance distance [meter]"])
            generalResult["TC"]["CPA [meter]"].append(testResults[ship.name][test]["CPA [meter]"])
            generalResult["TC"]["Max course [degrees]"].append(testResults[ship.name][test]["Max course [degrees]"])
            generalResult["TC"]["Start speed [knots]"].append(testResults[ship.name][test]["Start speed [knots]"])
            generalResult["TC"]["Speed other [knots]"].append(testResults[ship.name][test]["Speed other [knots]"])
            generalResult["TC"]["Shipname"].append(testResults[ship.name][test]["Shipname"])

    plotScatter("%d distsance CPA course" % numberOfTests, generalResult, "Distance till initial CPA [meter]", "CPA [meter]", "Max course [degrees]", save=True)
    #plotScatter("%d time passing distance advance" % numberOfTests, generalResult, "Time [seconds]", "Passing distance [meter]", "Speed other [knots]")

    # Save result
    saveResult(generalResult)

# Show plots
plt.show()

