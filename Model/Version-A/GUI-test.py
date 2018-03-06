import math

import tkinter as tk
from tkinter import *

root = tk.Tk()
root.title("Test GUI")

# Database & variables
vessels = ['janni', 'jon', 'benjamin', 'titia']
vesselNames = StringVar(value=vessels)


# Use functions
def getPosition(event):
    print(event.x, event.y)

def motion(event):
    # calculate current angle relative to initial angle
    theta = slider2.get() * math.pi / 180

    shipA.heading = math.fmod(shipA.heading + slider2.get(), 360)

    print(map.coords(shipA.shipPlot))
    print(type(map.coords(shipA.shipPlot)))

    ox = map.coords(shipA.shipPlot)[0]
    oy = map.coords(shipA.shipPlot)[1]

    newxy = []
    for i in range(0, int(len(map.coords(shipA.shipPlot))/2)):
        px = map.coords(shipA.shipPlot)[i * 2]
        py = map.coords(shipA.shipPlot)[i * 2 + 1]

        newx = math.cos(theta) * (px - ox) - math.sin(theta) * (py - oy) + ox
        newy = math.sin(theta) * (px - ox) + math.cos(theta) * (py - oy) + oy

        newxy.append(newx)
        newxy.append(newy)
    map.coords(shipA.shipPlot, *newxy)

    slider2.set(0)

def itemSelected(event):
    if len(vesselList.curselection()) is 1:
        print("%s selected" % vesselList.curselection())


# Use objects
class Ship:
    def __init__(self, map, length, width):
        self.length = length
        self.width = width
        self.map = map
        self.xy = [(.5 * self.width, 1.5 * self.length), (self.width, self.length), (self.width, 0), (0, 0), (0, self.length)]
        self.heading = 0

        self.shipPlot = map.create_polygon(self.xy)
        self.map.move(self.shipPlot, 250, 250)


    def moveShip(self):
        v = slider1.get()

        self.map.move(self.shipPlot, -v * math.sin(self.heading * math.pi / 180), v * math.cos(self.heading * math.pi / 180))
        self.map.after(100, self.moveShip)




# Building GUI

## Info-bar at the bottom
info = StringVar()
info.set("Let it sail")

infoBar = Frame(root, bg='white')
infoBar.pack(side=BOTTOM, fill=X, expand=FALSE)
infoLabel = Label(infoBar, textvariable=info)
infoLabel.pack()

## Plotting canvas
mapSize = 500
mapViewer = Frame(root)
mapViewer.pack(side=LEFT, fill=BOTH, expand=FALSE)

map = Canvas(mapViewer, height=mapSize, width=mapSize, bg='royalblue')
map.pack()

shipA = Ship(map, 20, 18)

## Side-bar
optionMenu = tk.Frame(root)
optionMenu.pack(side=RIGHT, fill=BOTH, expand=TRUE)

vesselList = Listbox(optionMenu)
vesselList.pack(side=BOTTOM, fill=BOTH)
for vessel in vessels:
    vesselList.insert(END, vessel)
vesselList.bind('<<ListboxSelect>>', itemSelected)

slider1 = Scale(optionMenu, from_=-10, to=10, orient=HORIZONTAL)
slider1.pack(side=TOP, fill=X)
slider2 = Scale(optionMenu, from_=-360, to=360, orient=HORIZONTAL)
slider2.pack(side=TOP, fill=X)

slider1.bind("<ButtonRelease-1>", shipA.moveShip())
slider2.bind("<ButtonRelease-1>", motion)

## Rotating ship
center = 250, 250





root.mainloop()
