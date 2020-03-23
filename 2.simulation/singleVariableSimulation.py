# betting simulator - testing different strategies. For each strategy, providing a sensitivity analysis
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib
import strategies.strategyMaster as sm
from defaultTestVars import defaultOdds
import os.path as path


NOBET = 0


class SingleVariableSimulation():

    def __init__(self, fig, unchangedVars=defaultOdds):
        # ----------------------setup vraibles - do not change ------------------------
        self.bankroll = [200]
        self.timesAndPrices = None

        self.timesAndPrices = np.load(path.join(path.dirname(
            path.abspath(__file__)), "..", "tennisArrays.npy"), allow_pickle=True)

        self.stratList = {
            "simpleAboveOdds": sm.simpleAboveOdds,
            "earlyLiveOdds": sm.earlyLiveOdds
        }

        self.testVariableUnits = {
            "minBuyPrice": "dollars",
            "minArrayLength": "datapoints",
            "minOdds": "dollars",
            "timeForCutoff": "mins",
            "edge": "percent"
        }

        self.fig = fig

        # -------------------------change these values---------------------------------

        self.strat = "earlyLiveOdds"

        try:
            # print("cool1")
            self.unchangedVars = unchangedVars[self.strat]

        except:
            # print("cool2")
            self.unchangedVars = unchangedVars

        self.testVariables = None
        self.singleVariables(self.unchangedVars)
        self.test(self.testVariables)

        # ----------------------------main functions-----------------------------------

    def singleVariables(self, testVariables):

        for variable in testVariables:
            # if(isinstance(testVariables[list(testVariables.keys())[0]], list)):
            if(isinstance(testVariables[variable], list)):
                # print(self.testVariables[variable])
                temp = self.unchangedVars[variable][0]
                self.unchangedVars[variable] = temp

            self.testVariables = self.unchangedVars
        else:
            self.testVariables = self.unchangedVars

            # print("done")

    def test(self, testVariables):
        # print(testVariables)
        for timePrice in self.timesAndPrices:

            obj = self.stratList[self.strat](
                timePrice, self.bankroll[-1], self.testVariables)
            betprice, betsize, outcome = obj.main()
            self.executeDecision(betprice, betsize, outcome)

        self.plotGraphs()

    def plotGraphs(self):
        self.plotBankroll()
        # self.plotReturns(variableName, variableList)

    def executeDecision(self, betprice, betsize, outcome):
        bankroll = self.bankroll
        if betprice == NOBET:
            return
        else:
            if outcome == "WINNER":
                bankroll.append(bankroll[-1]+betsize*(betprice-1))
                # print("Bet placed at %lf, with %lf betsize, and %s outcome. old bank=%f, new bank=%lf" %(betprice, betsize, outcome, bankroll[-2], bankroll[-1]))
            else:
                bankroll.append(bankroll[-1]-betsize)
                # print("Bet placed at %lf, with %lf betsize, and %s outcome. old bank=%f, new bank=%lf" %(betprice, betsize, outcome, bankroll[-2], bankroll[-1]))

    def plotBankroll(self):

        # print("plotting!")
        # print(self.testVariables)
        # print(self.bankroll[-10:-1])

        # pyplot.subplot(2, len(self.testVariables), plotIndex)
        # a = self.fig.add_subplot(2, 1, 1)

        pyplot.title(
            "Graphing" " tennis betting strategy bankrolls and returns")

        pyplot.xlabel("Number of bets")
        pyplot.ylabel("Bankroll outcomes")

        self.fig.plot(self.bankroll)

    # def plotReturns(self):
    #     tryValues = []
    #     returns = []
    #     plotIndex = list(self.testVariables.keys()).index(variableName) + 1 + len(self.testVariables)

    #     # pyplot.subplot(2, len(self.testVariables), plotIndex)
    #     b = self.fig.add_subplot(2, len(self.testVariables), plotIndex)
    #     # pyplot.xlabel("Changing "+variableName)

    #     # pyplot.ylabel("Returns from strategy in %")
    #     for index, bankroll in enumerate(self.bankrolls):
    #         tryValues.append(variableList[index])
    #         returns.append(((bankroll[-1]/bankroll[0])-1)*100)
    #     # pyplot.plot(tryValues, returns)
    #     b.plot(tryValues, returns)


# something = SingleVariableSimulation()
