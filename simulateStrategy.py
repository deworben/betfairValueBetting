#betting simulator - testing different strategies. For each strategy, providing a sensitivity analysis
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib
import strategies.strategyMaster as sm


#change these values
initialValue = [10000]
testingValuesSimpleStrat = [5, 7, 10, 20, 50]
testingValuesLiveStrat = [1, 2, 3, 10, 20] 

#stratList = {"simpleAboveOdds":simpleAboveOdds, "earlyLiveValue":earlyLiveValue}
strat = "earlyLiveValue"
testingValues = testingValuesLiveStrat



bankrolls = []
timesAndPrices = np.load("tennisArraysTemp.npy")
# timesAndPrices = np.load("tennisArraysFullYr.npy")
NOBET = 0

def run():
    createBankrolls()
    for bankrollIndex, testingValue in enumerate(testingValues):
        for timePrice in timesAndPrices:
            betprice, betsize, outcome = sm.stratList[strat](timePrice, testingValue)
            executeDecision(betprice, betsize, outcome, bankrollIndex)
    plotBankroll()
    plotReturns()


def createBankrolls():
    i=0
    while i<len(testingValues):
        bankrolls.append(initialValue.copy())
        i+=1
    # print(bankrolls)



def executeDecision(betprice, betsize, outcome, bankrollIndex):
    bankroll = bankrolls[bankrollIndex]
    if betprice == NOBET:
        return
    else:
        if outcome == "WINNER":
            bankroll.append(bankroll[-1]+betsize*(betprice-1))
        else:
            bankroll.append(bankroll[-1]-betsize)


def plotBankroll():
    # print(bankroll)
    pyplot.subplot(2, 1, 1)
    pyplot.title("Graphing simple tennis betting strategy bankrolls and returns")
    pyplot.xlabel("Number of bets")
    pyplot.ylabel("Bankroll outcomes")
    for i, bankroll in enumerate(bankrolls):
        line = str(testingValues[i])+" mins"
        pyplot.plot(bankroll, label=line)
        pyplot.legend()
    

def plotReturns():
    tryValues = []
    returns = []
    pyplot.subplot(2, 1, 2)
    pyplot.xlabel("Changing input variable")
    pyplot.ylabel("Returns from strategy in %")
    for index, bankroll in enumerate(bankrolls):
        tryValues.append(testingValues[index])
        returns.append(((bankroll[-1]/bankroll[0])-1)*100)
    pyplot.plot(tryValues, returns)
    pyplot.show()



run()