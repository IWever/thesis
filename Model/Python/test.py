import numpy as np
import matplotlib.pyplot as plt

plt.show

a = np.zeros((5,5))
b = np.random.random((5, 5))


map = b

print(map)
plt.imshow(map, cmap='RdYlGn', interpolation='nearest')
plt.colorbar()
plt.show()
