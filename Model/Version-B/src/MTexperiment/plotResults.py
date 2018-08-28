import matplotlib.pyplot as plt
import matplotlib
import numpy as np


def createPlot(figureName):
    plt.figure(figureName)

def storePlot(figureName):
    plt.tight_layout()
    plt.savefig("D:\ingma\OneDrive\Studie\Thesis\Model\Version-B\plots\ " + figureName + ".png", dpi=250)

def plotLinesOverTime(figureName, testResults, plotY, save=True):
    createPlot(figureName)

    for testname in testResults:
        for value in plotY:
            plt.plot(testResults[testname]["timestamp"], testResults[testname][value], label=value)
        plt.legend()

    if save:
        storePlot(figureName)


def plotScatter(figureName, testResults, plotX, plotY, plotC, save=True):
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
    cbar = plt.colorbar()
    cbar.set_label(plotC)

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

