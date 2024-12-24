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

def transformToGeophysicalQuantity(valueType, flightNumber, channelType, channel, counts):
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
    "f06": {
        1: 1.8, 2: 1.25, 3: 0.8439, 4: 0.573, 5: 0.3959, 6: 0.2709, 7: 0.1875,
        8: 0.125, 9: 0.08439, 10: 0.05835, 11: 2.437, 12: 1.589, 13: 1.483, 14: 0.8369, 
        15: 0.5827, 16: 0.392, 17: 0.2649, 18: 0.1907, 19: 0.1271, 20: 0.08475
    },
    "f07": {
        1: 2.4, 2: 1.667, 3: 1.146, 4: 0.7814, 5: 0.5418, 6: 0.3647, 7: 0.2501, 
        8: 0.1771, 9: 0.1146, 10: 0.07918, 11: 2.058, 12: 1.372, 13: 0.9603, 14: 0.6467, 
        15: 0.4507, 16: 0.3038, 17: 0.2058, 18: 0.147, 19: 0.09799, 20: 0.06859
    },
    "f08": {
        1: 1.15, 2: 0.8012, 3: 0.5512, 4: 0.3761, 5: 0.2605, 6: 0.175, 7: 0.1198,
        8: 0.08512, 9: 0.05512, 10: 0.03803, 11: 1.096, 12: 0.7315, 13: 0.5123, 14: 0.3445,
        15: 0.2399, 16: 0.1619, 17: 0.1096, 18: 0.07838, 19: 0.05222, 20: 0.03653
    },
    "f09": {
        1: 1.14, 2: 0.7939, 3: 0.5459, 4: 0.372, 5: 0.2584, 6: 0.174, 7: 0.1188,
        8: 0.08439, 9: 0.05459, 10: 0.03772, 11: 1.266, 12: 0.8411, 13: 0.589, 14: 0.3962,
        15: 0.2765, 16: 0.1859, 17: 0.1266, 18: 0.09015, 19: 0.06007, 20: 0.04206
    },
    "f10": {
        1: 0.567, 2: 0.4032, 3: 0.2709, 4: 0.1823, 5: 0.124, 6: 0.08523, 7: 0.05772,
        8: 0.03938, 9: 0.02678, 10: 0.01844, 11: 0.5549, 12: 0.3755, 13: 0.2548, 14: 0.1739,
        15: 0.1196, 16: 0.08097, 17: 0.05549, 18: 0.03821, 19: 0.02636, 20: 0.01794
    },
    "f11": {
        1: 0.549, 2: 0.397, 3: 0.2709, 4: 0.1844, 5: 0.1261, 6: 0.08585, 7: 0.05876,
        8: 0.04032, 9: 0.02771, 10: 0.01844, 11: 0.5818, 12: 0.4065, 13: 0.2787, 14: 0.1939,
        15: 0.1324, 16: 0.09093, 17: 0.0612, 18: 0.04308, 19: 0.02973, 20: 0.02056
    },
    "f12": {
        1: 0.706, 2: 0.5022, 3: 0.3428, 4: 0.2344, 5: 0.1594, 6: 0.1094, 7: 0.07449,
        8: 0.05084, 9: 0.03469, 10: 0.02375, 11: 0.639, 12: 0.4371, 13: 0.2988, 14: 0.2051,
        15: 0.1402, 16: 0.096, 17: 0.06566, 18: 0.04499, 19: 0.03084, 20: 0.02098
    },
    "f13": {
        1: 0.984, 2: 0.6981, 3: 0.4761, 4: 0.324, 5: 0.2209, 6: 0.1511, 7: 0.1027,
        8: 0.07001, 9: 0.04772, 10: 0.03251, 11: 0.5572, 12: 0.03798, 13: 0.02602, 14: 0.01778,
        15: 0.01214, 16: 0.008305, 17: 0.005679, 18: 0.003869, 19: 0.002651, 20: 0.00181
    },
    "f14": { 
        1: 1.33, 2: 0.9408, 3: 0.6397, 4: 0.4355, 5: 0.2959, 6: 0.2011, 7: 0.1365,
        8: 0.09314, 9: 0.06335, 10: 0.04303, 11: 1.008, 12: 0.6877, 13: 0.4705, 14: 0.3206,
        15: 0.2196, 16: 0.1499, 17: 0.1021, 18: 0.0697, 19: 0.04763, 20: 0.03253
    },
    "f15": {
        1: 0.9016, 2: 0.6392, 3: 0.435, 4: 0.296, 5: 0.2014, 6: 0.1371, 7: 0.09328,
        8: 0.06347, 9: 0.0432, 10: 0.02939, 11: 0.9439, 12: 0.6443, 13: 0.4398, 14: 0.3002,
        15: 0.2049, 16: 0.1398, 17: 0.09454, 18: 0.06515, 19: 0.04447, 20: 0.03035
    },
    "f16": {
        1: 13.3, 2: 8.51, 3: 5.43, 4: 3.43, 5: 2.19, 6: 1.4, 7: 0.903,
        8: 0.575, 9: 0.368, 10: 0.244, 12: 0.162, 13: 0.105, 14: 0.0718, 
        15: 0.0505, 16: 0.0342, 17: 0.023, 18: 0.0157, 19: 0.00745, 20: 0.00394
    },
    "f17": {
        1: 5.71, 2: 3.81, 3: 2.54, 4: 1.7, 5: 1.13, 6: 0.715, 7: 0.47,
        8: 0.306, 9: 0.199, 10: 0.122, 12: 0.0899, 13: 0.0581, 14: 0.0307,
        15: 0.017, 16: 0.0101, 17: 0.005, 18: 0.00302, 19: 0.00158, 20: 0.000911
    },
    "f18": {
        1: 10.6, 2: 6.9, 3: 4.51, 4: 2.81, 5: 1.82, 6: 1.19, 7: 0.774,
        8: 0.485, 9: 0.296, 10: 0.208, 12: 0.15, 13: 0.105, 14: 0.0725,
        15: 0.0448, 16: 0.0324, 17: 0.0215, 18: 0.0131, 19: 0.00448, 20: 0.00182
    },
    "f19": {
        1: 3.60, 2: 2.29, 3: 1.45, 4: 0.913, 5: 0.556, 6: 0.360, 7: 0.240,
        8: 0.156, 9: 0.0966, 10: 0.0603, 12: 0.0369, 13: 0.0237, 14: 0.0124,
        15: 0.00855, 16: 0.0059, 17: 0.00436, 18: 0.00258, 19: 0.00156, 20: 0.000929
    },
    "f20": {
        1: 7.06, 2: 4.8, 3: 3.26, 4: 2.06, 5: 1.53, 6: 0.988, 7: 0.65,
        8: 0.416, 9: 0.275, 10: 0.171, 12: 0.102, 13: 0.0718, 14: 0.0454, 
        15: 0.0214, 16: 0.0188, 17: 0.0144, 18: 0.0113, 19: 0.00709, 20: 0.00385
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
    def calculateDifferentialNumberFluxForChannel(channel, counts):
        if channelType == "ions":
            return (counts) / (IonsChannelsGeometricFactors[flightNumber][channel] * 0.098)
        elif channelType == "electrons":
            return (counts) / (ElectronsChannelsGeometricFactors[flightNumber][channel] * 0.098)
    def calculateDifferentialEnergyFluxForChannel(channel, counts):
        return (calculateDifferentialNumberFluxForChannel(channel, counts) * ChannelCentralEnergy[channel])
    def calculateIntegratedNumberFlux(channels):
        #print(channels)
        return sum([calculateDifferentialNumberFluxForChannel(i,counts[i-1]) * ChannelSpasing[i] for i in channels])
    def calculateIntegratedEnergyFlux(channels):
        return sum([calculateIntegratedNumberFlux(channels) * ChannelCentralEnergy[i] * ChannelSpasing[i] for i in channels])
    def calculateMeanEnergy(channels):
        return calculateIntegratedEnergyFlux(channels) / calculateIntegratedNumberFlux(channels)
    
    print(valueType, flightNumber, channelType, channel, counts)
    if valueType == "differential number flux":
        return calculateDifferentialNumberFluxForChannel(channel, counts)
    elif valueType == "differential energy flux":
        return calculateDifferentialEnergyFluxForChannel(channel, counts)
    elif valueType == "integrated number flux":
        return calculateIntegratedNumberFlux(channels=channel[::])
    elif valueType == "integrated energy flux":
        return calculateIntegratedEnergyFlux(channels=channel[::])
    elif valueType == "mean energy":
        return calculateMeanEnergy(channels=channel[::])
    
filename = 'f15/ssj/2005/03/j4f1505060'
filePathVars = filename.split('/')
flightNumber = filePathVars[-1][2:5]
flightYear = filePathVars[-1][5:7]
flightDay = filePathVars[-1][7:10]
#создал эти переменные для проверки дат в названии файла и считаном значении, на поиск ошибок
with open(filename, 'rb') as f:
    array  = np.fromfile(f, dtype = '>u2')
    electronsCounts = []
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
            electronsCounts.append([getCountsFromData(array[21+j*2640+i*43]),
                                    getCountsFromData(array[20+j*2640+i*43]),
                                    getCountsFromData(array[19+j*2640+i*43]),
                                    getCountsFromData(array[18+j*2640+i*43]),
                                    getCountsFromData(array[25+j*2640+i*43]),
                                    getCountsFromData(array[24+j*2640+i*43]),
                                    getCountsFromData(array[23+j*2640+i*43]),
                                    getCountsFromData(array[22+j*2640+i*43]),
                                    getCountsFromData(array[29+j*2640+i*43]),
                                    getCountsFromData(array[28+j*2640+i*43]),
                                    getCountsFromData(array[27+j*2640+i*43]),
                                    getCountsFromData(array[26+j*2640+i*43]),
                                    getCountsFromData(array[33+j*2640+i*43]),
                                    getCountsFromData(array[32+j*2640+i*43]),
                                    getCountsFromData(array[31+j*2640+i*43]),
                                    getCountsFromData(array[30+j*2640+i*43]),
                                    getCountsFromData(array[37+j*2640+i*43]),
                                    getCountsFromData(array[36+j*2640+i*43]),
                                    getCountsFromData(array[35+j*2640+i*43]),
                                    getCountsFromData(array[34+j*2640+i*43])])
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
    print(f'Test for  differential number flux for 13channel of electrons of 2nd second of data for 2nd minute: {transformToGeophysicalQuantity(valueType="differential number flux", flightNumber=flightNumber, channelType="electrons", channel=13, counts=getCountsFromData(array[33+1*2640+1*43]))}')
    print(f'Test for  differential number flux for 4channel of ions of 1st second of data for 2nd minute: {transformToGeophysicalQuantity(valueType="differential number flux", flightNumber=flightNumber, channelType="ions", channel=4, counts=getCountsFromData(array[38+1*2640+0*43]))}')
    print(f'Test for  differential energy flux for 13channel of electorns of 2nd second of data for 2nd minute: {transformToGeophysicalQuantity(valueType="differential energy flux", flightNumber=flightNumber, channelType="electrons", channel=13, counts=getCountsFromData(array[33+1*2640+1*43]))}')
    print(f'Test for  integrated number flux for 1-20 channels of electorns of 2nd second of data for 2nd minute: {transformToGeophysicalQuantity(valueType="integrated number flux", flightNumber=flightNumber, channelType="electrons", channel=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], counts=electronsCounts[3])}')
    # print(f'Test for  integrated energy flux: {transformToGeophysicalQuantity(valueType='', flightNumber=flightNumber, channelType='', channel=(), counts=)}')
    # print(f'Test for  mean energy: {transformToGeophysicalQuantity(valueType='', flightNumber=flightNumber, channelType='', channel=(), counts=)}')
    #print(electronsCounts[3])
    del array
    