from parsingJson import *
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#run this script once per data set to create a saved lists where you can decompress to use

path_to_folder = r"C:\Users\User\Documents\Betting\Tennis\oddsPatterns\betfairTennisAnalysis\data\oct_data"
# path_to_folder = r"C:\Users\User\Documents\Betting\Tennis\oddsPatterns\betfairTennisAnalysis\fullYrData"
i=0

endFile = "tennisArraysTemp.npy"
# endFile = "tennisArraysFullYr.npy"
listOfLists = []


for file in os.listdir(path_to_folder):

        if not file.endswith('.bz2'):
                (timeLists, priceLists) = readFile(path_to_folder + "\\" + file)
                if timeLists:
                        for index, times in enumerate(timeLists):
                                #adds individual time-price array paris intio seperate array
                                listOfLists.append([timeLists[index].copy(), priceLists[index].copy()])
                                # print([timeLists[index].copy(), priceLists[index].copy()])
        i+=1
        if(i%500 == 0):
                print(i)
                # print(listOfLists[i:i+500])
print(listOfLists)
print(len(listOfLists))




try:
        os.remove(endFile)
except:
        pass      
np.save(endFile, listOfLists)

print("--------------------------------------\n\n\n")



