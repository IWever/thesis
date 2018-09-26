def initial(simulation):
    # Dynamic objects
    simulation.addDynamicObject("Tanker", [-1400, -1400], 45, speed=16, rudderAngle=0)
    simulation.addDynamicObject("Astrorunner", [3250, 0], 278, speed=15.2, rudderAngle=0)
    simulation.addDynamicObject("EmmaMaersk", [400, 2400], 225, speed=12, rudderAngle=0)

    simulation.world.do["Tanker"].waypoints.append([230, -50])
    simulation.world.do["Astrorunner"].waypoints.append([0, 400])


    # Static objects
    separationZonePolygon = [
        (2670, -350),
        (1300, -550),
        (560, -1900),
        (0, -3000),
        (5000, -3000),
        (5000, -1000)]
    simulation.world.so["Traffic separation"] = simulation.createDangerPatch(separationZonePolygon)

    separationSchemeSouth = [
        (-11000, -12000),
        (9000, 8000)
    ]
    simulation.world.so["Seperation scheme south"] = simulation.createDangerLinePatch(separationSchemeSouth)

    separationSchemeNorth = [
        (-11000, -10000),
        (9000, 10000)
    ]
    simulation.world.so["Seperation scheme north"] = simulation.createDangerLinePatch(separationSchemeNorth)

    # Initial view
    simulation.world.mapLocation = [-3500, 3500, -2000, 2000]



