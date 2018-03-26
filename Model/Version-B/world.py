import tkinter as tk
import simpy
from simulation import Simulation
from viewer import Viewer
from dynamicObjects import shipList


class World:
    """ The world in which everything will happen """

    def __init__(self, name="Thesis tool", staticObjects=True, dynamicObjects=True, simulation=True, viewer=True):
        self.name = name

        if staticObjects:
            self.so = []

        if dynamicObjects:
            self.do = shipList
        if simulation:
            self.env = simpy.rt.RealtimeEnvironment(factor=0.1)
            self.sim = Simulation(self)

        if viewer:
            self.root = tk.Tk()
            self.viewer = Viewer(self)

# Create the world
world = World()
