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
        self.selectedShip = None

        # Callbacks
        self.plotButtonPress = None

        # Created Frames
        self.createInfoBar()
        self.createPlottingCanvas()
        self.createSidebar()

        # Run the GUI
        print("Created GUI screen")
        self.updatePlot()

    def createInfoBar(self):
        self.message.set("Let it sail")

        self.infoBar = Frame(self.root)
        self.infoBar.pack(side=BOTTOM, fill=X, expand=FALSE)
        self.infoLabel = Label(self.infoBar, textvariable=self.message)
        self.infoLabel.pack()

    def createPlottingCanvas(self):
        sns.set()

        self.mapViewer = Frame(self.root)
        self.mapViewer.pack(side=LEFT, fill=BOTH, expand=True)

        self.mapFigure = Figure()

        self.mapPlot = self.mapFigure.add_subplot(111, adjustable='box', aspect=1)
        self.mapPlot.axis([-self.scale * 650, self.scale * 650, -self.scale * 500, self.scale * 500])

        self.mapCanvas = FigureCanvasTkAgg(self.mapFigure, master=self.mapViewer)
        self.mapCanvas.get_tk_widget().pack(fill=BOTH, expand=TRUE)
        self.mapCanvas.show()

        self.plotControls = NavigationToolbar2TkAgg(self.mapCanvas, self.infoBar)
        self.plotControls.pack(side=TOP, fill=X)

    def createSidebar(self):
        self.optionMenu = Frame(self.root)
        self.optionMenu.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        self.vesselList = Listbox(self.optionMenu, selectmode=SINGLE)
        self.vesselList.pack(side=BOTTOM, fill=BOTH)

        self.timeLabel = Label(self.optionMenu, textvariable=self.time)
        self.timeLabel.pack(side=TOP, fill=X)

        self.modifyShipButton = Button(self.optionMenu, text="Modify mode", command=self.modifyShipFromList)
        self.modifyShipButton.pack(side=TOP, fill=X)

        self.removeShipButton = Button(self.optionMenu, text="Remove ship from plot", command=self.removeShipFromPlot)
        self.speedSlider = Scale(self.optionMenu, from_=-20, to=20, orient=HORIZONTAL)
        self.courseSlider = Scale(self.optionMenu, from_=-180, to=360, orient=HORIZONTAL)


        for vessel in self.world.do:
            self.vesselList.insert(END, vessel)

    def updatePlot(self):
        for shipname in self.world.sim.activeShips:
            self.plotShip(shipname)
        self.time.set("Time: %d seconds" % self.world.env.now)
        self.mapCanvas.draw()

    def plotShip(self, shipname):
        ship = self.world.sim.activeShips[shipname]

        self.deleteShipPlotObjects(ship)

        ship.polygonPlot = ship.patchPolygon()
        self.mapPlot.add_patch(ship.polygonPlot)

        if ship.speed != 0:
            ship.scalarPlot = self.mapPlot.quiver(ship.location[0],
                                                  ship.location[1],
                                                  self.scale * ship.speed * math.sin(math.radians(ship.course)),
                                                  self.scale * ship.speed * math.cos(math.radians(ship.course)),
                                                  units='xy',
                                                  scale=.1)

        ship.markerPlot = self.mapPlot.scatter(ship.location[0], ship.location[1], marker='o', color=ship.color)
        ship.tag = self.mapPlot.text(ship.location[0], ship.location[1], shipname)

    @staticmethod
    def deleteShipPlotObjects(ship):
        try:
            ship.markerPlot.remove()
        except AttributeError:
            pass
        except ValueError:
            pass

        try:
            ship.scalarPlot.remove()
        except AttributeError:
            pass
        except ValueError:
            pass

        try:
            ship.polygonPlot.remove()
        except AttributeError:
            pass
        except ValueError:
            pass

        try:
            ship.tag.remove()
        except AttributeError:
            pass
        except ValueError:
            pass

    def modifyShipFromList(self):
        self.speedSlider.pack(side=TOP, fill=X)
        self.courseSlider.pack(side=TOP, fill=X)
        self.removeShipButton.pack(side=TOP, fill=X)
        self.modifyShipButton.configure(text="Back to viewer mode", command=self.quitModifyShip)
        self.vesselList.selection_clear(0, END)

        self.message.set("Use sliders or click new position to edit selected ship")

        self.vesselList.bind('<<ListboxSelect>>', self.shipSelectedToModify)
        self.speedSlider.bind("<ButtonRelease-1>", self.setSpeed)
        self.courseSlider.bind("<ButtonRelease-1>", self.setCourse)
        self.plotButtonPress = self.mapCanvas.mpl_connect('button_press_event', self.selectLocationForShip)

    def quitModifyShip(self):
        self.courseSlider.forget()
        self.speedSlider.forget()
        self.removeShipButton.forget()
        self.modifyShipButton.configure(text="Switch modify mode on", command=self.modifyShipFromList)

        self.message.set("Closed modify mode")

        self.vesselList.unbind('<<ListboxSelect>>')
        self.speedSlider.unbind("<ButtonRelease-1>")
        self.courseSlider.unbind("<ButtonRelease-1>")
        self.mapCanvas.mpl_disconnect(self.plotButtonPress)

    def shipSelectedToModify(self, event=None):
        self.selectedShip = self.vesselList.get(self.vesselList.curselection())
        ship = self.world.do[self.selectedShip]

        self.message.set("Modify %s using sliders and click for new location" % self.selectedShip)
        self.speedSlider.config(from_=-ship.vmax, to=ship.vmax)
        self.speedSlider.set(ship.speed)
        self.courseSlider.set(ship.course)

        if self.selectedShip not in self.world.sim.activeShips:
            self.message.set("Choose location for %s and set speed and course" % self.selectedShip)
            self.world.sim.addDynamicObject(self.selectedShip, ship.location, ship.course, speed=ship.speed)
            self.speedSlider.set(ship.vmean)

    def selectLocationForShip(self, event=None):
        try:
            self.world.do[self.selectedShip].location = [event.xdata, event.ydata]
        except KeyError:
            self.message.set("No ship is selected")

    def setCourse(self, event=None):
        self.world.do[self.selectedShip].course = self.courseSlider.get()

    def setSpeed(self, event=None):
        self.world.do[self.selectedShip].speed = self.speedSlider.get()

    def removeShipFromPlot(self, event=None):
        if self.selectedShip in self.world.sim.activeShips:
            self.world.sim.removeDynamicObject(self.selectedShip)
            self.deleteShipPlotObjects(self.world.do[self.selectedShip])
        else:
            self.message.set("No active vessel was selected")

        self.vesselList.selection_clear(0, END)