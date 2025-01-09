import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from unzip import unzip


def getDateFromFileName(filename):
    def is_leap_year(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    flightDay = int(filename.split('/')[-1][-3:])
    flightYear = int(filename.split('/')[-1][5:7])
    month_days = [31, 28 + is_leap_year(flightYear), 31, 30, 31, 30, 
                  31, 31, 30, 31, 30, 31]  # Февраль учитывает високосный год
    month = 0
    while flightDay > month_days[month]:
        flightDay -= month_days[month]
        month += 1
    if flightYear > 25:
        flightYear = "19"+str.zfill(str(flightYear),2)
    else:
        flightYear = "20"+str.zfill(str(flightYear),2)
    return f"{str.zfill(str(flightDay),2)}.{str.zfill(str(month + 1),2)}.{flightYear}"

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
            result[j, 5] = float(int(array[5 + j*2640]) - 4995.0)/10.0 if array[5 + j*2640] > 1800 else float(int(array[5 + j*2640])-900)/10.0 #Geodetic latitude
            result[j, 6] = float(array[6 + j*2640])/10.0 #Geodetic longitude
            result[j, 7] = array[7 + j*2640] #Altitude, nautical miles
            result[j, 8] = float(int(array[8 + j*2640]) - 4995)/10.0 if array[8 + j*2640] > 1800 else float(int(array[8 + j*2640])-900)/10.0 #Geographic latitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft
            result[j, 9] = float(array[9 + j*2640]/10.0) #Geographic longitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft
            result[j, 10] = float(int(array[10 + j*2640]) - 4995)/10.0 if array[10 + j*2640] > 1800 else float(int(array[10 + j*2640])-900)/10.0 #Corrected geomagnetic latitude at 110km
            result[j, 11] = float(array[11 + j*2640]/10.0) #Corrected geomagnetic longitude at 100km
            result[j, 12] = array[12 + j*2640] #Hour of magnetic local time
            result[j, 13] = array[13 + j*2640] #Minute of hour of magnetic local time
            result[j, 14] = array[14 + j*2640] #Second of minute of magnetic local time
        del array
        flightDate = getDateFromFileName(path)
        expectedTime = np.arange(result.shape[0])
        location = ["lat", "lon"]
        dateType = ["year","day","hour","minute","second","time"]
        magneticTimeType = ["hour","minute","second","time"]
        ds = xr.Dataset(
            data_vars=dict(
                real_datetime =                                  (["date_type","expected_time"],
                                                                  np.stack((
                                                                      result[:, 4],
                                                                      result[:, 0],
                                                                      result[:, 1],
                                                                      result[:, 2],
                                                                      result[:, 3],
                                                                      result[:, 1]*60+result[:, 2]+result[:, 3]/60
                                                                      ),axis=0)),
                real_geodic_location =                           (["location","expected_time"], 
                                                                  np.stack((result[:, 5], result[:, 6]), axis=0)),
                real_altitude =                                  (["expected_time"], result[:, 7]),
                real_geographic_location =                       (["location","expected_time"],
                                                                  np.stack((result[:, 8], result[:, 9]), axis=0)),
                real_corrected_geomagnetic_location =            (["location","expected_time"],
                                                                  np.stack((result[:, 10], result[:, 11]), axis=0)),
                real_magnetic_local_time =                       (["magnetic_time_type","expected_time"], 
                                                                  np.stack((
                                                                      result[:, 12],
                                                                      result[:, 13],
                                                                      result[:, 14],
                                                                      result[:, 12]*60+result[:, 13]+result[:, 14]/60
                                                                      ),axis=0)),
            ),
            coords=dict(
                date_type=dateType,
                expected_time=expectedTime,
                location=location,
                magnetic_time_type=magneticTimeType,
            ),
            attrs=dict(description=f"SSJ4 raw data variables on day {flightDate}")
        )
        return ds
    
    
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
            result[j][12] = array[12 + j*2640] #Hour of f f magnetic local time
            result[j][13] = array[13 + j*2640] #Minute of hour of magnetic local time
            result[j][14] = array[14 + j*2640] #Second of minute of magnetic local time
        del array
        flightDate = getDateFromFileName(path)
        expectedTime = np.arange(result.shape[0])
        ds = xr.Dataset(
            data_vars=dict(
                raw_day_of_year =                               (["expected_time"], result[:, 0]),
                raw_hour_of_day =                               (["expected_time"], result[:, 1]),
                raw_minute_of_hour =                            (["expected_time"], result[:, 2]),
                raw_second_of_minute =                          (["expected_time"], result[:, 3]),
                raw_integer_year =                              (["expected_time"], result[:, 4]),
                raw_geodic_latitude =                           (["expected_time"], result[:, 5]),
                raw_geodic_longitude =                          (["expected_time"], result[:, 6]),
                raw_altitude =                                  (["expected_time"], result[:, 7]),
                raw_geographic_latitude =                       (["expected_time"], result[:, 8]),
                raw_geographic_longitude =                      (["expected_time"], result[:, 9]),
                raw_corrected_geomagnetic_latitude =            (["expected_time"], result[:, 10]),
                raw_corrected_geomagnetic_longitude =           (["expected_time"], result[:, 11]),
                raw_hour_of_magnetic_local_time =               (["expected_time"], result[:, 12]),
                raw_minute_of_hour_of_magnetic_local_time =     (["expected_time"], result[:, 13]),
                raw_second_of_minute_of_magnetic_local_time =   (["expected_time"], result[:, 14]),
            ),
            coords=dict(
                expected_time=expectedTime,
            ),
            attrs=dict(description=f"SSJ4 raw data variables on day {flightDate}")
        )
        return ds
    
    
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
        for (j) in range(minutesOfData*60):
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
        del array
        flightDate = getDateFromFileName(path)
        expectedTime = np.arange(0,result.shape[0])
        channels_types=["electrons","ions"]
        channels=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        ds = xr.Dataset(
            data_vars=dict(
                real_hours=         (["expected_time"], result[:, 0]),
                real_minutes=       (["expected_time"], result[:, 1]),
                real_seconds=   (["expected_time"], result[:, 2]/1000),
                real_time = (["expected_time"], result[:,0]*3600+result[:,1]*60+result[:,2]/1000),
                measures =  (["channels","expected_time","channel_type"],
                             np.stack(([result[:,i+3:i+24:20] for i in range(20)]),axis=0)),
            ),
            coords=dict(
                expected_time=expectedTime,
                channel_type=channels_types,
                channels=channels
            ),
            attrs=dict(description=f"SSJ4 transformed measures for every second on day {flightDate}")
        )
        return ds
    

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
            result[j][0] =  array[15+(j // 60)*2640+(j % 60)*43] #Hour of day for {i+1} second of data
            result[j][1] =  array[16+(j // 60)*2640+(j % 60)*43] #Minute of hour for {i+1} second of data
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
        
        flightDate = getDateFromFileName(path)
        expectedTime = np.arange(result.shape[0])
        channels_types=["electrons","ions"]
        channels=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],dtype=np.int8)
        ds = xr.Dataset(
            data_vars=dict(
                raw_real_hours=         (["expected_time"], result[:, 0]),
                raw_real_minutes=       (["expected_time"], result[:, 1]),
                raw_real_seconds=   (["expected_time"], result[:, 2]),
                raw_measures =  (["channels","expected_time","channel_type"],
                             np.stack(([result[:,i+3:i+24:20] for i in range(20)]),axis=0)),
            ),
            coords=dict(
                expected_time=expectedTime,
                channel_type=channels_types,
                channels=channels
            ),
            attrs=dict(description=f"SSJ4 raw measures for every second on day {flightDate}")
        )
        return ds
    
def transformToGeophysicalQuantity(data, valueType, flightNumber, channelType, channel):
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
        if channelType == 1:
            return (counts) / (IonsChannelsGeometricFactors[flightNumber][channel+1] * 0.098)
        elif channelType == 0:
            return (counts) / (ElectronsChannelsGeometricFactors[flightNumber][channel+1] * 0.098)
    def calculateDifferentialEnergyFluxForChannel(channel, counts):
        return (calculateDifferentialNumberFluxForChannel(channel, counts) * ChannelCentralEnergy[channel+1])
    def calculateIntegratedNumberFlux(channels):
        return sum([calculateDifferentialNumberFluxForChannel(i,counts[i-1]) * ChannelSpasing[i+1] for i in channels])
    def calculateIntegratedEnergyFlux(channels):
        return sum([calculateDifferentialEnergyFluxForChannel(i,counts[i-1]) * ChannelSpasing[i+1] for i in channels])
    def calculateMeanEnergy(channels):
        return calculateIntegratedEnergyFlux(channels) / calculateIntegratedNumberFlux(channels)
    
    counts = data.measures.isel(channels=channel,channel_type=channelType).values
    #if type(channel)
    print(counts)
    
    if valueType == "differential number flux" or valueType == 0:
        return calculateDifferentialNumberFluxForChannel(channel, counts)
    elif valueType == "differential energy flux" or valueType == 1:
        return calculateDifferentialEnergyFluxForChannel(channel, counts)
    elif valueType == "integrated number flux" or valueType == 2:
        return calculateIntegratedNumberFlux(channels=channel[::])
    elif valueType == "integrated energy flux" or valueType == 3:
        return calculateIntegratedEnergyFlux(channels=channel[::])
    elif valueType == "mean energy" or valueType == 4:
        return calculateMeanEnergy(channels=channel[::])

filename = 'f15/ssj/2005/03/j4f1505060'

data = createTransformedDataMeasuresSet(filename)
print(transformToGeophysicalQuantity(data,4,filename.split('/')[-1][2:5],0,range(20)))
#Получение средней энергии по всем каналам сенсора для электронов для каждой секунды


#datavars = createTransformedDataVariablesSet(filename)
#print(data.measures.isel(channels=0,channel_type=0).values)
#Plotting examples
plt.style.use("seaborn-v0_8-whitegrid")

# datavars.real_datetime.isel(date_type=[0,1,2,3]).plot.line("-o",x="expected_time")
# plt.show()

# datavars.real_geographic_location.isel(location=0).plot.line("-o",x="expected_time")
# plt.show()

# data.measures.isel(channels=0, channel_type=[0,1], expected_time=range(120)).plot.line("-o", x="expected_time")
# plt.show()

#data.measures.isel(channels=[0,4,9], channel_type=0).plot.line("-o", x="expected_time")
# plt.yscale("log", base=10)
#plt.show()

# data.real_Hours.isel().plot.line("-o")
# data.real_Minutes.isel().plot.line("-o")
# plt.show()

# data.real_Time.isel().plot.line("-o")
# plt.xlim(0,100)
# plt.ylim(0,100)
# plt.show()