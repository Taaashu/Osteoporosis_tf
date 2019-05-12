# Simple demo of of the ADXL345 accelerometer library.  Will print the X, Y, Z
# axis acceleration values every half second.
# Author: TF
# License: Public Domain
import time
import numpy as np
# Import the ADXL345 module.
import Adafruit_ADXL345
import easygui as eg
from scipy import pi
from scipy.fftpack import fft

# Create an ADXL345 instance.
accel = Adafruit_ADXL345.ADXL345()

# Alternatively you can specify the device address and I2C bus with parameters:
#accel = Adafruit_ADXL345.ADXL345(address=0x54, busnum=2)
# You can optionally change the range to one of:
#  - ADXL345_RANGE_2_G   = +/-2G (default)
#  - ADXL345_RANGE_4_G   = +/-4G
#  - ADXL345_RANGE_8_G   = +/-8G
#  - ADXL345_RANGE_16_G  = +/-16G
# For example to set to +/- 16G:
#accel.set_range(Adafruit_ADXL345.ADXL345_RANGE_4_G)

# Or change the data rate to one of:
#  - ADXL345_DATARATE_0_10_HZ = 0.1 hz
#  - ADXL345_DATARATE_0_20_HZ = 0.2 hz
#  - ADXL345_DATARATE_0_39_HZ = 0.39 hz
#  - ADXL345_DATARATE_0_78_HZ = 0.78 hz
#  - ADXL345_DATARATE_1_56_HZ = 1.56 hz
#  - ADXL345_DATARATE_3_13_HZ = 3.13 hz
#  - ADXL345_DATARATE_6_25HZ  = 6.25 hz
#  - ADXL345_DATARATE_12_5_HZ = 12.5 hz
#  - ADXL345_DATARATE_25_HZ   = 25 hz
#  - ADXL345_DATARATE_50_HZ   = 50 hz
#  - ADXL345_DATARATE_100_HZ  = 100 hz (default)
#  - ADXL345_DATARATE_200_HZ  = 200 hz
#  - ADXL345_DATARATE_400_HZ  = 400 hz
#  - ADXL345_DATARATE_800_HZ  = 800 hz
#  - ADXL345_DATARATE_1600_HZ = 1600 hz
#  - ADXL345_DATARATE_3200_HZ = 3200 hz
# For example to set to 6.25 hz:
accel.set_data_rate(Adafruit_ADXL345.ADXL345_DATARATE_800_HZ)

xData = []
recFreq = 0
avgFreq = 0
#print('Printing X, Y, Z axis values, press Ctrl-C to quit...')
while True:
    # Read the X, Y, Z axis acceleration values and print them.
    #x, y, z = accel.read()
    start = time.time()
    for a in range (0,10):
        for i in range (0,100):
            x,_,_ = accel.read()
            xData.append(x)
            #print('X={0}, Y={1}, Z={2}'.format(x, y, z))
            # Wait half a second and repeat.
        end = time.time()
        print("Time taken :",end-start)
        #time.sleep(1)
        
        N = len(xData)
        # Nyquist Sampling Criteria
        
        T = 1/800 # inverse of the sampling rate
        x = np.linspace(0.0, 1.0/(2.0*T), int(N/2))

        # FFT algorithm
        yr = fft(xData) # "raw" FFT with both + and - frequencies
        y = 2/N * np.abs(yr[0:np.int(N/2)]) # positive freqs only

        xData=[]
        yNoPeakArray = y[1:]
        gHigh = np.max(yNoPeakArray)
        #print(gHigh)
        gHighPos = np.where(y == gHigh)
        #print(gHighPos)
        freqData = x[gHighPos] 
        recFreq = recFreq+freqData
        print("recFreq = ",recFreq)
        print("Highest Vibration Peak :",gHigh)
        time.sleep(1)

    avgFreq = recFreq/10
    print("\n")
    print("***********************")
    if avgFreq>0 and avgFreq<76.8:
        print("Osteoporosis")
        eg.msgbox("Osteporosis:"+str(avgFreq)+"Hz","ODR[Osteoporosis Detection Report]")
    elif avgFreq>76.8 and avgFreq<96.8:
        print("Osteopenia")
        eg.msgbox("Osteopenia:"+str(avgFreq)+"Hz","ODR[Osteoporosis Detection Report]")
    else:
        print("Normal")
        eg.msgbox("Normal:"+str(avgFreq)+"Hz","ODR[Osteoporosis Detection Report]")
    print("***********************")
    print("\n")
    time.sleep(60)
