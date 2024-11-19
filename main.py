#include <iostream>
import numpy as np
import pandas as pd

dt = np.dtype([("day","i2"), ("hour", "i2"), ("minute", "i2"), ("second","i2"), ("year","i2"), \
                ("geodetic latitude","i2"), ("geographic longitude","i2"), \
                ("altitude","i2"), ("geographic latitude*","i2"), ("geographic longitude*","i2"), \
                ("corrected geomagnetic latitude","i2"), ("corrected geomagnetic longitude","i2"), \
                ("hour of magnetic local time","i2"), ("minute of hour of magnetic local time","i2"), \
                ("second of minute of magnetic local time","i2"), \
                ("hour of day for 1st second of data","i2"), \
                ("minute of hour for 1st second of data","i2"), \
                ("second of minute for 1st second of data", "i2"), \ 
                ("channel 4, 9450 eV electrons,","i2"), ("channel 3, 13900 eV electrons,","i2"), \
                ("channel 2, 20400 eV electrons,","i2"), ("Channel 1, 30000 eV electrons","i2"), ("channel 8, 2040 eV electrons","i2"), \
                ("channel 7, 3000 eV electrons","i2"), ("channel 6, 4400 eV electrons","i2"), \
                ("channel 5, 6460 eV electrons","i2"), ("channel 12, 646 eV electrons","i2"), \
                ("channel 11, 949 eV electrons/status word 1 if SSJ5 data","i2"), 
                ("channel 10, 949 eV electrons","i2"), ("channel 9, 1392 eV electrons","i2"), \
                ("channel 16, 139 eV electrons","i2"), ("channel 15, 204 eV electrons","i2"), \
                ("channel 14, 300 eV electrons","i2"), ("channel 13, 440 eV electrons,","i2"), \
                ("channel 20, 30 eV electrons","i2"), \
                ("channel 19, 44 eV electrons","i2"), ("channel 18, 65 eV electrons","i2"), \
                ("channel 17, 95 eV electrons","i2"), ("channel 4, 9450 eV ions","i2"), ("channel 3, 13900 eV ions","i2"), \
                ("channel 2, 20400 eV ions,","i2"), ("channel 1, 30000 eV ions","i2"), \
                ("channel 8, 2040 eV ions","i2"), ("channel 7, 3000 eV ions","i2"), ("channel 6, 4400 eV ions","i2"), \
                ("channel 5, 6460 eV ions","i2"), ("channel 12, 646 eV ions","i2"), ("channel 11, 949 eV ions","i2"), \
                ("channel 10, 949 eV ions","i2"), ("channel 9, 1392 eV ions","i2"), \
                ("channel 16, 139 eV ions","i2"), ("channel 15, 204 eV ions","i2"), \
                ("channel 14, 300 eV ions","i2"), ("channel 13, 440 eV ions","i2"), \
                ("channel 20, 30 eV ions","i2"), \
                ("channel 14, 300 eV ions","i2"), ("channel 13, 440 eV ions","i2"), \
                ("channel 20, 30 eV ions","i2"), ("channel 19, 44 eV ions","i2"), \
                ("channel 18, 65 eV ions","i2"), ("channel 17, 95 eV ions","i2"), \
                ("channel 14, 300 eV ions","i2"), ("channel 13, 440 eV ions","i2")])
