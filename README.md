# betfairTennisAnalysis
Code to analyse the accuracy of betfair odds compared to observed probabilities


Files parse json data provided by beyfair historical data and convert them to python arrays. Each has a sub-array of relative time data (relative to the first time provided as '0') and price data for analysis.
Testing has been done on tennis match odds, however code can easily be modified for different sports. 

interperateData shows the opportunities that exist in the market and highlight the accuracies and inaccuracies comparing historical (actual) and provided (theoretical) odds per match.

Finally, analysis is done and uses two successful betting strategies. Bankrolls are simulated and projected if you were to apply these strategies over the provided data.
