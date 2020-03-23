#This file cleans the messy data provided by the betfair historical data service
#It reports only the real price movements as well as the time into the event that
#these events occured and if the competitor was the winner or loser

import json
import os 

outcomeFLIPPED = {'WINNER':'LOSER', 'LOSER':'WINNER'}
outcomeFLIPPEDKeys = ['WINNER', 'LOSER']
maxNumTeams = 2
margin = 0.05

adjustedOdds = 1-margin 

def readFile(path):

    timeLists  = []
    priceLists = []

    started          = False
    firstLivePoint   = True
    startTime        = None
    teamIDs          = []

    i=0
    num_lines = sum(1 for line in open(path, encoding="utf=8"))

    try:
        with open(path, encoding="utf=8") as f:
            for line in f:
                i+=1
                #if the match hasn't started
                if not started:
                    #dont do anything until you see the match start - then update the started value
                    if "\"inPlay\":true" in line:
                        started = True

                #if the match has started
                elif started: 
                    #check if theres a price
                    if "marketDefinition" not in line:
                        obj = json.loads(line)
                        #set the first points time
                        if firstLivePoint:
                            startTime = int(obj['pt'])
                            #print(startTime)
                            firstLivePoint = False

                        
                        addPoints(obj, teamIDs, priceLists, timeLists, startTime)

                    #when finished, add "win"/"los" (win/loss) text to end 
                    if i==num_lines:
                        winningTeamIndex = None
                        obj = json.loads(line)
                        for index, team in enumerate(obj['mc'][0]['marketDefinition']['runners']):

                                
                                # #if only zero or one teams odds reported but multiple runners
                                try:
                                    # get winning team index
                                    if team['status'] == "WINNER":
                                        winningTeamIndex = teamIDs.index(team['id'])
                                        priceLists[winningTeamIndex].append("WINNER")
                                        
                                except:
                                    return [], []

                        #if undefined winner     
                        if winningTeamIndex == None:
                            return [], []

                        #if not the winner, change all other team outcomes to loser
                        for index, team in enumerate(priceLists):
                            if index != winningTeamIndex:
                                priceLists[index].append("LOSER")                                    
    finally:
        pass             

    #CHECK LIQUIDITY!! - Maybe (first try without - if data is rubbish then do it)
    # 
    # 
    # 
    # 
    # 
    #    
    return timeLists.copy(), priceLists.copy()

def addPoints(obj, teamIDs, priceLists, timeLists, startTime):
    objList = obj['mc'][0]['rc']
    #check if any team id's need to be added
    if len(teamIDs) < maxNumTeams:
        #try add a new team id
        for team in objList:
            if team['id'] not in teamIDs:
                teamIDs.append(team['id'])
                priceLists.append([])
                timeLists.append([])

    #now add data points
    #the index number of the team id in team ids is the index of the array with that teams price list
    #go through each team in objList
    for team in objList:
        #go through each possible team 
        for index, teamID in enumerate(teamIDs):
            if teamID == team["id"]:
                #load in adjusted betfair odds and times
                priceLists[index].append(1+((team['ltp']-1)*adjustedOdds))
                timeLists[index].append(int(obj['pt'])-startTime)
            


#Test rinning the function here
# [a, b] = readFile(os.getcwd() + "\\data\\oct_data\\1.148783384")
# print(a, b)
# [a, b] = readFile(os.getcwd() + r"\data\oct_data\1.148784444")
# print(a, b)
# [a, b] = readFile(os.getcwd() + r"\data\oct_data\1.148841533")
# print(a, b)