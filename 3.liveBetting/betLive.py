import logging
import os
import queue
from heapq import heappop, heappush, heapify
import time
import sys
import winsound
from multiprocessing import SimpleQueue
from userPassKey import obj
from datetime import datetime, timedelta

import betfairlightweight
from betfairlightweight import filters

# setup logging
logging.basicConfig(level=logging.INFO)
HIGH_FREQ = 1500
LOW_FREQ = 400


class MakeTrades():

    def __init__(self):
        self.sport = 'Soccer'
        self.minMarketVol = 1  # 10,000 for live
        self.matchTimeList = []
        self.timeZoneCorrection = timedelta(hours=11)

        self.nextToJump = datetime.now()
        self.nextToJumpEvents = SimpleQueue()
        self.cancelTradesQueue = []

        # create trading instance (no need to put in correct details)
        self.trading = betfairlightweight.APIClient(
            obj["username"], obj["password"], app_key=obj["key"])
        self.main()

    def main(self):
        # __init__ stuff
        self.trading.login()
        self.killAllTrades()
        heapify(self.cancelTradesQueue)
        heappush(self.cancelTradesQueue,
                 (datetime(2022, 3, 20), 123445, 'FALSE'))

        # the setup
        self.createMatchTimeList()
        self.updateNextToJump()

        # the main loop
        while 1:
            self.waitTillEarliestAction()

            # if next to jump is first, place trades and update
            if self.nextToJump < self.cancelTradesQueue[0][0]:
                # self.waitTillNextToJump()
                self.executeTrades()
                self.updateNextToJump()

            # if cancelTradesTime is first, cancel trades and update
            elif self.cancelTradesQueue[0][0] < self.nextToJump:
                self.cancelTrades()

    def waitTillEarliestAction(self):
        print("start waitTillEarliestAction")
        # sleep till either you should make a trade or cancel trades
        # if next to jump earlier, sleep the difference between then and now (- 10 secs for buffer)

        if self.nextToJump < self.cancelTradesQueue[0][0]:
            print("waiting for next to jump at %s, time now is %s" %
                  (self.nextToJump, datetime.now()))
            timeToSleep = (self.nextToJump - datetime.now() -
                           timedelta(seconds=10))
            # print("total seconds sleeping is %d " %(timeToSleep))
            if timeToSleep > timedelta(seconds=0):
                print("sleeping")
                # countdown timer instead of just being asleep
                self.sleepCountdown(timeToSleep.seconds)
        # if need to cancel trades first, sleep the difference between then and now
        else:
            print("waiting for cancel trades at %s, time now is %s" %
                  (self.cancelTradesQueue[0][0], datetime.now()))
            timeToSleep = (
                self.cancelTradesQueue[0][0] - datetime.now() - timedelta(seconds=10))
            if timeToSleep > timedelta(seconds=0):
                print("sleeping")
                self.sleepCountdown(timeToSleep.seconds)
            # self.sleepCountdown(timeToSleep)
        print("Finish waitTillEarliestAction")

    def sleepCountdown(self, timeToSleep):
        for i in range(timeToSleep, 0, -1):
            sys.stdout.flush()
            sys.stdout.write(str(i)+' ')
            time.sleep(0.99)

    # create a list of lists that contain market id strings and time objects
    def createMatchTimeList(self, extendedNumber=0):
        print("start createMatchTimeList")
        market_catalogues = self.getMatchList(extendedNumber)
        # print("raw times:")
        # for market_catalogue in market_catalogues:
        #     print(market_catalogue.market_start_time+self.timeZoneCorrection, market_catalogue.market_id)
        self.matchTimeList = []
        # for each of the most recent games, print runners,
        for market_catalogue in market_catalogues:
            temp = [9999, 9999]

            # only add the times if starting later than now.
            if market_catalogue.market_start_time+self.timeZoneCorrection > datetime.now()+timedelta(seconds=30):
                temp[0] = market_catalogue.market_id
                temp[1] = market_catalogue.market_start_time + \
                    self.timeZoneCorrection
                self.matchTimeList.append(temp.copy())
            else:
                print("didn't make it %s" % (
                    market_catalogue.market_start_time+self.timeZoneCorrection))

        print(self.matchTimeList)
        print("end createMatchTimeList")

    def updateNextToJump(self):
        print("start updateNextToJump")

        nextIndex = None
        # cycle to find the nextToJump
        for i, match in enumerate(self.matchTimeList):
            # print(self.nextToJump, match[1])
            if match[1] > self.nextToJump:
                self.nextToJump = match[1]
                nextIndex = i
                print("next to jump at %s" % self.nextToJump)
                break
        # if the next to jump time is the last one in the matchTimeList, order more data
        if self.matchTimeList[nextIndex][1] == self.matchTimeList[-1][1]:
            print("getting new list")
            self.createMatchTimeList(20)
            self.updateNextToJump()
            return

        for match in self.matchTimeList:
            if match[1] == self.nextToJump:
                print("%s in queue to execute" % match)
                self.nextToJumpEvents.put(match)
        print("end updateNextToJump")

    def executeTrades(self):
        self.alert()
        print("start executeTrades")
        while not self.nextToJumpEvents.empty():

            market_id = float(self.nextToJumpEvents.get()[0])
            betSize = 5
            market_book = self.trading.betting.list_market_book([market_id])[0]
            runner1 = market_book.runners[0]
            runner2 = market_book.runners[1]

            # check that there's enough volume in the market
            if int(market_book.total_matched) < self.minMarketVol:
                print("cancelling bet in market %s because only traded %s and %s is min" % (
                    market_id, market_book.total_matched, self.minMarketVol))
                return

            # make sure the bet is on the underdog
            print(runner1.last_price_traded)

            selection_id = runner1.selection_id

            limit_order = filters.limit_order(
                size=betSize,
                price=100,
                persistence_type='PERSIST'
            )
            instruction = filters.place_instruction(
                order_type='LIMIT',
                selection_id=selection_id,
                side='BACK',
                limit_order=limit_order
            )
            place_orders = self.trading.betting.place_orders(
                market_id=str(market_id),
                instructions=[instruction]  # list
            )
            print(place_orders.status)
            for order in place_orders.place_instruction_reports:
                print('Order placed at: %s, Status: %s, BetId: %s, Average Price Matched: %s ' %
                      (datetime.now(), order.status, order.bet_id, order.average_price_matched))

            # betReport = self.trading.betting.list_current_orders()

            # if the bet went through, get it ready to cancel, otherwise do nothing
            if place_orders.status == "SUCCESS":
                self.updateCancelTrades(market_id)
            # else:
            #     self.createMatchTimeList(10)
            #     self.updateNextToJump

        print("end executeTrades")
        return

    def updateCancelTrades(self, market_id):  # , bet_id):
        print("start updateCancelTrades")
        # the time you'd like to check into the event, id, isTagged as inplay
        heappush(self.cancelTradesQueue, (datetime.now() +
                                          timedelta(seconds=40), market_id, 'FALSE'))
        print("pushed %s to cancel queue, queue looks like this: %s" %
              (market_id, list(self.cancelTradesQueue)))
        print("end updateCancelTrades")

    def cancelTrades(self):
        print("start cancelTrades")

        needToCancel = heappop(self.cancelTradesQueue)
        marketBook = self.trading.betting.list_market_book(
            [str(needToCancel[1])])[0]

        # check if the match has gone live. If not, add 1min30secs to datetime and put back on the queue
        if marketBook.inplay == False:

            # marketCatalogue = self.trading.betting.list_market_catalogue(filters.market_filter(
            #     market_ids=[str(needToCancel[1])]
            # ))[0]
            marketCatalogue = self.trading.betting.list_market_catalogue(
                filter=filters.market_filter(
                    market_ids=[str(needToCancel[1])]
                ),
                market_projection=['MARKET_START_TIME'],
            )[0]
            matchTime = marketCatalogue.market_start_time+self.timeZoneCorrection
            print("Market catalogue says start time is %s" % (matchTime))
            # if the match is delayed, get rid of it
            if matchTime-datetime.now() > timedelta(minutes=5):
                print("****************** we reset the old time to %s" %
                      (marketCatalogue.market_start_time))
                # CANCEL THE TRADE
                report = self.trading.betting.cancel_orders(needToCancel[1])
                print("cancelled a bet in %s market, result is %s" %
                      (report.market_id, report.status))
                self.nextToJump = datetime.now()
                # re-update the matchtime list
                self.createMatchTimeList()
                self.updateNextToJump()
                return

            temp = list(needToCancel)
            oldTime = needToCancel[0]
            temp[0] = oldTime + timedelta(seconds=30)
            newTuple = tuple(temp)
            heappush(self.cancelTradesQueue, newTuple)
            print("%s wasn't inplay, reset" % (newTuple[1]))
            return

        elif marketBook.inplay == True and needToCancel[2] == 'FALSE':
            temp = list(needToCancel)
            oldTime = needToCancel[0]
            temp[2] = 'TRUE'
            temp[0] = oldTime + timedelta(seconds=70)
            newTuple = tuple(temp)
            heappush(self.cancelTradesQueue, newTuple)
            print("%s just turned inplay, reset" % (temp[1]))
            return
        else:
            report = self.trading.betting.cancel_orders(needToCancel[1])
            self.alert()
            print("cancelled a bet in %s market, result is %s" %
                  (report.market_id, report.status))

        print("end cancelTrades")
    # returns a list of lists with eventid-starttime key-values

    def getMatchList(self, extendedNumber=0):
        numberOfMatches = 15+extendedNumber
        print("Start getMatchList")
        numMatches = numberOfMatches
        while True:
            sport_market_filter = filters.market_filter(
                text_query=self.sport
            )
            # tldr: high level - whats the sport? this will get you a list of the betfair codes of that(those) sport(s)
            event = self.trading.betting.list_event_types(
                filter=sport_market_filter)[0]

            # go through the list of event_type_id objects and find the catalogues (day match lineups - (1 catalogue = 1 match))...
            # then go through each catalogue (match) and print the information available.

            sport_id = event.event_type.id

            # list all horse racing market catalogues

            market_catalogues = self.trading.betting.list_market_catalogue(

                filter=filters.market_filter(
                    event_type_ids=[sport_id],  # filter on just the sport_id
                    # market_type_codes=['WIN'],  # filter on just WIN market types
                    # filter on just MATCH_ODDS market types
                    market_type_codes=['MATCH_ODDS'],
                    in_play_only=False             # filter on just matches that haven't started
                ),

                # start time and runner description required
                market_projection=['MARKET_START_TIME', 'RUNNER_DESCRIPTION'],

                # big enough to have multiple times in case multiple events happening at the same time
                # small enough that schedule changes don't mess with it - might need to check if this enough and increase number
                max_results=numMatches
            )

            if market_catalogues[0].market_start_time == market_catalogues[numMatches-1].market_start_time:
                numMatches += 5
                continue
            else:
                break

        print('%s market catalogues returned' % len(market_catalogues))
        print("end getMatchList")
        return market_catalogues

    def alert(self):
        for i in range(3):
            winsound.Beep(HIGH_FREQ, 500)
            winsound.Beep(LOW_FREQ, 500)
            # time.sleep(0.0001)

    def killAllTrades(self):
        self.trading.betting.cancel_orders()


while True:
    try:
        makeTrades = MakeTrades()
    except:
        try:
            makeTrades.trading.killAllTrades()
            makeTrades.trading.logout()
        except:
            print("retry")
            time.sleep(2)
