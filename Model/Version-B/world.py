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
            self.staticObjects = []

        if dynamicObjects:
            self.dynamicObjects = shipList
        if simulation:
            self.env = simpy.Environment()
            self.sim = Simulation(self)

        if viewer:
            self.root = tk.Tk()
            self.viewer = Viewer(self)


world = World()
