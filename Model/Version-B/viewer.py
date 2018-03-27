from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import seaborn as sns

import math

class Viewer:
    """ The class in which the viewer for representing the simulation will be created"""

    def __init__(self, world):

        # Initial creation and import of world
        self.world = world
        self.root = world.root
        self.root.title(world.name)

        # Create variables
        self.message = StringVar()
        self.time = StringVar()
        self.scale = 12
        self.shipLocationMarkers = None

        # Created Frames
        self.createInfoBar()
        self.createPlottingCanvas()
        self.createSidebar()

        # Run the GUI
        print("Created GUI screen")
        self.plotShips()

    def createInfoBar(self):
        self.message.set("Let it sail")

        self.infoBar = Frame(self.root)
        self.infoBar.pack(side=BOTTOM, fill=X, expand=FALSE)
        self.infoLabel = Label(self.infoBar, textvariable=self.message)
        self.infoLabel.pack()

    def createPlottingCanvas(self):
        self.mapViewer = Frame(self.root)
        self.mapViewer.pack(side=LEFT, fill=BOTH, expand=True)

        self.mapFigure = Figure()

        self.mapPlot = self.mapFigure.add_subplot(111, adjustable='box', aspect=1)
        self.mapPlot.axis([-self.scale * 650, self.scale * 650, -self.scale * 500, self.scale * 500])

        self.mapViewer.winfo_height()

        self.mapCanvas = FigureCanvasTkAgg(self.mapFigure, master=self.mapViewer)

        self.mapCanvas.show()
        self.mapCanvas.get_tk_widget().pack(fill=BOTH, expand=TRUE)

        self.plotControls = NavigationToolbar2TkAgg(self.mapCanvas, self.infoBar)
        self.plotControls.pack(side=TOP, fill=X)

    def createSidebar(self):
        self.optionMenu = Frame(self.root)
        self.optionMenu.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        self.vesselList = Listbox(self.optionMenu)
        self.vesselList.pack(side=BOTTOM, fill=BOTH)

        self.timeLabel = Label(self.optionMenu, textvariable=self.time)
        self.timeLabel.pack(sid=TOP, fill=X)

        self.slider1 = Scale(self.optionMenu, from_=-20, to=20, orient=HORIZONTAL)
        self.slider1.pack(side=TOP, fill=X)
        self.slider2 = Scale(self.optionMenu, from_=-360, to=360, orient=HORIZONTAL)
        self.slider2.pack(side=TOP, fill=X)

        for vessel in self.world.do:
            self.vesselList.insert(END, vessel)

    def plotShips(self):
        # try:
        #     del self.shipLocations
        # except AttributeError:
        #     pass

        for shipname in self.world.sim.activeShips:

            ship = self.world.sim.activeShips[shipname]

            try:
                ship.marker.remove()
                ship.scalar.remove()
            except AttributeError:
                pass

            ship.marker = self.mapPlot.scatter(ship.location[0], ship.location[1], marker='o', color=ship.color)
            if ship.speed != 0:
                ship.scalar = self.mapPlot.quiver(ship.location[0],
                           ship.location[1],
                           10 * self.scale * ship.speed * math.sin(math.radians(ship.course)),
                           10 * self.scale * ship.speed * math.cos(math.radians(ship.course)),
                           units='xy',
                           scale=1)

    def updatePlot(self):
        self.plotShips()

        self.time.set("Time: %d" % self.world.env.now)

        self.mapCanvas.draw()
