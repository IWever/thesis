import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Map(object):

    """ The situation where everything happens:"""

    vessels = []

    def __init__(self, screensize=40000):
        self.screensize = screensize
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

        plt.figure('Map')
        plt.cla()
        self.updateMap()

    def updateMap(self):
        """ Plot vessels """
        plt.figure('Map')
        plt.axes().set_aspect('equal')
        plt.xlim(-self.screensize / 2, self.screensize / 2)
        plt.ylim(-self.screensize / 2, self.screensize / 2)

        for ship in self.vessels:
            plt.plot(ship.location[0], ship.location[1],  marker='o')
            plt.text(ship.location[0], ship.location[1],  ship.name)

            if ship.speed != 0:
                plt.quiver(ship.location[0],
                           ship.location[1],
                           600 * ship.speed * math.sin(ship.course),
                           600 * ship.speed * math.cos(ship.course),
                           units='xy',
                           scale=1)

    def createMap(self):
        """ Initialize plot """
        plt.figure('Map')
        plt.ion()
        plt.show()

        self.updateMap()

    def runSimulation(self, ownship, timestep=10, positionPrediction=True, predictionTimer=1000):
        """ Run simulation of current situation with specified timestep"""
        self.createMap()
        time_elapsed = 0

        while plt.fignum_exists('Map'):
            self.updateSituation(timestep, ownship)
            if positionPrediction:
                self.positionPrediction(predictionTimer)

            time_elapsed += timestep
            plt.text(-self.screensize / 2, self.screensize * 0.5125,
                     'Time elapsed: %d minutes' % (time_elapsed / 60))
            plt.pause(0.0001)

        print('Stopped simulation by closing map')

    def positionPrediction(self, time=600):
        x = np.empty(0)
        y = np.empty(0)

        for ship in self.vessels:
            xi, yi = ship.possiblePositions(time)
            x = np.concatenate((x, xi))
            y = np.concatenate((y, yi))

        # sns.kdeplot(x, y, shade=True, shade_lowest=False)
        self.updateMap()
