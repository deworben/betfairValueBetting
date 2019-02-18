#betting simulator - testing different strategies. For each strategy, providing a sensitivity analysis
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib
import strategies.strategyMaster as sm
from defaultTestVars import defaultOdds


NOBET = 0

class MultivariableSimulation():

    def __init__(self, fig, testVariables=defaultOdds):       
        #----------------------setup vraibles - do not change ------------------------
        self.bankrolls = []
        self.timesAndPrices = None

        self.timesAndPrices = np.load("tennisArraysTemp.npy")
        # self.timesAndPrices = np.load("tennisArraysFullYr.npy")

        self.stratList = {
            "simpleAboveOdds":sm.simpleAboveOdds,
            "earlyLiveOdds":sm.earlyLiveOdds
        }

        
        self.testVariableUnits = {
            "minBuyPrice":"dollars",
            "minArrayLength":"datapoints",
            "minOdds":"dollars",
            "timeForCutoff":"mins",
            "edge":"percent"
        }

        self.fig = fig

        #-------------------------change these values---------------------------------
        self.initialValue = [200]


        self.strat = "earlyLiveOdds"

        #used for earlyLiveOdds strat
        self.testVariables = testVariables[self.strat]

        self.run()
        #----------------------------main functions-----------------------------------


    def run(self):
        # print(len(self.timesAndPrices))
        for testVariable in self.testVariables:
            # print(testVariable)
            self.test(testVariable, self.testVariables[testVariable])
        # pyplot.show()

    def test(self, variableName, variableList):
        self.createBankrolls(len(variableList))
        
        for bankrollIndex, testingValue in enumerate(variableList):
            for timePrice in self.timesAndPrices:

                obj = self.stratList[self.strat](timePrice, self.bankrolls[bankrollIndex][-1], {variableName:testingValue})
                # obj = sm.earlyLiveOdds(timePrice, {variableName:testingValue})

                betprice, betsize, outcome = obj.main()
                self.executeDecision(betprice, betsize, outcome, bankrollIndex)
              
        # print(len(self.bankrolls))
        self.plotGraphs(variableName, variableList)


    def createBankrolls(self, size):
        i=0
        self.bankrolls = []
        while i<size:
            self.bankrolls.append(self.initialValue.copy())
            i+=1

    def plotGraphs(self, variableName, variableList):
        self.plotBankroll(variableName, variableList)
        self.plotReturns(variableName, variableList)
        


    def executeDecision(self, betprice, betsize, outcome, bankrollIndex):
        bankroll = self.bankrolls[bankrollIndex]
        if betprice == NOBET:
            return
        else:
            if outcome == "WINNER":
                bankroll.append(bankroll[-1]+betsize*(betprice-1))
            else:
                bankroll.append(bankroll[-1]-betsize)


    def plotBankroll(self, variableName, variableList):
        plotIndex = list(self.testVariables.keys()).index(variableName) + 1

        # pyplot.subplot(2, len(self.testVariables), plotIndex)
        a = self.fig.add_subplot(2, len(self.testVariables), plotIndex)

        if plotIndex == 0:
            pyplot.title("Graphing " + self.strat + " tennis betting strategy bankrolls and returns")

        pyplot.xlabel("Number of bets")
        pyplot.ylabel("Bankroll outcomes")
        for i, bankroll in enumerate(self.bankrolls):

            line = str(variableList[i]) + " " + self.testVariableUnits[variableName]
            a.plot(bankroll)
            # pyplot.plot(bankroll, label=line)
            # pyplot.legend()
        


    def plotReturns(self, variableName, variableList):
        tryValues = []
        returns = []
        plotIndex = list(self.testVariables.keys()).index(variableName) + 1 + len(self.testVariables)

        # pyplot.subplot(2, len(self.testVariables), plotIndex)
        b = self.fig.add_subplot(2, len(self.testVariables), plotIndex)
        # pyplot.xlabel("Changing "+variableName)

        # pyplot.ylabel("Returns from strategy in %")
        for index, bankroll in enumerate(self.bankrolls):
            tryValues.append(variableList[index])
            returns.append(((bankroll[-1]/bankroll[0])-1)*100)
        # pyplot.plot(tryValues, returns)
        b.plot(tryValues, returns)
        


# something = MultivariableSimulation()