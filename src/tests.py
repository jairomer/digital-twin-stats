#!/usr/bin/python3 

import analisis 
import unittest


class TestDatasetLoading(unittest.TestCase): 
    def test_load(self): 
        speeds = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]

        threadedRt          = []
        notThreadedRt       = []
        notThreadedNotRt    = []
        threadedNotRt       = []

        for spd in speeds:
            threadedRt.append(
                analisis.loadDataset(RealTime=True, Speed=spd)
            )
            notThreadedRt.append(
                analisis.loadDataset(RealTime=True, Speed=spd)
            )
            threadedNotRt.append(
                analisis.loadDataset(RealTime=False, Speed=spd)
            )            
            notThreadedNotRt.append(
                analisis.loadDataset(RealTime=False, Speed=spd)
            )
        
        for spd in speeds:
            self.assertTrue(len(threadedRt[spd]) > 0)
            print(threadedRt[spd])
            self.assertTrue(len(notThreadedRt[spd]) > 0)
            print(notThreadedRt[spd])
            self.assertTrue(len(threadedNotRt[spd]) > 0)
            print(threadedNotRt[spd])
            self.assertTrue(len(notThreadedNotRt[spd]) > 0)
            print(notThreadedNotRt[spd])


if __name__ == "__main__":
    unittest.main()