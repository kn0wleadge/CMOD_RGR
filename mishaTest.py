import numpy as np
import pandas as pd
from IPython.display import display


#Я тут просто тестировал, разбирал данные, особо ничего интересного, надо будет разобраться с преобразованием данных сенсоров
#Для этого нужно использовать формулы и значения коэффициентов под таблицей из мануала
#Для проверки можно воспользоватся готовой библой по парсингу данного спутника - pydmsp

def getCountsFromData(data):
    '''returns physical data from sensor channel
    if return -1 then no measurement was made
    if return 0 then measurment was made but no counts detected
    else return counts'''
    X = data % 32
    Y = (data - X) / 32
    counts = (X + 32) * pow(2,Y) - 33
    return counts

def transformToGeophysicalQuantity(valueType, flightYear, channelType, channel, counts):
    '''return geophysical value such as\n
    differential number flux |
    differential energy flux |
    integrated number flux |
    integrated energy flux |
    mean energy \n
    result depends on selected type of value, flight year, type of channel (ions or electrons), channel and counts'''
    ElectronsChannelsGeometricFactors = {
    "f06": {
        1: 0.75, 2: 0.49, 3: 0.41, 4: 0.33, 5: 0.27, 6: 0.21, 7: 0.16, 8: 0.13, 9: 0.096, 10: 0.076,
        11: 0.0157, 12: 0.01122, 13: 0.008974, 14: 0.005721, 15: 0.003814, 16: 0.002243, 17: 0.001122, 18: 0.0005609, 19: 0.0002243, 20: 0.00007067
    },
    "f07": {
        1: 0.58, 2: 0.49, 3: 0.41, 4: 0.33, 5: 0.27, 6: 0.21, 7: 0.16, 8: 0.13, 9: 0.096, 10: 0.076,
        11: 0.032, 12: 0.02424, 13: 0.01939, 14: 0.01261, 15: 0.008824, 16: 0.005624, 17: 0.003297, 18: 0.001939, 19: 0.001067, 20: 0.0005527
    },
    "f08": {
        1: 0.326, 2: 0.275, 3: 0.23, 4: 0.185, 5: 0.152, 6: 0.118, 7: 0.0899, 8: 0.073, 9: 0.0539, 10: 0.0427,
        11: 0.03163, 12: 0.02402, 13: 0.01917, 14: 0.01245, 15: 0.008737, 16: 0.005564, 17: 0.003261, 18: 0.001917, 19: 0.001057, 20: 0.0005465
    },
    "f09": {
        1: 0.201, 2: 0.17, 3: 0.142, 4: 0.115, 5: 0.0937, 6: 0.0729, 7: 0.0555, 8: 0.0451, 9: 0.0333, 10: 0.0264,
        11: 0.03688, 12: 0.02797, 13: 0.02234, 14: 0.01455, 15: 0.01014, 16: 0.006467, 17: 0.003801, 18: 0.002234, 19: 0.001229, 20: 0.0006363
    },
    "f10": {
        1: 0.462, 2: 0.389, 3: 0.302, 4: 0.243, 5: 0.194, 6: 0.158, 7: 0.126, 8: 0.102, 9: 0.0824, 10: 0.0669,
        11: 0.05206, 12: 0.03714, 13: 0.02506, 14: 0.0174, 15: 0.01219, 16: 0.006839, 17: 0.003697, 18: 0.001952, 19: 0.0009389, 20: 0.0003628
    },
    "f11": {
        1: 0.631, 2: 0.544, 3: 0.428, 4: 0.349, 5: 0.278, 6: 0.226, 7: 0.182, 8: 0.149, 9: 0.121, 10: 0.095,
        11: 0.1092, 12: 0.07788, 13: 0.05345, 14: 0.03585, 15: 0.0246, 16: 0.01391, 17: 0.007392, 18: 0.003907, 19: 0.001846, 20: 0.0006987
    },
    "f12": {
        1: 0.4552, 2: 0.3815, 3: 0.3188, 4: 0.2661, 5: 0.2232, 6: 0.1858, 7: 0.1561, 8: 0.1297, 9: 0.1088, 10: 0.09103,
        11: 0.06909, 12: 0.04888, 13: 0.03279, 14: 0.02248, 15: 0.01536, 16: 0.008516, 17: 0.004523, 18: 0.002338, 19: 0.001094, 20: 0.0004161
    },
    "f13": {
        1: 0.456, 2: 0.362, 3: 0.287, 4: 0.228, 5: 0.181, 6: 0.144, 7: 0.114, 8: 0.0908, 9: 0.0721, 10: 0.0572,
        11: 0.03644, 12: 0.02615, 13: 0.01777, 14: 0.01232, 15: 0.008563, 16: 0.004827, 17: 0.002598, 18: 0.001359, 19: 0.0006463, 20: 0.0002496
    },
    "f14": {
        1: 0.334, 2: 0.272, 3: 0.222, 4: 0.181, 5: 0.148, 6: 0.121, 7: 0.0985, 8: 0.0803, 9: 0.0656, 10: 0.0535,
        11: 0.03939, 12: 0.02828, 13: 0.0193, 14: 0.01345, 15: 0.009314, 16: 0.005287, 17: 0.002839, 18: 0.001488, 19: 0.000714, 20: 0.0002746
    },
    "f15": {
        1: 0.3124, 2: 0.2528, 3: 0.2046, 4: 0.1657, 5: 0.1341, 6: 0.1086, 7: 0.0879, 8: 0.07116, 9: 0.0576, 10: 0.04662,
        11: 0.05072, 12: 0.03647, 13: 0.02488, 14: 0.01733, 15: 0.01205, 16: 0.006807, 17: 0.003672, 18: 0.001928, 19: 0.0009189, 20: 0.000356
    },
    "f16": {
        1: 1.781, 2: 1.477, 3: 1.188, 4: 0.935, 5: 0.722, 6: 0.551, 7: 0.416, 8: 0.306, 9: 0.225, 10: 0.166,
        11: 0.0, 12: 0.123, 13: 0.0876, 14: 0.0613, 15: 0.0429, 16: 0.0289, 17: 0.0182, 18: 0.0113, 19: 0.00621, 20: 0.00307
    },
    "f17": {
        1: 1.044, 2: 0.808, 3: 0.602, 4: 0.458, 5: 0.349, 6: 0.262, 7: 0.191, 8: 0.142, 9: 0.103, 10: 0.0727,
        11: 0.0, 12: 0.0541, 13: 0.0394, 14: 0.0276, 15: 0.0188, 16: 0.0134, 17: 0.00901, 18: 0.00645, 19: 0.00445, 20: 0.00294
    },
    "f18": {
        1: 0.725, 2: 0.534, 3: 0.412, 4: 0.315, 5: 0.266, 6: 0.199, 7: 0.147, 8: 0.107, 9: 0.0803, 10: 0.0562,
        11: 0.0, 12: 0.041, 13: 0.0296, 14: 0.0203, 15: 0.0144, 16: 0.0104, 17: 0.00708, 18: 0.00562, 19: 0.00386, 20: 0.00239
    },
    "f19": {
        1: 3.735, 2: 2.885, 3: 2.196, 4: 1.615, 5: 1.17, 6: 0.832, 7: 0.605, 8: 0.418, 9: 0.28, 10: 0.197,
        11: 0.0, 12: 0.134, 13: 0.0958, 14: 0.064, 15: 0.0445, 16: 0.0312, 17: 0.0204, 18: 0.0083, 19: 0.00222, 20: 0.000639
    },
    "f20": {
        1: 2.992, 2: 2.101, 3: 1.532, 4: 1.08, 5: 0.782, 6: 0.539, 7: 0.389, 8: 0.295, 9: 0.186, 10: 0.128,
        11: 0.0, 12: 0.0825, 13: 0.0516, 14: 0.0351, 15: 0.0235, 16: 0.0175, 17: 0.00975, 18: 0.00723, 19: 0.0041, 20: 0.00193
    }
}
    IonsChannelsGeometricFactors = {
        "f15": {
        1: 0.9016, 2: 0.6392, 3: 0.435, 4: 0.296, 5: 0.2014, 6: 0.1371, 7: 0.09328, 8: 0.06347, 9: 0.0432, 10: 0.02939,
        11: 0.9439, 12: 0.6443, 13: 0.4398, 14: 0.3002, 15: 0.2049, 16: 0.1398, 17: 0.09454, 18: 0.06515, 19: 0.04447, 20: 0.03035
    }
}
    ChannelCentralEnergy = {
        1: 30000, 2: 20400, 3: 13900, 4: 9450, 5: 6460, 6: 4400, 7: 3000, 8: 2040, 9: 1392, 10: 949,
        11: 949, 12: 646, 13: 440, 14: 300, 15: 204, 16: 139, 17: 95, 18: 65, 19: 44, 20: 30,
    }
    ChannelSpasing = {
        1: 9600, 2: 8050, 3: 5475, 4: 3720, 5:2525, 6: 1730, 7: 1180, 8: 804, 9: 545.5, 10: 373,
        11: 373, 12: 254.5, 13: 173, 14: 118, 15: 80.5, 16: 54.5, 17: 37, 18: 25.5, 19: 17, 20: 14,
    }
    
    
