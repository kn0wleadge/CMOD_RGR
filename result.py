import numpy as np
import xarray as xr
from unzip import unzip

def createTransformedDataVariablesSet(filename):
    path = filename
    if filename.find(".gz",0) != -1:
        unzip(filename)
        path = filename[0:len(path) - 3]
    with open(path, 'rb') as f:
        array = np.fromfile(f, dtype = '>u2')
        minutesOfData = int(array.size / 2640)
        result = np.empty((minutesOfData, 15), dtype=np.float16)
        for (j) in range(minutesOfData):
            result[j, 0] = array[0 + j*2640] #Day of year
            result[j, 1] = array[1 + j*2640] #Hour of day
            result[j, 2] = array[2 + j*2640] #Minute of hour
            result[j, 3] = array[3 + j*2640] #Second of minute
            result[j, 4] = 1950 + array[4 + j*2640] #Integer year
            result[j, 5] = float(array[5 + j*2640]) - 4995/10.0 if array[5 + j*2640] > 1800 else float(array[5 + j*2640])-900/10.0 #Geodetic latitude
            result[j, 6] = float(array[6 + j*2640])/10.0 #Geodetic longitude
            result[j, 7] = array[7 + j*2640] #Altitude, nautical miles
            result[j, 8] = float(array[8 + j*2640]) - 4995/10.0 if array[8 + j*2640] > 1800 else float(array[8 + j*2640])-900/10.0 #Geographic latitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft
            result[j, 9] = float(array[9 + j*2640]/10.0) #Geographic longitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft
            result[j, 10] = float(array[10 + j*2640]) - 4995/10.0 if array[10 + j*2640] > 1800 else float(array[10 + j*2640])-900/10.0 #Corrected geomagnetic latitude at 110km
            result[j, 11] = float(array[11 + j*2640]/10.0) #Corrected geomagnetic longitude at 100km
            result[j, 12] = array[12 + j*2640] #Hour of magnetic local time
            result[j, 13] = array[13 + j*2640] #Minute of hour of magnetic local time
            result[j, 14] = array[14 + j*2640] #Second of minute of magnetic local time
        del array
        #TODO: возвращать Dataset
        return result
    
    
def createRawDataVariablesSet(filename):
    path = filename
    if filename.find(".gz",0) != -1:
        unzip(filename)
        path = filename[0:len(path) - 3]
    with open(path, 'rb') as f:
        array = np.fromfile(f, dtype = '>u2')
        minutesOfData = int(array.size / 2640)
        result = np.empty((minutesOfData, 15), dtype='>u2')
        for (j) in range(minutesOfData):
            result[j][0] = array[0 + j*2640] #Day of year
            result[j][1] = array[1 + j*2640] #Hour of day
            result[j][2] = array[2 + j*2640] #Minute of hour
            result[j][3] = array[3 + j*2640] #Second of minute
            result[j][4] = array[4 + j*2640] #Integer year
            result[j][5] = array[5 + j*2640] #Geodetic latitude
            result[j][6] = array[6 + j*2640] #Geodetic longitude
            result[j][7] = array[7 + j*2640] #Altitude, nautical miles
            result[j][8] = array[8 + j*2640] #Geographic latitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft
            result[j][9] = array[9 + j*2640] #Geographic longitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft
            result[j][10] = array[10 + j*2640] #Corrected geomagnetic latitude at 110km
            result[j][11] = array[11 + j*2640] #Corrected geomagnetic longitude at 100km
            result[j][12] = array[12 + j*2640] #Hour of magnetic local time
            result[j][13] = array[13 + j*2640] #Minute of hour of magnetic local time
            result[j][14] = array[14 + j*2640] #Second of minute of magnetic local time
        del array
        #TODO: возвращать Dataset
        return result
    
    
def getCountsFromData(data):
    '''returns physical data from sensor channel
    if return -1 then no measurement was made
    if return 0 then measurment was made but no counts detected
    else return counts'''
    X = data % 32
    Y = (data - X) / 32
    counts = (X + 32) * pow(2,Y) - 33
    return counts
