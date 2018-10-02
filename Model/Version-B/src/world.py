import tkinter as tk
from tkinter import*
import simpy
from src.simulation import Simulation
from src.viewer import Viewer
from src.dynamicObjects import shipList
import datetime


class World:
    """ The world in which everything will happen """

    def __init__(self):

        # Set-up for world
        self.experimentName = "Dover1_control_Astrorunner"
        self.comment = "Test"
        self.showWaypointMarkers = False
        self.saveLog = False

        # Set-up for simulation
        self.mapName = None
        self.mapLocation = [-4000, 4000, -2500, 2500]  # [Xleft, Xright, Ybottom, Ytop]
        self.secondsPerStep = 8
        self.updateFrequency = 16  # amount of simulation steps per screen update

        # Initialization simulation
        self.simEnd = 10
        self.actionLog = []

        self.so = {}
        print("Created empty list to store static objects")

        self.do = shipList
        print("Stored database of ships in world")

        self.env = simpy.rt.RealtimeEnvironment(factor=1/self.secondsPerStep, strict=False)
        self.sim = Simulation(self)

        self.root = tk.Tk()
        #self.secondScreen = tk.Tk()
        self.viewer = Viewer(self)

    def runSimulation(self):
        try:
            simMinStep = 1
            while world.viewer.simulationRunning:
                self.simEnd += simMinStep
                world.env.run(until=self.simEnd)

            self.log("Simulation paused at %d seconds" % (self.simEnd - 1))

        except TclError:
            self.closeSimulation()

    def closeSimulation(self):
        for shipname in self.sim.activeShips:
            self.log("")
            ship = self.sim.activeShips[shipname]

            self.log("%s - CPA (meter)" % ship.name)
            for shipname in ship.perceivedShipCPA:
                self.log("%20s | %d meter" % (shipname, ship.perceivedShipCPA[shipname]))

        if self.saveLog:
            filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "_" + self.experimentName + "-" + self.comment
            with open("D:\ingma\OneDrive\Studie\Thesis\Model\Version-B\log\%s.txt" % filename, 'w') as f:
                for line in self.actionLog:
                    f.write("%s\n" % line)

        self.log("")
        self.log("Simulation closed by user after %d seconds" % (self.simEnd - 1))
        sys.exit()

    def log(self, message):
        print(message)
        self.actionLog.append("%d s: %s" % (self.env.now, message))


# Create the world
world = World()

# Run GUI and simulation
world.runSimulation()
world.root.mainloop()
