# Betfair Trading Analysis and Execution Tool
This code was used to analyse the accuracy of betfair odds, simulate strategies to backtest ideas according to the historical data, and run these ideas live on the market.

**WARNING**: This code has not been refactored to fit best practices like naming conventions or design patters. It is simply a tool iteratively built for personal use. Please cover your eyes.

## How this works
The scripts in this repository were designed to be used sequentially (0, then 1, then 2, then 3). This is a reflection of how they were built to assist me after I had gathered insights from the steps previous.

0. Parse Betfair historical data. This data is surprisingly messy and isn't adjusted to reflect the real odds after Betfair takes their commission.
1. interperateData.py shows the opportunities that exist in the market and highlight the accuracies and inaccuracies comparing historical (actual) and provided (theoretical) odds per match. This alone shows great opporunities that exist in the market)
2. Simulate how applying different strategies would affect your bankroll. This supports different betting strategies, money management techniques, and inputs.
3. Finally, there is functionality to connect your own Betfair account credentials and apply the strategies from backtesting immediately. This is quite resillient against the unreliable connection, start times and odds quoting from the Betfair servers.

## Finally
Testing has been done on tennis match odds, however code can easily be modified for different sports.
There is plenty of scope for improvement. My highest priority items are:
* Creating more modular designs for more complicated strategies for backtesting
* Creating more sophisticated analysis tools - especially for live opportunities (this is in the making with projected completion around 1/5/2020

As bad as the UI looks, it was never meant for anything except analysis and so does that job well. It would be cool to have a fully functioning platform, however that is one big migration from python away...

I this looks as fun to you as it was to make. Thanks for checking out my repo!
