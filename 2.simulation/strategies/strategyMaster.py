NOBET = 0


class simpleAboveOdds():

    def __init__(self, timePrice, changableVars):
        self.timePrice = timePrice
        self.minArrayLength = 20
        self.minBuyPrice = 3
        self.varDict = {"minArrayLength":self.minArrayLength, "minBuyPrice":self.minBuyPrice}
        self.decodeVars(changableVars)


    def decodeVars(self,changableVars):
        # print(changableVars)
        for k,v in changableVars.items():
            if k == "minArrayLength":
                self.minArrayLength = v
            if k == "minBuyPrice":
                self.minBuyPrice = v



    def main(self):
        # print(self.timePrice)

        prices = self.timePrice[1]
        betprice = NOBET
        outcome = None

        if(len(prices)<self.minArrayLength):
            return 0, 0, 0

        if (prices[0] > self.minBuyPrice) and (prices[0] < self.minBuyPrice+1):
            betprice = prices[0]
            outcome = prices[-1]
        else:
            pass
        return betprice, 5, outcome


class earlyLiveOdds():

    def __init__(self, timePrice, bankAmount, changableVars):
        self.timePrice = timePrice
        self.minArrayLength = 20
        self.timeForCutoff = 1.5
        self.minOdds = 4
        self.edge = 0.05
        self.varDict = {
            "minArrayLength":self.minArrayLength,
            "timeForCutoff":self.timeForCutoff,
            "minOdds":self.minOdds,
            "edge":self.edge
        }
        self.bankAmount = bankAmount
        self.decodeVars(changableVars)


    def decodeVars(self,changableVars):
        # self.singleVsMultiVarFormat(changableVars)
        for k,v in changableVars.items():
            if k == "minArrayLength":
                self.minArrayLength = v
            if k == "timeForCutoff":
                self.timeForCutoff = v
            if k == "minOdds":
                self.minOdds = v
            if k == "edge":
                self.edge = v

    def singleVsMultiVarFormat(self, changableVars):
        for k,v in changableVars.items():
            if isinstance(v, list):
                break
            else:
                return
        else:
            for k,v in changableVars.items():
                changableVars[k] = v[0]
        return



    def main(self):
        #first testingValue mins into the match
        times = self.timePrice[0]
        prices = self.timePrice[1]

        # buyingPrices = [] #try with or without the first odds price
        # betamounts = []

        try:
            if(len(prices)<self.minArrayLength):
                return 0, 0, 0
            if(prices[0]<self.minOdds):
                return 0, 0, 0
        except:
            pass

        cutoffTimeInMs = self.timeForCutoff * 60000
        #index of cutoff point
        cutoff = 0

        try:
            while times[cutoff] < cutoffTimeInMs:
                cutoff += 1

            # for price in prices[1:cutoff]:
            #     if price>prices[0]:
            #         return price, kelly(self.bankAmount, 1/prices[0], price), prices[-1]
            # print("---------")
            # print(timePrice)
            # print("bought at %lf, with outcome %s, final index was %d" % (max(prices[0:cutoff]), prices[-1], cutoff))

            #not using max, but buying half the remainder of betsize every price increase
            #take the average of all the buying levels with equal betsizing
            i=1
            while i>cutoff:
                if (((prices[i]-prices[0])/prices[0])) > self.edge:
                    # print("---------")
                    # print(timePrice)
                    # print("start price = %lf, edge = %lf as a percentage = %lf" %(prices[i], prices[i]-prices[0],(prices[i]-prices[0])/prices[0]))

                    # buyingPrices.append(10)
                    # print("startprice=%lf, ourvalue=%lf, edge=%lf"%(prices[0], prices[i], ((prices[i]-prices[0])/prices[0])))
                    return prices[i], kelly(self.bankAmount, 1/prices[0], prices[i]), prices[-1]
                i+=1

            #max(prices[0:cutoff]), prices[-1]
            return 0, 0, 0
        except:
            return 0, 0, 0
        #max(timePrice[0:10])

    # stratList = {"simpleAboveOdds":simpleAboveOdds, "earlyLiveValue":earlyLiveValue}

def kelly(bankAmount, probability, payout):

    ratio = ((probability * payout) -(1-probability))/(payout)
    betsize = bankAmount*ratio

    if betsize<5:
        return 5
    else:
        # print(betsize)
        return 5
    # return 5
