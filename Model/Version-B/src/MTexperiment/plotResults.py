import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime

def createPlot(figureName):
    plt.figure(figureName)

def storePlot(figureName):
    plt.tight_layout()
    plt.savefig("D:\ingma\OneDrive\Studie\Thesis\Model\Version-B\plots\ " + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "_" + figureName + ".png", dpi=250)

def plotLinesOverTime(figureName, testResults, plotY, save=True):
    createPlot(figureName)

    for testname in testResults:
        for value in plotY:
            plt.plot(testResults[testname]["Timestamp"], testResults[testname][value], label=value)
        plt.legend()
        plt.xlabel("Time [seconds]")

    if save:
        storePlot(figureName)




def plotScatter(figureName, testResults, plotX, plotY, plotC, save=True, label=False):
    createPlot(figureName)
    cmap = matplotlib.cm.get_cmap('Spectral')  # blue is high, red is low

    resultX = []
    resultY = []
    resultC = []

    for testname in testResults:
        resultX.append(testResults[testname][plotX])
        resultY.append(testResults[testname][plotY])
        resultC.append(testResults[testname][plotC])

    plt.scatter(np.array(resultX), np.array(resultY), c=np.array(resultC), alpha=0.6)

    plt.xlabel(plotX)
    plt.ylabel(plotY)
    plt.xlim(xmin=0.0)
    cbar = plt.colorbar()
    cbar.set_label(plotC)

    if label:
        for i in range(0, len(resultC[0])):
            annot = plt.annotate(resultC[0][i], (resultX[0][i], resultY[0][i]))

    if save:
        storePlot(figureName)



def plotPath(figureName, testResults, save=True):
    createPlot(figureName)

    for testname in testResults:
        plt.plot(testResults[testname]["locx"], testResults[testname]["locy"], label=testname)
        plt.axis('equal')
    plt.legend()

    if save:
        storePlot(figureName)


