import math

class Car(object):

    numberOfWheels = 4


    def __init__(self, color):
        self.location = []
        self.color = color

car1 = Car("orange")
car2 = Car("pink")

print(car1.numberOfWheels)
print(car1.color)
print(car1.location)
print(car2.location)

car1.location.append([5,4])

print(car1.location)


car1.location.append([9,2])

print(car1.location)

car1.location.pop(0)

print(car1.location)

dx = 5
dy = -1

print(math.degrees(math.atan(dx/dy)))