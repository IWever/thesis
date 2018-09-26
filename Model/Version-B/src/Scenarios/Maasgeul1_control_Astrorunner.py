def initial(simulation):
    simulation.addDynamicObject("Tanker", [-1372, -1377], 98, speed=7.8, rudderAngle=-35)
    simulation.addDynamicObject("Astrorunner", [-3090, 1395], 114, speed=13.4)
    simulation.addDynamicObject("Anglia", [3000, -550], 291, speed=10.3)

    simulation.world.do["Tanker"].waypoints.append([-550, -1000])
    simulation.world.do["Tanker"].waypoints.append([-3000, 1300])

    simulation.world.do["Anglia"].waypoints.append([500, 600])
    simulation.world.do["Anglia"].waypoints.append([-3800, 2150])

    simulation.world.mapLocation = [-4000, 3200, -1900, 2500]

    #simulation.world.mapName = "Maasgeul-map"

    Maasvlakte1 = [
        (-500, -2500),
        (-325, -1800),
        (-132, -1230),
        (0, -660),
        (325, -460),
        (850, -720),
        (880, -820),
        (2110, -1400),
        (2300, -1800),
        (2200, -2500)]
    simulation.world.so["Maasvlakte1"] = simulation.createLandPatch(Maasvlakte1)

    Maasvlakte2 = [
        (-4000, 0),
        (-2000, -780),
        (-1425, -450),
        (-1000, -1150),
        (-750, -650),
        (-940, -100),
        (-3500, 1170),
        (-4000, 1400),
        (-6000, 1400),
        (-6000, 500)]
    simulation.world.so["Maasvlakte2"] = simulation.createLandPatch(Maasvlakte2)

    Noordkade = [
        (1700, 2600),
        (0, 1160),
        (-3070, 2180),
        (-3080, 2140),
        (1030, 680),
        (2120, 140),
        (2900, -370),
        (4000, -680),
        (4000, 3000),
        (2200, 3000)]
    simulation.world.so["Noordkade"] = simulation.createLandPatch(Noordkade)

    Zuidkade = [
        (-1200, -2500),
        (-1180, -2270),
        (-1375, -1650),
        (-4500, -2000),
        (-5000, -1560),
        (-4650, -1000),
        (-4100, -1200),
        (-3285, -1500),
        (-2800, -1400),
        (-2800, -1070),
        (-4100, -600),
        (-6000, -350),
        (-6000, -2500)]
    simulation.world.so["Zuidkade"] = simulation.createLandPatch(Zuidkade)

    Pier = [
        (-825, 710),
        (-815, 775),
        (2080, -400),
        (2900, -1050),
        (4000, -1400),
        (4000, -2000),
        (2900, -1400),
        (1870, -523)]
    simulation.world.so["Pier"] = simulation.createLandPatch(Pier)