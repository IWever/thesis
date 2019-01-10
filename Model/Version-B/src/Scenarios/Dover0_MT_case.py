def initial(simulation):
    # Dynamic objects
    simulation.addDynamicObject("Gulf Valour", [-100, -100], 45, speed=15, rudderAngle=0)
    simulation.addDynamicObject("Astrorunner", [3250, 0], 315, speed=14.7, rudderAngle=0)
    simulation.addDynamicObject("EmmaMaersk", [2800, 4300], 225, speed=12, rudderAngle=0)

    simulation.world.do["Gulf Valour"].waypoints.append([800, 800])
    simulation.world.do["Gulf Valour"].waypoints.append([1700, 900])
    simulation.world.do["Gulf Valour"].waypoints.append([3500, 2700])

    simulation.world.do["Astrorunner"].waypoints.append([1500, 1700])
    simulation.world.do["Astrorunner"].waypoints.append([1600, 2400])
    simulation.world.do["Astrorunner"].waypoints.append([0, 3000])

    # Static objects
    forbiddenZonePolygonSouth = [
        (2670, -350),
        (1300, -550),
        (560, -1900),
        (0, -3000),
        (5000, -3000),
        (5000, -1000)]
    simulation.world.so["Forbidden zone south"] = simulation.createDangerPatch(forbiddenZonePolygonSouth)

    forbiddenZonePolygonNorth = [
        (8000, 330),
        (5140, 100),
        (3475, 218),
        (2933, 740),
        (3051, 1415),
        (3782, 2306),
        (4509, 3000),
        (7200, 6000),
        (8000, 6000)]
    simulation.world.so["Forbidden zone north"] = simulation.createDangerPatch(forbiddenZonePolygonNorth)

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
    simulation.world.mapLocation = [-2500, 5200, -500, 3900]



