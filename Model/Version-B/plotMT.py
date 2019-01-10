import pickle
from src.MTexperiment.plotResults import *

file = open("results/20181112-155526_Result_Advance", "rb")
generalResult = pickle.load(file)

# plotScatter("Distsance, Passing distance, Advance", generalResult, "Distance till initial CPA [meter]", "Passing distance [meter]", "Advance [meter]", save=False)
# plotScatter("Distsance, Advance, Passing distance", generalResult, "Advance [meter]", "Distance till initial CPA [meter]", "Passing distance [meter]", save=False)

# plotScatter("Advance, Passing distance, Distance", generalResult, "Advance distance [meter]", "Passing distance [meter]", "Distance till initial CPA [meter]", save=False)
# plotScatter("Advance, CPA, Distance", generalResult, "Advance distance [meter]", "CPA [meter]", "Distance till initial CPA [meter]", save=False)
# plotScatter("Distsance, CPA, Advance", generalResult, "Distance till initial CPA [meter]", "CPA [meter]", "Advance distance [meter]", save=False)
# plotScatter("Passing distance, CPA, Distance", generalResult, "Passing distance [meter]", "CPA [meter]", "Distance till initial CPA [meter]", save=False)

# plotScatter("Distance, CPA, Course change", generalResult, "Distance till initial CPA [meter]", "CPA [meter]", "Max course [degrees]", save=False)
# plotScatter("Distance, CPA, Start-speed", generalResult, "Distance till initial CPA [meter]", "CPA [meter]", "Start speed [knots]", save=False)
# plotScatter("Course change, CPA, start speed", generalResult, "Max course [degrees]", "CPA [meter]", "Start speed [knots]", save=False)
plotScatter("Distance CPA advance", generalResult, "Distance till initial CPA [meter]", "CPA [meter]", "Advance distance [meter]", save=False, label=False)

plotScatter("distance passing distance advance", generalResult, "Distance till initial CPA [meter]", "Passing distance [meter]", "Start speed [knots]", save=True)

#plt.axes().set_aspect('equal', 'datalim')
plt.xlim(xmin=0.0)
plt.ylim(ymin=0.0)


plt.show()

file.close()

file = open("results/20181031-182935_Result", "rb")
generalResult = pickle.load(file)