filename = 'f15/ssj/2005/03/j4f1505060'
filePathVars = filename.split('/')
flightNumber = filePathVars[-1][2:5]
flightYear = filePathVars[-1][5:7]
flightDay = filePathVars[-1][7:10]
#создал эти переменные для проверки дат в названии файла и считаном значении, на поиск ошибок
with open(filename, 'rb') as f:
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
        for i in range(2):
            print(f"Hour of day for {i+1} second of data: ", array[15+j*2640+i*43])
            print(f"Minute of hour for {i+1} second of data: ", array[16+j*2640+i*43])
            print(f"Second of minute for {i+1} second of data: ", float(array[17+j*2640+i*43])/1000.0 if array[2595+j*2640] == 1 else array[17+j*2640+i*43])
            print(f"Chanel 1, 30000 eV electrons, counts: {getCountsFromData(array[21+j*2640+i*43])}")
            print(f"Chanel 2, 20400 eV electrons, counts: {getCountsFromData(array[20+j*2640+i*43])}")
            print(f"Chanel 3, 13900 eV electrons, counts: {getCountsFromData(array[19+j*2640+i*43])}")
            print(f"Chanel 4, 9450 eV electrons, counts: {getCountsFromData(array[18+j*2640+i*43])}")
            print(f"Chanel 5, 6460 eV electrons, counts: {getCountsFromData(array[25+j*2640+i*43])}")
            print(f"Chanel 6, 4400 eV electrons, counts: {getCountsFromData(array[24+j*2640+i*43])}")
            print(f"Chanel 7, 3000 eV electrons, counts: {getCountsFromData(array[23+j*2640+i*43])}")
            print(f"Chanel 8, 2040 eV electrons, counts: {getCountsFromData(array[22+j*2640+i*43])}")
            print(f"Chanel 9, 1392 eV electrons, counts: {getCountsFromData(array[29+j*2640+i*43])}")
            print(f"Chanel 10, 949 eV electrons, counts: {getCountsFromData(array[28+j*2640+i*43])}") #вообще в нашей выборке файлов нету сенсоров ssj5, так что это всегда будет инфой, а не статус вордом
            print(f"Chanel 11, 949 eV electrons, counts: {getCountsFromData(array[27+j*2640+i*43])}")
            print(f"Chanel 12, 646 eV electrons, counts: {getCountsFromData(array[26+j*2640+i*43])}")
            print(f"Chanel 13, 440 eV electrons, counts: {getCountsFromData(array[33+j*2640+i*43])}")
            print(f"Chanel 14, 300 eV electrons, counts: {getCountsFromData(array[32+j*2640+i*43])}")
            print(f"Chanel 15, 204 eV electrons, counts: {getCountsFromData(array[31+j*2640+i*43])}")
            print(f"Chanel 16, 139 eV electrons, counts: {getCountsFromData(array[30+j*2640+i*43])}")
            print(f"Chanel 17, 95 eV electrons, counts: {getCountsFromData(array[37+j*2640+i*43])}")
            print(f"Chanel 18, 65 eV electrons, counts: {getCountsFromData(array[36+j*2640+i*43])}")
            print(f"Chanel 19, 44 eV electrons, counts: {getCountsFromData(array[35+j*2640+i*43])}")
            print(f"Chanel 20, 30 eV electrons, counts: {getCountsFromData(array[34+j*2640+i*43])}")
            
            print(f"Chanel 1, 30000 eV ions, counts: {getCountsFromData(array[41+j*2640+i*43])}")
            print(f"Chanel 2, 20400 eV ions, counts: {getCountsFromData(array[40+j*2640+i*43])}")
            print(f"Chanel 3, 13900 eV ions, counts: {getCountsFromData(array[39+j*2640+i*43])}")
            print(f"Chanel 4, 9450 eV ions, counts: {getCountsFromData(array[38+j*2640+i*43])}")
            print(f"Chanel 5, 6460 eV ions, counts: {getCountsFromData(array[45+j*2640+i*43])}")
            print(f"Chanel 6, 4400 eV ions, counts: {getCountsFromData(array[44+j*2640+i*43])}")
            print(f"Chanel 7, 3000 eV ions, counts: {getCountsFromData(array[43+j*2640+i*43])}")
            print(f"Chanel 8, 2040 eV ions, counts: {getCountsFromData(array[42+j*2640+i*43])}")
            print(f"Chanel 9, 1392 eV ions, counts: {getCountsFromData(array[49+j*2640+i*43])}")
            print(f"Chanel 10, 949 eV ions, counts: {getCountsFromData(array[48+j*2640+i*43])}")#вообще в нашей выборке файлов нету сенсоров ssj5, так что это всегда будет инфой, а не статус вордом
            print(f"Chanel 11, 949 eV ions, counts: {getCountsFromData(array[47+j*2640+i*43])}")
            print(f"Chanel 12, 646 eV ions, counts: {getCountsFromData(array[46+j*2640+i*43])}")
            print(f"Chanel 13, 440 eV ions, counts: {getCountsFromData(array[53+j*2640+i*43])}")
            print(f"Chanel 14, 300 eV ions, counts: {getCountsFromData(array[52+j*2640+i*43])}")
            print(f"Chanel 15, 204 eV ions, counts: {getCountsFromData(array[51+j*2640+i*43])}")
            print(f"Chanel 16, 139 eV ions, counts: {getCountsFromData(array[50+j*2640+i*43])}")
            print(f"Chanel 17, 95 eV ions, counts: {getCountsFromData(array[57+j*2640+i*43])}")
            print(f"Chanel 18, 65 eV ions, counts: {getCountsFromData(array[56+j*2640+i*43])}")
            print(f"Chanel 19, 44 eV ions, counts: {getCountsFromData(array[55+j*2640+i*43])}")
            print(f"Chanel 20, 30 eV ions, counts: {getCountsFromData(array[54+j*2640+i*43])}")
        print(array[2595+j*2640]) # flag for ms time or s time
        print(array[2596+j*2640:2640+j*2640]) #zero fills
    
    del array
    