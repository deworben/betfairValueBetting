defaultEarlyLiveVars = {
                        "minArrayLength":[25], 
                        "minOdds":[1.5],#[1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6],
                        "timeForCutoff":[1.5],#[0.5, 1, 1.5, 2, 2.5, 3],
                        "edge":[0.05],#[0.01, 0.02, 0.03, 0.04,0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13]
                        #[from, to, resolution]
                        "ranges":[[0, 100, 5], [1.1, 5, 0.1], [0, 10, 0.1], [0, 0.1, 0.01]]
}

defaultSimpleAboveVars = {                
                        "minBuyPrice":[1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],
                        "minArrayLength":[10, 20, 40, 45, 50, 55, 60, 65, 70]
}


defaultOdds = {
            "simpleAboveOdds":defaultSimpleAboveVars,
            "earlyLiveOdds":defaultEarlyLiveVars
        }
                 