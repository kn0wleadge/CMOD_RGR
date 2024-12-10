import numpy as np
import pandas as pd
from IPython.display import display


#Я тут просто тестировал, разбирал данные, особо ничего интересного, надо будет разобраться с преобразованием данных сенсоров
#Для этого нужно использовать формулы и значения коэффициентов под таблицей из мануала
#Для проверки можно воспользоватся готовой библой по парсингу данного спутника - pydmsp

with open('f15/ssj/2005/03/j4f1505060', 'rb') as f:
    array  = np.fromfile(f, dtype = '>u2')
    print(array.size)
    print(minutesOfData := array.size / 2640)
    #Шапка для i-ой минуты
    for (j) in range(2): #minutesOfData):
        print(f'Data for {j + 1} minute of data:')
        print("Day of year: ", array[0 + j*2640])
        print("Hour of day: ", array[1 + j*2640])
        print("Minute of hour: ", array[2 + j*2640])
        print("Second of minute: ", array[3 + j*2640])
        print("Integer year: ", 1950 + array[4 + j*2640])
        print("Geodetic latitude: ", float(array[5 + j*2640]) - 4995/10.0 if array[5 + j*2640] > 1800 else float(array[5 + j*2640])-900/10.0)
        print("Geodetic longitude: ", float(array[6 + j*2640])/10.0)
        print("Altitude, nautical miles", array[7 + j*2640])
        print("Geographic latitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft: ", float(array[8 + j*2640]) - 4995/10.0 if array[8 + j*2640] > 1800 else float(array[8 + j*2640])-900/10.0)
        print("Geographic longitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft: ", float(array[9 + j*2640]/10.0))
        print("Corrected geomagnetic latitude at 110km: ", float(array[10 + j*2640]) - 4995/10.0 if array[10 + j*2640] > 1800 else float(array[10 + j*2640])-900/10.0)
        print("Corrected geomagnetic longitude at 100km: ", float(array[11 + j*2640]/10.0))
        print("Hour of magnetic local time: ", array[12 + j*2640])
        print("Minute of hour of magnetic local time: ", array[13 + j*2640])
        print("Second of minute of magnetic local time: ", array[14 + j*2640])
        #i-я секунда
        for i in range(60):
            print(f"Hour of day for {i+1} second of data: ", array[15+j*2640+i*43])
            print(f"Minute of hour for {i+1} second of data: ", array[16+j*2640+i*43])
            print(f"Second of minute for {i+1} second of data: ", float(array[17+j*2640+i*43])/1000.0 if array[2595+j*2640] == 1 else array[17+j*2640+i*43])
            print(f"Chanel 1, 30000 eV electrons, raw data: {array[21+j*2640+i*43]}")
            print(f"Chanel 2, 20400 eV electrons, raw data: {array[20+j*2640+i*43]}")
            print(f"Chanel 3, 13900 eV electrons, raw data: {array[19+j*2640+i*43]}")
            print(f"Chanel 4, 9450 eV electrons, raw data: {array[18+j*2640+i*43]}")
            print(f"Chanel 5, 6460 eV electrons, raw data: {array[25+j*2640+i*43]}")
            print(f"Chanel 6, 4400 eV electrons, raw data: {array[24+j*2640+i*43]}")
            print(f"Chanel 7, 3000 eV electrons, raw data: {array[23+j*2640+i*43]}")
            print(f"Chanel 8, 2040 eV electrons, raw data: {array[22+j*2640+i*43]}")
            print(f"Chanel 9, 1392 eV electrons, raw data: {array[29+j*2640+i*43]}")
            print(f"Chanel 10, 949 eV electrons, raw data, or status word 1 for ssj5: {array[28+j*2640+i*43]}")#вообще в нашей выборке файлов нету сенсоров ssj5, так что это всегда будет инфой, а не статус вордом
            print(f"Chanel 11, 949 eV electrons, raw data: {array[27+j*2640+i*43]}")
            print(f"Chanel 12, 646 eV electrons, raw data: {array[26+j*2640+i*43]}")
            print(f"Chanel 13, 440 eV electrons, raw data: {array[33+j*2640+i*43]}")
            print(f"Chanel 14, 300 eV electrons, raw data: {array[32+j*2640+i*43]}")
            print(f"Chanel 15, 204 eV electrons, raw data: {array[31+j*2640+i*43]}")
            print(f"Chanel 16, 139 eV electrons, raw data: {array[30+j*2640+i*43]}")
            print(f"Chanel 17, 95 eV electrons, raw data: {array[37+j*2640+i*43]}")
            print(f"Chanel 18, 65 eV electrons, raw data: {array[36+j*2640+i*43]}")
            print(f"Chanel 19, 44 eV electrons, raw data: {array[35+j*2640+i*43]}")
            print(f"Chanel 20, 30 eV electrons, raw data: {array[34+j*2640+i*43]}")
            
            print(f"Chanel 1, 30000 eV ions, raw data: {array[41+j*2640+i*43]}")
            print(f"Chanel 2, 20400 eV ions, raw data: {array[40+j*2640+i*43]}")
            print(f"Chanel 3, 13900 eV ions, raw data: {array[39+j*2640+i*43]}")
            print(f"Chanel 4, 9450 eV ions, raw data: {array[38+j*2640+i*43]}")
            print(f"Chanel 5, 6460 eV ions, raw data: {array[45+j*2640+i*43]}")
            print(f"Chanel 6, 4400 eV ions, raw data: {array[44+j*2640+i*43]}")
            print(f"Chanel 7, 3000 eV ions, raw data: {array[43+j*2640+i*43]}")
            print(f"Chanel 8, 2040 eV ions, raw data: {array[42+j*2640+i*43]}")
            print(f"Chanel 9, 1392 eV ions, raw data: {array[49+j*2640+i*43]}")
            print(f"Chanel 10, 949 eV ions, raw data, or status word 2 for ssj5: {array[48+j*2640+i*43]}")#вообще в нашей выборке файлов нету сенсоров ssj5, так что это всегда будет инфой, а не статус вордом
            print(f"Chanel 11, 949 eV ions, raw data: {array[47+j*2640+i*43]}")
            print(f"Chanel 12, 646 eV ions, raw data: {array[46+j*2640+i*43]}")
            print(f"Chanel 13, 440 eV ions, raw data: {array[53+j*2640+i*43]}")
            print(f"Chanel 14, 300 eV ions, raw data: {array[52+j*2640+i*43]}")
            print(f"Chanel 15, 204 eV ions, raw data: {array[51+j*2640+i*43]}")
            print(f"Chanel 16, 139 eV ions, raw data: {array[50+j*2640+i*43]}")
            print(f"Chanel 17, 95 eV ions, raw data: {array[57+j*2640+i*43]}")
            print(f"Chanel 18, 65 eV ions, raw data: {array[56+j*2640+i*43]}")
            print(f"Chanel 19, 44 eV ions, raw data: {array[55+j*2640+i*43]}")
            print(f"Chanel 20, 30 eV ions, raw data: {array[54+j*2640+i*43]}")
        #array[2595+j*2640] - flag for ms time or s time
        #array[from 2596+j*2640 to 2640+j*2640] zero fills
    
    del array