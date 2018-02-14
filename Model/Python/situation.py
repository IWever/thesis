import math
import matplotlib.pyplot as plt
import numpy as np

class Map(object):

    """ The situation where everything happens:"""

    vessels = []
    screensize = 40000

    def __init__(self):
        pass

    def addShip(self, ship, speed_kn, course_deg, locationX, locationY):
        """ Add ship to map

        Args:
            ship: ship object which is created previously
            speed_kn: current speed of vessel, input [knots], stored in [m/s]
            course_deg: direction relative to north [degrees], stored in [rad]
            locationX: X coordinate in [m]
            locationY: Y coordinate in [m]
        """

        self.vessels.append(ship)
        ship.speed = speed_kn * 1852 / 3600
        ship.course = math.pi * course_deg / 180
        ship.location = [locationX, locationY]

    def updateSituation(self, timestep, ownship):
        for ship in self.vessels:
            ship.updateLocation(timestep, ownship)

        self.updateMap()

    def updateMap(self):
        """ Plot vessels """

        plt.figure('Map')
        plt.cla()
        plt.axes().set_aspect('equal')
        plt.xlim(-self.screensize / 2, self.screensize / 2)
        plt.ylim(-self.screensize / 2, self.screensize / 2)

        # plt.imshow(map,
        #            cmap='RdYlGn',
        #            interpolation='nearest',
        #            extent=[-20000, 20000, -20000, 20000],
        #            alpha=0.4)

        for ship in self.vessels:
            plt.plot(ship.location[0], ship.location[1],  marker='o')
            plt.text(ship.location[0], ship.location[1],  ship.name)

            if ship.speed != 0:
                plt.quiver(ship.location[0],
                           ship.location[1],
                           ship.speed * math.sin(ship.course),
                           ship.speed * math.cos(ship.course))

    def createMap(self):
        """ Initialize plot """
        plt.ion()
        plt.show()

        self.updateMap()

    def runSimulation(self, stepsize, ownship):
        self.createMap()
        time_elapsed = 0

        while plt.fignum_exists('Map'):
            self.updateSituation(stepsize, ownship)
            time_elapsed += stepsize
            plt.text(-20000, 20500, 'Time elapsed: %d minutes' % (time_elapsed / 60))
            plt.pause(0.0001)

        print('Stopped simulation by closing map')
