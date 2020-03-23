import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

# Load the array that was created in step 0 (all the parsed betfair data)
dataList = np.load(os.path.dirname(
    os.path.abspath(__file__)) + r"\..\tennisArrays.npy", allow_pickle=True)


# e.g. [ 5 (wins), 6 (losses), 11 (total) ]
tempArray = [0, 0, 0]
dataBuckets = []


# Specify the data range you'd like to analyse
oddsRangeMax = 6
oddsRangeMin = 1
pointsPerDollar = 10

numIncrements = (oddsRangeMax-oddsRangeMin)*pointsPerDollar
# also = 1/pointsPerDollar e.g. 10 means counting in 0.1 increments
incrementSize = (oddsRangeMax-oddsRangeMin)/numIncrements
BUFFER = 0.0001
WININDEX = 0
LOSEINDEX = 1
TOTALINDEX = 2

# theres a range of odds in the data set. Split into chucks with
# size: (max-min)/increments. Put win/losses into odds buckets


# 1. make buckets figure out which bucket to put it in
def init():
    for i in range(numIncrements):
        dataBuckets.append(tempArray.copy())


# 2. put in bucket (increase win or loss count depending on outcome and add one to total
def addData():
    for timePrice in dataList:
        # select bucket
        prices = timePrice[1]

        # get rid of incomplete/bad data - based on excel analysis 10k market volume
        if len(prices) < 25:
            continue

        bucketIndex = int((prices[0]-oddsRangeMin+BUFFER)/incrementSize)
        # print("first price = %lf  in bucket = %lf and a %s" % (prices[0], bucketIndex, prices[-1]))

        # skip anything outside the odds range
        if bucketIndex >= numIncrements:
            continue

        # update counter
        dataBuckets[bucketIndex][TOTALINDEX] += 1
        if prices[-1] == "WINNER":
            dataBuckets[bucketIndex][WININDEX] += 1
        else:
            dataBuckets[bucketIndex][LOSEINDEX] += 1

    # print(dataBuckets)
    total = 0
    for bucket in dataBuckets:
        total += bucket[-1]
    print("size of dataList = %d, number of points used = %d" %
          (len(dataList), total))


# 3. graph win percentage to calculated win percentage
xValues = []
yValues = []


def graph():
    for index, winLossTot in enumerate(dataBuckets):
        if winLossTot[0] == 0:
            continue
        observedOdds = winLossTot[TOTALINDEX]/winLossTot[WININDEX]
        betfairOdds = (oddsRangeMin + (index * incrementSize) +
                       incrementSize/2)  # *0.5 for the middle

        xValues.append(betfairOdds)
        yValues.append(observedOdds)

    # Get a cheeky graph going
    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(xValues, yValues, 'o')
    z = np.polyfit(xValues, yValues, 1)
    p = np.poly1d(z)

    plt.plot(xValues, p(xValues), "r-")

    # the line equation:
    print("y=%.6fx+(%.6f)" % (z[0], z[1]))
    plt.xlabel("betfair adjusted odds")
    plt.ylabel("observed outcome odds")
    print(polyfit(xValues, yValues, 1))
    # plt.show()


# Polynomial Regression
def polyfit(x, y, degree):
    results = {}

    coeffs = np.polyfit(x, y, degree)

    # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    # or sum([ (yihat - ybar)**2 for yihat in yhat])
    ssreg = np.sum((yhat-ybar)**2)
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot

    return results


def insights():
    # Find out if there is a trend to over or underprice bets
    # Figure out the distribution of over vs underpriced bets

    diff = [(yValues[i] - xValues[i]) for i, val in enumerate(yValues)]
    print("The mass of this distribution = {} {}".format(sum(diff), "overpriced" if sum(diff)>0 else "underpriced"))

    # Show the distribution of over/underpriced values
    plt.subplot(2, 1, 2)
    plt.hist(diff, bins=100)
    plt.gca().set(title='Frequency of over/underpricing', ylabel='Frequency')
    plt.xticks(ticks=[0.05, -0.05], labels=['', ''])
    plt.show()



# 4 run!
def run():
    init()
    addData()
    graph()
    insights()


run()
