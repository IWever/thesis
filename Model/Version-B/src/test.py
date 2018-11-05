import matplotlib.pyplot as plt
import numpy as np
import math
import datetime

b = [-5, 19]
a = [3, 21]

d = math.hypot(a[0]-b[0], a[1] - b[1])

filename = r"D:\ingma\OneDrive\Studie\Thesis\Model\Version-B\results\%s" % datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "_Result"
print(filename)