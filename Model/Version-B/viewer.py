class Viewer:
    """ The class in which the viewer for representing the simulation will be created"""

    def __init__(self, world):
        self.root = world.root
        self.root.title(world.name)
        self.root.mainloop()
