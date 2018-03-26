class Simulation:
    """ The class in which the simulation is created """

    activeShips = {}

    def __init__(self, world):
        self.world = world
        self.env = world.env

        self.addObjects()

        self.env.run(until=100)

    def addDynamicObject(self, objectName, location, course_deg, speed=None):
        ship = self.world.do[objectName]

        ship.location = location
        ship.course = course_deg

        if speed is None:
            ship.speed = ship.vmean
        else:
            ship.speed = speed

        ship.AIS.update(ship, time=self.env.now)

        self.activeShips[objectName] = ship

    def addObjects(self):
        self.addDynamicObject("Tanker", [0, 0], 0, 7)
        self.addDynamicObject("Bibby", [8000, 10000], 223)
        self.addDynamicObject("Bulk", [-8000, 5000], 85)
        yield
