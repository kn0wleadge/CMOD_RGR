import numpy as np
import pandas as pd
from IPython.display import display
import gc

#Я тут просто тестировал, разбирал данные, особо ничего интересного, надо будет разобраться с преобразованием данных сенсоров
#Для этого нужно использовать формулы и значения коэффициентов под таблицей из мануала
#Для проверки можно воспользоватся готовой библой по парсингу данного спутника - pydmsp

with open('f15/ssj/1999/12/j4f1599351', 'rb') as f:
    array  = np.fromfile(f, dtype = '>u2')
    print(array.size)
    #Шапка для i-ой минуты
    print("Day of year: ", array[0])
    print("Hour of day: ", array[1])
    print("Minute of hour: ", array[2])
    print("Second of minute: ", array[3])
    print("Integer year: ", 1987 + array[4])
    print("Geodetic latitude: ", float(array[5] - 4995)/10.0 if array[5] > 1800 else float(array[5]-900)/10.0)
    print("Geodetic longitude: ", float(array[6])/10.0)
    print("Altitude, nautical miles", array[7])
    print("Geographic latitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft: ", float(array[8] - 4995)/10.0 if array[8] > 1800 else float(array[8]-900)/10.0)
    print("Geographic longitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft: ", float(array[9]/10.0))
    print("Corrected geomagnetic latitude at 110km: ", float(array[10] - 4995)/10.0 if array[10] > 1800 else float(array[10]-900)/10.0)
    print("Corrected geomagnetic longitude at 100km: ", float(array[11]/10.0))
    print("Hour of magnetic local time: ", array[12])
    print("Minute of hour of magnetic local time: ", array[13])
    print("Second of minute of magnetic local time: ", array[14])
    #i-я секунда
    for i in range(60):
        print(f"Hour of day for {i+1} second of data: ", array[15+i*43])
        print(f"Minute of hour for {i+1} second of data: ", array[16+i*43])
        print(f"Second of minute for {i+1} second of data: ", float(array[17+i*43]/1000.0) if array[2595] == 1 else array[17+i*43])
    
    
    del array
print("Garbage collected: ",gc.collect())