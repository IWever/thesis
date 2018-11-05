import pickle
from src.MTexperiment.plotResults import *

file = open("results/20181102-155239_Result", "rb")
generalResult = pickle.load(file)

plotScatter("Distsance, Passing distance, Advance", generalResult, "Distance till initial CPA [meter]", "Passing distance [meter]", "Advance [meter]", save=False)
plotScatter("Distsance, Advance, Passing distance", generalResult, "Advance [meter]", "Distance till initial CPA [meter]", "Passing distance [meter]", save=False)
plotScatter("Advance, Passing distance, Distance", generalResult, "Advance [meter]", "Passing distance [meter]", "Distance till initial CPA [meter]", save=False)

plt.show()

file.close()

file = open("results/20181031-182935_Result", "rb")
generalResult = pickle.load(file)
