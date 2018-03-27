import tkinter as tk
from tkinter import*
import simpy
from simulation import Simulation
from viewer import Viewer
from dynamicObjects import shipList


class World:
    """ The world in which everything will happen """

    def __init__(self, name="Dutos ship sim"):
        self.name = name
        self.secondsPerStep = 8
        self.updateFrequency = 2

        self.so = []
        print("Created empty list to store static objects")

        self.do = shipList
        print("Stored database of ships in world")

        self.env = simpy.rt.RealtimeEnvironment(factor=1/self.secondsPerStep, strict=False)
        self.sim = Simulation(self)

        self.root = tk.Tk()
        self.viewer = Viewer(self)


# Create the world
world = World()

# Run GUI and simulation
try:
    world.env.run()
except RuntimeError:
    print('Simulation is too slow and stopped')
except TclError:
    print('Application closed by user')

world.root.mainloop()

