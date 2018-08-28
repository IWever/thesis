import matplotlib.pyplot as plt
import numpy as np

def make_plot(slope):
    x = np.arange(1,10)
    y = slope*x+3
    plt.figure()
    plt.plot(x,y)

make_plot(2)
make_plot(3)
plt.show()

a = "name"

b = int(a)

print(b)