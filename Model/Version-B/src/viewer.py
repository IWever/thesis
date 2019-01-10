from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import seaborn as sns


import math

class Viewer:
    """ The class in which the viewer for representing the simulation will be created"""

    def __init__(self, world):
        """" Create viewer with infobar, plottingcanvas and sidebar. """

        # Initial creation and import of world
        self.world = world
        self.root = world.root
        self.root.title(world.experimentName)

        try:
            self.secondScreen = world.secondScreen
            self.secondScreen.title("ECDIS viewer")
        except AttributeError:
            pass

        # Create variables
        self.message = StringVar()
        self.simulationRunning = True
        self.time = StringVar()
        self.scale = 4
        self.shipLocationMarkers = None
        self.selectedShip = None
        self.shipSpeed = StringVar()
        self.shipCourse = StringVar()
        self.shipRudder = StringVar()
        self.shipName = StringVar()

        # Collection of callbacks for plot
        self.plotButtonPress = None

        # Created Frames
        self.createInfoBar()
        self.createPlottingCanvas()
        self.createSidebar()

        # Run the GUI
        self.world.log("Created GUI screen")
        self.initialPlot()
        self.updatePlot()

    """" Create the different parts of the GUI. """
    def createInfoBar(self):
        """" Create inforbar to print messages and space for plot controls. """
        # Initial message in info-bar
        self.message.set("Let it sail")

        # Create bar and label containing message
        self.infoBar = Frame(self.root)
        self.infoBar.pack(side=BOTTOM, fill=X, expand=FALSE)
        self.infoLabel = Label(self.infoBar, textvariable=self.message)
        self.infoLabel.pack()

    def createPlottingCanvas(self):
        """" Create plotting canvas en controls to draw ships. """
        # Set lay-out plot using seaborne package
        sns.set()

        # Frame containing the plot
        self.mapViewer = Frame(self.root)
        self.mapViewer.pack(side=LEFT, fill=BOTH, expand=True)

        # Figure within frame containing plot
        self.mapFigure = Figure()
        # Adjust margins
        self.mapPlot = self.mapFigure.subplots_adjust(left=0.05, bottom=0.05, right=1, top=1)

        self.mapPlot = self.mapFigure.add_subplot(111, adjustable='box', aspect=1, facecolor='lightblue')
        self.mapPlot.axis(self.world.mapLocation)
        self.mapPlot.grid(False)

        # Canvas used to draw plot within GUI
        self.mapCanvas = FigureCanvasTkAgg(self.mapFigure, master=self.mapViewer)
        self.mapCanvas.get_tk_widget().pack(fill=BOTH, expand=TRUE)
        self.mapCanvas.show()

        # Add standard control panel for plot to info-bar
        self.plotControls = NavigationToolbar2TkAgg(self.mapCanvas, self.mapViewer)
        self.plotControls.pack(side=TOP, fill=X)


    def createSidebar(self):
        """" Create sidebar where simulation and plot can be controlled. """

        # Frame containing all options for plot and simulation
        self.optionMenu = Frame(self.root, width=500)
        self.optionMenu.pack(side=RIGHT, fill=BOTH, expand=FALSE)

        # Listbox showing vessels within simulation
        self.vesselList = Listbox(self.optionMenu, selectmode=SINGLE)
        self.vesselList.pack(side=BOTTOM, fill=BOTH)
        for vessel in self.world.sim.activeShips:
            self.vesselList.insert(END, vessel)

        # Labels with details for selected ship
        self.shipInformationFrame = Frame(self.optionMenu)
        self.shipInformationFrame.pack(side=BOTTOM, fill=X)
        self.shipNameLabel = Label(self.shipInformationFrame, textvariable=self.shipName)
        self.shipNameLabel.pack(side=TOP)
        self.shipSpeedLabel = Label(self.shipInformationFrame, textvariable=self.shipSpeed)
        self.shipSpeedLabel.pack(side=TOP)
        self.shipCourseLabel = Label(self.shipInformationFrame, textvariable=self.shipCourse)
        self.shipCourseLabel.pack(side=TOP)
        self.shipRudderLabel = Label(self.shipInformationFrame, textvariable=self.shipRudder)
        self.shipRudderLabel.pack(side=TOP)

        # Label showing runtime of simulation
        self.timeLabel = Label(self.optionMenu, textvariable=self.time)
        self.timeLabel.pack(side=TOP, fill=X)
        self.simulationControlButton = Button(self.optionMenu, text="Pause simulation", command=self.pauseSimulation)
        self.simulationControlButton.pack(side=TOP, fill=X)
        self.root.bind("<space>", self.pauseSimulation)

        # Button to enter menu where situation can be modified
        self.modifyShipButton = Button(self.optionMenu, text="Modify mode", command=self.modifyShipFromList)
        self.modifyShipButton.pack(side=TOP, fill=X)

        # Button to enter menu where ships can be sailed as a captain
        self.sailModeButton = Button(self.optionMenu, text="Sailing mode", command=self.sailSelectedShip)
        self.sailModeButton.pack(side=TOP, fill=X)
        self.sailSelectedShip()

    """" Run and pause simulation. """
    def pauseSimulation(self, event=None):
        self.simulationControlButton.configure(text="Run simulation", command=self.runSimulation)
        self.simulationRunning = False
        self.root.bind("<space>", self.runSimulation)
        self.message.set("Simulation paused")

    def runSimulation(self, event=None):
        self.message.set("Simulation continued")
        self.simulationControlButton.configure(text="Pause simulation", command=self.pauseSimulation)
        self.simulationRunning = True
        self.root.bind("<space>", self.pauseSimulation)
        self.world.runSimulation()

    """" The modify mode, where ships can be edited to create a specific situation. """
    def modifyShipFromList(self):
        self.openModifyMenu()
        self.modifyShipButton.configure(text="Close modify mode", command=self.closeModifyMenu)
        self.vesselList.selection_clear(0, END)

        self.message.set("Use sliders or click new position to edit selected ship")

        self.vesselList.bind('<<ListboxSelect>>', self.shipSelectedToModify)
        self.speedSlider.bind("<ButtonRelease-1>", self.setSpeed)
        self.speedSlider.bind("<ButtonRelease-3>", self.setSpeed)
        self.courseSlider.bind("<ButtonRelease-1>", self.setCourse)
        self.courseSlider.bind("<ButtonRelease-3>", self.setCourse)
        self.plotButtonPress = self.mapCanvas.mpl_connect('button_press_event', self.setLocationForShip)

    def openModifyMenu(self):
        """" Frame with buttons and sliders which are used to modify situation. """
        self.modifyMenuFrame = Frame(self.optionMenu)
        self.modifyMenuFrame.pack(side=TOP, fill=X)

        self.removeShipButton = Button(self.modifyMenuFrame, text="Remove ship from plot", command=self.removeShipFromPlot)
        self.removeShipButton.pack(side=TOP, fill=X)

        self.speedSlider = Scale(self.modifyMenuFrame, from_=-20, to=20,
                                 orient=HORIZONTAL, label="Non-turning speed [kn]", resolution=0.1)
        self.speedSlider.pack(side=TOP, fill=X)

        self.courseSlider = Scale(self.modifyMenuFrame, from_=-180, to=360,
                                  orient=HORIZONTAL, label="Course [deg]")
        self.courseSlider.pack(side=TOP, fill=X)

        self.vesselList.delete(0,'end')
        for vessel in self.world.do:
            self.vesselList.insert(END, vessel)

    def shipSelectedToModify(self, event=None):
        """ Select a ship to modify and set sliders according to current information known about the ship. """
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

    def closeModifyMenu(self):
        self.modifyMenuFrame.forget()
        self.modifyShipButton.configure(text="Modify mode", command=self.modifyShipFromList)

        self.message.set("Closed modify mode")

        self.vesselList.unbind('<<ListboxSelect>>')
        self.speedSlider.unbind("<ButtonRelease-1>")
        self.courseSlider.unbind("<ButtonRelease-1>")
        self.mapCanvas.mpl_disconnect(self.plotButtonPress)

        self.vesselList.delete(0, 'end')
        for vessel in self.world.sim.activeShips:
            self.vesselList.insert(END, vessel)

    """" Functions called in modify menu to modify situation. """
    def setLocationForShip(self, event=None):
        """" Set location of selected vessel. """
        try:
            self.world.do[self.selectedShip].location = [event.xdata, event.ydata]
            self.world.log("%s added at [%d, %d]" % (self.selectedShip, event.xdata, event.ydata))
        except KeyError:
            self.message.set("First select ship from list")

    def setCourse(self, event=None):
        """" Set course of selected vessel. """
        try:
            self.world.do[self.selectedShip].course = self.courseSlider.get()
            self.world.do[self.selectedShip].heading = self.courseSlider.get()
            self.world.log("For %s course set at %d degrees" % (self.selectedShip, self.courseSlider.get()))
        except KeyError:
            self.message.set("First select ship from list")

    def setSpeed(self, event=None):
        """" Set speed of selected vessel. """
        try:
            ship = self.world.do[self.selectedShip]
            ship.speed = self.speedSlider.get()
            ship.telegraphSpeed = ship.speed / ship.vmax
            self.world.log("For %s speed set at %d knots" % (self.selectedShip, ship.speed))
        except KeyError:
            self.message.set("First select ship from list")

    def removeShipFromPlot(self, event=None):
        """" Remove ship from simulation and plot based on selection"""
        if self.selectedShip in self.world.sim.activeShips:
            self.world.sim.removeDynamicObject(self.selectedShip)
            self.deleteShipPlotObjects(self.world.do[self.selectedShip])
            self.world.log("%s has been removed" % (self.selectedShip))
        else:
            self.message.set("No active vessel was selected")

        self.vesselList.selection_clear(0, END)

    """" The sailing mode, where ship can be sailed as captain. """
    def sailSelectedShip(self):
        self.openSailingMenu()
        self.sailModeButton.configure(text="Close sail mode", command=self.closeSailingMenu)
        self.vesselList.selection_clear(0, END)

        self.message.set("Use sliders to sail selected vessel")

        self.vesselList.bind('<<ListboxSelect>>', self.shipSelectedToSail)
        self.rudderAngleSlider.bind("<ButtonRelease-1>", self.setRudder)
        self.rudderAngleSlider.bind("<ButtonRelease-3>", self.setRudder)
        self.throttleSlider.bind("<ButtonRelease-1>", self.setThrottle)
        self.throttleSlider.bind("<ButtonRelease-3>", self.setThrottle)

    def openSailingMenu(self):
        """" Frame with buttons and sliders to sail ship. """
        self.sailMenuFrame = Frame(self.optionMenu)
        self.sailMenuFrame.pack(side=TOP, fill=X)

        self.rudderAngleSlider = Scale(self.sailMenuFrame, from_=-35, to=35,
                                       orient=HORIZONTAL, label="Rudder [deg]", resolution=0.5)
        self.rudderAngleSlider.pack(side=TOP, fill=X)

        self.throttleSlider = Scale(self.sailMenuFrame, from_=-1, to=1,
                                    orient=HORIZONTAL, label="RPM [%]", resolution=0.01)
        self.throttleSlider.pack(side=TOP, fill=X)

        self.addWaypoint = Button(self.sailMenuFrame, text="Add waypoint", command=self.addWaypoint)
        self.addWaypoint.pack(side=TOP, fill=X)

        self.root.bind("<Left>", self.steerLeft)
        self.root.bind("<Right>", self.steerRight)
        self.root.bind("<Up>", self.speedUp)
        self.root.bind("<Down>", self.slowDown)

    def closeSailingMenu(self):
        self.sailMenuFrame.forget()
        self.sailModeButton.configure(text="Sailing mode", command=self.sailSelectedShip)

        self.message.set("Closed sailing mode")

        self.vesselList.unbind('<<ListboxSelect>>')
        self.rudderAngleSlider.unbind("<ButtonRelease-1>")
        self.throttleSlider.unbind("<ButtonRelease-1>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")

    def shipSelectedToSail(self, event=None):
        """ Select a ship to sail and set sliders according to current information known about the ship. """
        self.selectedShip = self.vesselList.get(self.vesselList.curselection())
        ship = self.world.do[self.selectedShip]

        self.message.set("Sail %s using sliders" % self.selectedShip)
        self.rudderAngleSlider.set(ship.rudderAngle)
        self.throttleSlider.set(ship.telegraphSpeed)

    def setRudder(self, event=None):
        """" Set rudder for selected vessel. """
        try:
            self.world.do[self.selectedShip].rudderAngle = self.rudderAngleSlider.get()
            self.world.log("Rudder angle for %s set at %d degrees" % (self.selectedShip, self.rudderAngleSlider.get()))
        except KeyError:
            self.message.set("First select ship from list")
        pass

    def steerRight(self, event=None):
        """" Set rudder for selected vessel. """
        try:
            self.world.do[self.selectedShip].rudderAngle += 5
            self.rudderAngleSlider.set(self.world.do[self.selectedShip].rudderAngle)
            self.world.log("Rudder angle for %s set at %d degrees" % (self.selectedShip, self.rudderAngleSlider.get()))
        except KeyError:
            self.message.set("First select ship from list")
        pass

    def steerLeft(self, event=None):
        """" Set rudder for selected vessel. """
        try:
            self.world.do[self.selectedShip].rudderAngle -= 5
            self.rudderAngleSlider.set(self.world.do[self.selectedShip].rudderAngle)
            self.world.log("Rudder angle for %s set at %d degrees" % (self.selectedShip, self.rudderAngleSlider.get()))
        except KeyError:
            self.message.set("First select ship from list")
        pass

    def speedUp(self, event=None):
        """" Set rudder for selected vessel. """
        try:
            self.world.do[self.selectedShip].telegraphSpeed += 0.02
            self.throttleSlider.set(self.world.do[self.selectedShip].telegraphSpeed)
            self.world.log("For %s telegraphspeed changed to %1.3f" % (self.selectedShip, self.throttleSlider.get()))
        except KeyError:
            self.message.set("First select ship from list")
        pass

    def slowDown(self, event=None):
        """" Set rudder for selected vessel. """
        try:
            self.world.do[self.selectedShip].telegraphSpeed -= 0.02
            self.throttleSlider.set(self.world.do[self.selectedShip].telegraphSpeed)
            self.world.log("For %s telegraphspeed changed to %1.3f" % (self.selectedShip, self.throttleSlider.get()))
        except KeyError:
            self.message.set("First select ship from list")
        pass

    def setThrottle(self, event=None):
        """" Set speed on telegraph for selected vessel. """
        try:
            self.world.do[self.selectedShip].telegraphSpeed = self.throttleSlider.get()
            self.world.log("For %s telegraphspeed changed to %1.3f" % (self.selectedShip, self.throttleSlider.get()))
        except KeyError:
            self.message.set("First select ship from list")
        pass

    def addWaypoint(self, event=None):
        self.message.set("Select new waypoint")
        self.plotButtonPress = self.mapCanvas.mpl_connect('button_press_event', self.clickWaypoint)

    def clickWaypoint(self, event=None):
        try:
            self.world.do[self.selectedShip].waypoints.append([event.xdata, event.ydata])
            self.world.log("For %s added waypoint at [%d, %d]" % (self.selectedShip, event.xdata, event.ydata))
            self.plotWaypoint(self.selectedShip)
            self.mapCanvas.mpl_disconnect(self.plotButtonPress)
            self.message.set("Sail selected ship")
        except KeyError:
            self.message.set("First select ship from list and than select waypoint")


    """" Functions needed to plot ships in figure. """
    def initialPlot(self):
        # Add map of situation using image
        if self.world.mapName is not None:
            ENCmap = plt.imread('image/%s.png' % self.world.mapName)
            self.mapPlot.imshow(ENCmap, zorder=0, extent=self.world.mapLocation)

        for staticPatch in self.world.so:
            self.mapPlot.add_patch(self.world.so[staticPatch])


    def updatePlot(self):
        for shipname in self.world.sim.activeShips:
            self.plotShip(shipname)

        self.time.set("Time: %d seconds" % self.world.env.now)

        shipSelectedListbox = self.vesselList.curselection()

        if shipSelectedListbox:
            selectedShip = self.world.do[self.vesselList.get(shipSelectedListbox)]

            self.shipName.set("%s" % selectedShip.name)
            self.shipSpeed.set("Speed: %2.1f knots" % selectedShip.speed)
            self.shipCourse.set("Course: %3.1f degrees" % selectedShip.course)
            self.shipRudder.set("Rudder: %2.1f degrees" % selectedShip.rudderAngleReal)

        else:
            self.shipName.set("First select a ship")
            self.shipSpeed.set("Speed: - knots")
            self.shipCourse.set("Course: - degrees")
            self.shipRudder.set("Rudder: - degrees")

        self.mapCanvas.draw()

    def plotShip(self, shipname):
        """" Plot ship with shipname in plot. """
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

        if self.world.coldwell:
            ship.safetyDomain = self.mapPlot.add_artist(ship.safetyDomainEllipse())

        if self.world.twoCables:
            ship.safetyDomain = self.mapPlot.add_artist(ship.safetyDomainCircle())

        if self.world.showWaypointMarkers:
            if not ship.waypointMarker:
                self.plotWaypoint(shipname)

        if ship.waypointUpdateNeeded and self.world.showWaypointMarkers:
            self.plotWaypoint(shipname)
            ship.waypointUpdateNeeded = False

    def plotWaypoint(self, shipname):
        ship = self.world.sim.activeShips[shipname]

        self.deleteWaypointMarkers(ship)

        if ship.waypoints:
            waypointX = []
            waypointY = []
            for waypointLocation in ship.waypoints:
                waypointX.append(waypointLocation[0])
                waypointY.append(waypointLocation[1])
            ship.waypointMarker = self.mapPlot.scatter(waypointX, waypointY, marker='x', color=ship.color)

    @staticmethod
    def deleteShipPlotObjects(ship):
        """" Remove previously plotted objects from map if they exist. """
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
            if ship.polygonNumber == -1:
                pass
            else:
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

        try:
            ship.safetyDomain.remove()
        except AttributeError:
            pass
        except ValueError:
            pass

    @staticmethod
    def deleteWaypointMarkers(ship):
        try:
            ship.waypointMarker.remove()
        except AttributeError:
            pass
        except ValueError:
            pass
