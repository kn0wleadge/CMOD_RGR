#include <iostream>
import numpy as np
import pandas as pd
from columns import dict
from IPython.display import display, HTML
# dt = np.dtype([ day"  ,  hour", "i2"),  minute", "i2"),  second"  ,  year"  , \
#                  geodetic latitude"  ,  geographic longitude"  , \
#                  altitude"  ,  geographic latitude*"  ,  geographic longitude*"  , \
#                  corrected geomagnetic latitude"  ,  corrected geomagnetic longitude"  , \
#                  hour of magnetic local time"  ,  minute of hour of magnetic local time"  , \
#                  second of minute of magnetic local time"  , \
#                  hour of day for 1st second of data"  , \
#                  minute of hour for 1st second of data"  , \
#                  second of minute for 1st second of data", "i2"), \
#                  channel 4, 9450 eV electrons,"  ,  channel 3, 13900 eV electrons,"  , \
#                  channel 2, 20400 eV electrons,"  ,  Channel 1, 30000 eV electrons"  ,  channel 8, 2040 eV electrons"  , \
#                  channel 7, 3000 eV electrons"  ,  channel 6, 4400 eV electrons"  , \
#                  channel 5, 6460 eV electrons"  ,  channel 12, 646 eV electrons"  , \
#                  channel 11, 949 eV electrons/status word 1 if SSJ5 data"  , 
#                  channel 10, 949 eV electrons"  ,  channel 9, 1392 eV electrons"  , \
#                  channel 16, 139 eV electrons"  ,  channel 15, 204 eV electrons"  , \
#                  channel 14, 300 eV electrons"  ,  channel 13, 440 eV electrons,"  , \
#                  channel 20, 30 eV electrons"  , \
#                  channel 19, 44 eV electrons"  ,  channel 18, 65 eV electrons"  , \
#                  channel 17, 95 eV electrons"  ,  channel 4, 9450 eV ions2"  ,  channel 3, 13900 eV ions 2"  , \
#                  channel 2, 20400 eV ions 2,"  ,  channel 1, 30000 eV ions 2"  , \
#                  channel 8, 2040 eV ions 2"  ,  channel 7, 3000 eV ions 2"  ,  channel 6, 4400 eV ions 2"  , \
#                  channel 5, 6460 eV ions 2"  ,  channel 12, 646 eV ions 2"  ,  channel 11, 949 eV ions2"  , \
#                  channel 10, 949 eV ions2"  ,  channel 9, 1392 eV ions2"  , \
#                  channel 16, 139 eV ions2"  ,  channel 15, 204 eV ions2"  , \
#                  channel 14, 300 eV ions2"  ,  channel 13, 440 eV ions2"  , \
#                  channel 20, 30 eV ions2"  , \
#                  channel 14, 300 eV ions3"  ,  channel 13, 440 eV ions3"  , \
#                  channel 20, 30 eV ions3"  ,  channel 19, 44 eV ions2"  , \
#                  channel 18, 65 eV ions2"  ,  channel 17, 95 eV ions2"  ])
#     columns_names = np.array(['day of year', 'Hour of day', 'Minute of hour', \
#                               'Second of minute', 'Integer year', 'Geodetic latitude', 'Geographic longitude', \
#                                 'Altitude', 'Geographic latitude at 110 km altitude' , \
#                                     'Geographic longitude at 110 km altitude', 
#                                     "corrected geomagnetic latitude", "corrected geomagnetic longitude", \
#                  "hour of magnetic local time", "minute of hour of magnetic local time", \
#                  "second of minute of magnetic local time", \
#                  "hour of day for n second of data", \
#                  "minute of hour for n second of data",\
#                  "second of minute for n second of data", "channel 4, 9450 eV electrons,", "channel 3, 13900 eV electrons, \
# #                 channel 2, 20400 eV electrons, Channel 1, 30000 eV electrons", "channel 8, 2040 eV electrons", \
#                   "channel 7, 3000 eV electrons",  "channel 6, 4400 eV electrons"  , \
#                   "channel 5, 6460 eV electrons"  ,  "channel 12, 646 eV electrons"  , \
#                   "channel 11, 949 eV electrons/status word 1 if SSJ5 data"  , 
#                   "channel 10, 949 eV electrons"  ,  "channel 9, 1392 eV electrons"  , \
#                   "channel 16, 139 eV electrons"  ,  "channel 15, 204 eV electrons"  , \
#                   "channel 14, 300 eV electrons"  ,  "channel 13, 440 eV electrons,"  , \
#                   "channel 20, 30 eV electrons"  , \
#                   "channel 19, 44 eV electrons"  ,  "channel 18, 65 eV electrons"  , \
#                   "channel 17, 95 eV electrons"  ,  "channel 4, 9450 eV ions2"  ,  "channel 3, 13900 eV ions 2"  , \
#                   "channel 2, 20400 eV ions 2,"  ,  "channel 1, 30000 eV ions 2"  , \
#                   "channel 8, 2040 eV ions 2"  ,  "channel 7, 3000 eV ions 2"  ,  "channel 6, 4400 eV ions 2"  , \
#                   "channel 5, 6460 eV ions 2"  ,  "channel 12, 646 eV ions 2"  ,  "channel 11, 949 eV ions2"  , \
#                   "channel 10, 949 eV ions2"  ,  "channel 9, 1392 eV ions2"  , \
#                   "channel 16, 139 eV ions2"  ,  "channel 15, 204 eV ions2"  , \
#                   "channel 14, 300 eV ions2"  ,  "channel 13, 440 eV ions2"  , \
#                   "channel 20, 30 eV ions2"  , \
#                   "channel 14, 300 eV ions3"  ,  "channel 13, 440 eV ions3"  , \
#                   "channel 20, 30 eV ions3"  ,  "channel 19, 44 eV ions2"  , \
#                   "channel 18, 65 eV ions2"  ,  "channel 17, 95 eV ions2"  ])
# file = "/home/eugene/Study/kmod/rgr/f15/ssj/1999/12/j4f1599351" 
# data = np.fromfile(file, dtype=dt)
# df = pd.DataFrame(data) 
with open('/home/eugene/Study/kmod/rgr/f15/ssj/1999/12/j4f1599351', 'rb') as f:

    array  = np.fromfile(f, dtype = ">u2")
    print(array.size)
    j = 0
    for i in range(array.size):

        if array[i] == 0:
            j = j+1
    print(j)
    keys = list(dict.keys())
    new_data = {k: [array[i]] for i, k in enumerate(keys)}
    for i in range(58):
        new_data[list(new_data.keys())[i]] = array[i]
    df = pd.DataFrame(new_data) 
    display(df)
        