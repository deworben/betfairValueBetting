from parseOneFile import *
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# run this script once per data set to create a saved list where you can perform analysis
dataTimeframe = "oct_data"
currentDir = os.path.dirname(os.path.abspath(__file__))
path_to_folder = os.path.join(currentDir, "..", "data", dataTimeframe)

i = 0

outputDump = os.path.join(currentDir, "..", "tennisArrays.npy")
# outputDump = "tennisArraysFullYr.npy"
listOfLists = []


for file in os.listdir(path_to_folder):
    if not file.endswith('.bz2'):
        (timeLists, priceLists) = readFile(path_to_folder + "\\" + file)
        if timeLists:
            for index, times in enumerate(timeLists):
                # adds individual time-price array paris intio seperate array
                listOfLists.append(
                    [timeLists[index].copy(), priceLists[index].copy()])

    i += 1
    # Print the number of files read to the screen
    if(i % 500 == 0):
        print(i)


try:
    os.remove(outputDump)
except:
    pass
# Save all the data that's been parsed
np.save(outputDump, listOfLists)

print("--------------------------------------\n\n\n")