def createTransformedDataMeasuresSet(filename):
    path = filename
    if filename.find(".gz",0) != -1:
        unzip(filename)
        path = filename[0:len(path) - 3]
    with open(path, 'rb') as f:
        array = np.fromfile(f, dtype = '>u2')
        minutesOfData = int(array.size / 2640)
        result = np.empty((minutesOfData*60, 43), dtype=np.int32)
        for (j) in range(minutesOfData):
            result[j][0] = array[15+(j // 60)*2640+(j % 60)*43] # Hour of day for {i+1} second of data
            result[j][1] = array[16+(j // 60)*2640+(j % 60)*43] # Minute of hour for {i+1} second of data
            if array[2595+(j // 60)*2640] == 1:
                result[j][2] =  array[17+(j // 60)*2640+(j % 60)*43]#MS of minute for {i+1} second of data
            else:
                result[j][2] =  array[17+(j // 60)*2640+(j % 60)*43] * 1000 #MS of minute for {i+1} second of data
            result[j][3] =  getCountsFromData(array[21+(j // 60)*2640+(j % 60)*43]) #Chanel 1, 30000 eV electrons
            result[j][4] =  getCountsFromData(array[20+(j // 60)*2640+(j % 60)*43]) #Chanel 2, 20400 eV electrons
            result[j][5] =  getCountsFromData(array[19+(j // 60)*2640+(j % 60)*43]) #Chanel 3, 13900 eV electrons
            result[j][6] =  getCountsFromData(array[18+(j // 60)*2640+(j % 60)*43]) #Chanel 4, 9450 eV electrons
            result[j][7] =  getCountsFromData(array[25+(j // 60)*2640+(j % 60)*43]) #Chanel 5, 6460 eV electrons
            result[j][8] =  getCountsFromData(array[24+(j // 60)*2640+(j % 60)*43]) #Chanel 6, 4400 eV electrons
            result[j][9] =  getCountsFromData(array[23+(j // 60)*2640+(j % 60)*43]) #Chanel 7, 3000 eV electrons
            result[j][10] = getCountsFromData(array[22+(j // 60)*2640+(j % 60)*43]) #Chanel 8, 2040 eV electrons
            result[j][11] = getCountsFromData(array[29+(j // 60)*2640+(j % 60)*43]) #Chanel 9, 1392 eV electrons
            result[j][12] = getCountsFromData(array[28+(j // 60)*2640+(j % 60)*43]) #Chanel 10, 949 eV electrons 
            result[j][13] = getCountsFromData(array[27+(j // 60)*2640+(j % 60)*43]) #Chanel 11, 949 eV electrons
            result[j][14] = getCountsFromData(array[26+(j // 60)*2640+(j % 60)*43]) #Chanel 12, 646 eV electrons
            result[j][15] = getCountsFromData(array[33+(j // 60)*2640+(j % 60)*43]) #Chanel 13, 440 eV electrons
            result[j][16] = getCountsFromData(array[32+(j // 60)*2640+(j % 60)*43]) #Chanel 14, 300 eV electrons
            result[j][17] = getCountsFromData(array[31+(j // 60)*2640+(j % 60)*43]) #Chanel 15, 204 eV electrons
            result[j][18] = getCountsFromData(array[30+(j // 60)*2640+(j % 60)*43]) #Chanel 16, 139 eV electrons
            result[j][19] = getCountsFromData(array[37+(j // 60)*2640+(j % 60)*43]) #Chanel 17, 95 eV electrons
            result[j][20] = getCountsFromData(array[36+(j // 60)*2640+(j % 60)*43]) #Chanel 18, 65 eV electrons
            result[j][21] = getCountsFromData(array[35+(j // 60)*2640+(j % 60)*43]) #Chanel 19, 44 eV electrons
            result[j][22] = getCountsFromData(array[34+(j // 60)*2640+(j % 60)*43]) #Chanel 20, 30 eV electrons
            result[j][23] = getCountsFromData(array[41+(j // 60)*2640+(j % 60)*43]) #Chanel 1, 30000 eV ions
            result[j][24] = getCountsFromData(array[40+(j // 60)*2640+(j % 60)*43]) #Chanel 2, 20400 eV ions
            result[j][25] = getCountsFromData(array[39+(j // 60)*2640+(j % 60)*43]) #Chanel 3, 13900 eV ions
            result[j][26] = getCountsFromData(array[38+(j // 60)*2640+(j % 60)*43]) #Chanel 4, 9450 eV ions
            result[j][27] = getCountsFromData(array[45+(j // 60)*2640+(j % 60)*43]) #Chanel 5, 6460 eV ions
            result[j][28] = getCountsFromData(array[44+(j // 60)*2640+(j % 60)*43]) #Chanel 6, 4400 eV ions
            result[j][29] = getCountsFromData(array[43+(j // 60)*2640+(j % 60)*43]) #Chanel 7, 3000 eV ions
            result[j][30] = getCountsFromData(array[42+(j // 60)*2640+(j % 60)*43]) #Chanel 8, 2040 eV ions
            result[j][31] = getCountsFromData(array[49+(j // 60)*2640+(j % 60)*43]) #Chanel 9, 1392 eV ions
            result[j][32] = getCountsFromData(array[48+(j // 60)*2640+(j % 60)*43]) #Chanel 10, 949 eV ions
            result[j][33] = getCountsFromData(array[47+(j // 60)*2640+(j % 60)*43]) #Chanel 11, 949 eV ions
            result[j][34] = getCountsFromData(array[46+(j // 60)*2640+(j % 60)*43]) #Chanel 12, 646 eV ions
            result[j][35] = getCountsFromData(array[53+(j // 60)*2640+(j % 60)*43]) #Chanel 13, 440 eV ions
            result[j][36] = getCountsFromData(array[52+(j // 60)*2640+(j % 60)*43]) #Chanel 14, 300 eV ions
            result[j][37] = getCountsFromData(array[51+(j // 60)*2640+(j % 60)*43]) #Chanel 15, 204 eV ions
            result[j][38] = getCountsFromData(array[50+(j // 60)*2640+(j % 60)*43]) #Chanel 16, 139 eV ions
            result[j][39] = getCountsFromData(array[57+(j // 60)*2640+(j % 60)*43]) #Chanel 17, 95 eV ions
            result[j][40] = getCountsFromData(array[56+(j // 60)*2640+(j % 60)*43]) #Chanel 18, 65 eV ions
            result[j][41] = getCountsFromData(array[55+(j // 60)*2640+(j % 60)*43]) #Chanel 19, 44 eV ions
            result[j][42] = getCountsFromData(array[54+(j // 60)*2640+(j % 60)*43]) #Chanel 20, 30 eV ions
        #TODO: возвращать дата сет
        del array
        return result
    

def createRawDataMeasuresSet(filename):
    path = filename
    if filename.find(".gz",0) != -1:
        unzip(filename)
        path = filename[0:len(path) - 3]
    with open(path, 'rb') as f:
        array = np.fromfile(f, dtype = '>u2')
        minutesOfData = int(array.size / 2640)
        result = np.empty((minutesOfData*60, 43), dtype=np.uint16)
        for (j) in range(minutesOfData*60):
            result[j][0] =  array[15+(j // 60)*2640+(j % 60)*43] # Hour of day for {i+1} second of data
            result[j][1] =  array[16+(j // 60)*2640+(j % 60)*43] # Minute of hour for {i+1} second of data
            result[j][2] =  array[17+(j // 60)*2640+(j % 60)*43] #Second of minute for {i+1} second of data
            result[j][3] =  array[21+(j // 60)*2640+(j % 60)*43] #Chanel 1, 30000 eV electrons
            result[j][4] =  array[20+(j // 60)*2640+(j % 60)*43] #Chanel 2, 20400 eV electrons
            result[j][5] =  array[19+(j // 60)*2640+(j % 60)*43] #Chanel 3, 13900 eV electrons
            result[j][6] =  array[18+(j // 60)*2640+(j % 60)*43] #Chanel 4, 9450 eV electrons
            result[j][7] =  array[25+(j // 60)*2640+(j % 60)*43] #Chanel 5, 6460 eV electrons
            result[j][8] =  array[24+(j // 60)*2640+(j % 60)*43] #Chanel 6, 4400 eV electrons
            result[j][9] =  array[23+(j // 60)*2640+(j % 60)*43] #Chanel 7, 3000 eV electrons
            result[j][10] = array[22+(j // 60)*2640+(j % 60)*43] #Chanel 8, 2040 eV electrons
            result[j][11] = array[29+(j // 60)*2640+(j % 60)*43] #Chanel 9, 1392 eV electrons
            result[j][12] = array[28+(j // 60)*2640+(j % 60)*43] #Chanel 10, 949 eV electrons 
            result[j][13] = array[27+(j // 60)*2640+(j % 60)*43] #Chanel 11, 949 eV electrons
            result[j][14] = array[26+(j // 60)*2640+(j % 60)*43] #Chanel 12, 646 eV electrons
            result[j][15] = array[33+(j // 60)*2640+(j % 60)*43] #Chanel 13, 440 eV electrons
            result[j][16] = array[32+(j // 60)*2640+(j % 60)*43] #Chanel 14, 300 eV electrons
            result[j][17] = array[31+(j // 60)*2640+(j % 60)*43] #Chanel 15, 204 eV electrons
            result[j][18] = array[30+(j // 60)*2640+(j % 60)*43] #Chanel 16, 139 eV electrons
            result[j][19] = array[37+(j // 60)*2640+(j % 60)*43] #Chanel 17, 95 eV electrons
            result[j][20] = array[36+(j // 60)*2640+(j % 60)*43] #Chanel 18, 65 eV electrons
            result[j][21] = array[35+(j // 60)*2640+(j % 60)*43] #Chanel 19, 44 eV electrons
            result[j][22] = array[34+(j // 60)*2640+(j % 60)*43] #Chanel 20, 30 eV electrons
            result[j][23] = array[41+(j // 60)*2640+(j % 60)*43] #Chanel 1, 30000 eV ions
            result[j][24] = array[40+(j // 60)*2640+(j % 60)*43] #Chanel 2, 20400 eV ions
            result[j][25] = array[39+(j // 60)*2640+(j % 60)*43] #Chanel 3, 13900 eV ions
            result[j][26] = array[38+(j // 60)*2640+(j % 60)*43] #Chanel 4, 9450 eV ions
            result[j][27] = array[45+(j // 60)*2640+(j % 60)*43] #Chanel 5, 6460 eV ions
            result[j][28] = array[44+(j // 60)*2640+(j % 60)*43] #Chanel 6, 4400 eV ions
            result[j][29] = array[43+(j // 60)*2640+(j % 60)*43] #Chanel 7, 3000 eV ions
            result[j][30] = array[42+(j // 60)*2640+(j % 60)*43] #Chanel 8, 2040 eV ions
            result[j][31] = array[49+(j // 60)*2640+(j % 60)*43] #Chanel 9, 1392 eV ions
            result[j][32] = array[48+(j // 60)*2640+(j % 60)*43] #Chanel 10, 949 eV ions
            result[j][33] = array[47+(j // 60)*2640+(j % 60)*43] #Chanel 11, 949 eV ions
            result[j][34] = array[46+(j // 60)*2640+(j % 60)*43] #Chanel 12, 646 eV ions
            result[j][35] = array[53+(j // 60)*2640+(j % 60)*43] #Chanel 13, 440 eV ions
            result[j][36] = array[52+(j // 60)*2640+(j % 60)*43] #Chanel 14, 300 eV ions
            result[j][37] = array[51+(j // 60)*2640+(j % 60)*43] #Chanel 15, 204 eV ions
            result[j][38] = array[50+(j // 60)*2640+(j % 60)*43] #Chanel 16, 139 eV ions
            result[j][39] = array[57+(j // 60)*2640+(j % 60)*43] #Chanel 17, 95 eV ions
            result[j][40] = array[56+(j // 60)*2640+(j % 60)*43] #Chanel 18, 65 eV ions
            result[j][41] = array[55+(j // 60)*2640+(j % 60)*43] #Chanel 19, 44 eV ions
            result[j][42] = array[54+(j // 60)*2640+(j % 60)*43] #Chanel 20, 30 eV ions
        del array
        #Тут все ок
        #TODO: возвращать Dataset
        return result
#def createDataSets(filename):
    
    

filename = 'f15/ssj/2005/03/j4f1505060'
filePathVars = filename.split('/')
flightNumber = filePathVars[-1][2:5]
flightYear = filePathVars[-1][5:7]
flightDay = filePathVars[-1][7:10]

#print(createTransformedDataVariablesSet(filename)[0,:].tolist()) #Тест получения преобразованных переменных для каждой минуты
## ---- все ок
#print(createRawDataVariablesSet(filename)[0, :].tolist()) #Тест получения сырых переменных для каждой минуты
## ---- все ок

#print(getMax(createRawDataMeasuresSet(filename)[0:1,:].tolist())) #Тест получения сырых данных для каждой секунды
#print(createRawDataMeasuresSet(filename)[0:3,:])
## ---- все ок
# for i in range(1,366):
#     print(getCountsFromData(np.max(createRawDataMeasuresSet(f'f15/ssj/2005/test/j4f1505{str.zfill(str(i),3)}')[:,3::])))
#     print(str.zfill(str(i),3))

#TODO: сделать метод, возвращающий датасет для преобразованных данных для каждой секунды |
#сделать проверку отправляемого в методы файлы на архив (если отправляется архив, то он распаковывается и дальше идет файл)
#думаю это надо для красоты сделать через обертку методов |
#подумать насчет предоставления методов для работы с данными сенсеров (преобразование к геофизическим данным) |
#сделать визуализацию через seaborn