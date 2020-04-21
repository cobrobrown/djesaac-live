'''
file		play.py
author		Conner Brown
description	run real time audio input through RGB processing and send to Arduino + LED strip
date created	08/15/2019
'''

import sounddevice as sd
from pyfirmata import Arduino
import matplotlib.pyplot as plt
import numpy as np
import math as m
import time
import collections
import queue
import librosa

print('Initializing...')

# setup
board = Arduino('/dev/ttyACM0')

pin3 = board.get_pin('d:3:p')
pin5 = board.get_pin('d:5:p')
pin6 = board.get_pin('d:6:p')
pin9 = board.get_pin('d:9:p')
pin10 = board.get_pin('d:10:p')
pin11 = board.get_pin('d:11:p')
led = board.get_pin('d:13:o')

fs = 48484
T = 1.0/fs
channels = 1
seconds = .02
N = int(fs*seconds)

print(sd.query_devices())

sd.default.device = 6
sd.default.samplerate = fs
sd.default.channels = channels

print('Ready!')

## processing config 
gain = .01
bin1 = 3#int(.02*len(Y))
bin2 = 5#int(.07*len(Y))
low_clip = .1
high_clip = 1
fade_len = 5

#mixing = [[0.5,0.5,0],[0.5,0,0.5],[0,0.5,0.5]]
mixing = [[1,0,0],[0,1,0],[0,0,1]]
mixed_values = {0:0,1:0,2:0}

qs = {x:collections.deque(np.zeros(5000)+1e-6) for x in range(3)}
thresh = np.ones(3)


## plotting config
run_bar = False
run_spec = True
#fig,(ax,ax_time) = plt.subplots(1,2)
if run_spec:
    ax_x = range(m.floor(N/2)-1)
    ax, = plt.plot(ax_x,np.random.rand(m.floor(N/2)-1)/100)
    ax_bin1 = plt.axvline(bin1)
    ax_bin2 = plt.axvline(bin2)
if run_bar:
    ax = plt.bar(range(3),[1,0,.5])
    for i in range(3):
        ax[i].set_color(mixing[i])
    plt.ion()
    plt.show()

# start stream
stream = sd.InputStream()
stream.start()

while stream.active:
    # stream input
    y,_=stream.read(N)
    y = y[:,0]
    if y.size==0:
        y = np.zeros(N)
    c = np.fft.fft(y, axis=0)/N
    Y = 2*(abs(c[1:int(m.floor(N/2))])**2)
    
    # scale Y with Equal-loudness contour
    #Y = [x*j for x,j in zip(Y,100.0/np.logspace(0,8,len(Y),base=2)[::-1])]
    # MFCC for more linear binning
    #mfcc = librosa.feature.mfcc(y=y,sr=fs,n_mfcc=20)
    #print(mfcc)
    
    
    # binning
    low = np.sum(Y[:bin1])
    med = np.sum(Y[bin1:bin2])
    high = np.sum(Y[bin2:])
    

    # update params
    values = {0:low,1:med,2:high}
    for i in range(3):
        # thresholding
        thresh[i] = gain*np.mean(sorted(qs[i])[-600:-10])
        
        #print('thresh',thresh[i])
        values[i] = values[i] / thresh[i]
        
        # clipping
        if values[i]  > high_clip:
            values[i]=1
        elif values[i] < low_clip:
            values[i]=0
        elif m.isnan(values[i]):
            values[i]=0
        
        # fading
        fade_thresh = max([qs[i][-j] for j in range(len(qs[i])-fade_len,len(qs[i]))])
        if values[i] < fade_thresh:
            values[i] = np.mean((fade_thresh,values[i]))
        
        # mixing
        for j in range(3):
            mixed_values[i] = values[j] * mixing[j][i]
        
        # either mixed_values or values below
        # shift q
        if mixed_values[i]:
            qs[i].pop()
            qs[i].appendleft(mixed_values[i])
    
    # autobinning: long term balancing of qs using bins
    # adjust bin index in proportion to the difference in power
    if (mixed_values[0] > np.mean(thresh)*3.0) and (bin1>2):
        # bump bin
        bin1-=1
    elif (mixed_values[0] < np.mean(thresh)*0.005) and (bin1<10):
        bin1+=1
    elif (mixed_values[1] > np.mean(thresh)*30.0) and (bin2>3):
        bin2-=1
    elif (mixed_values[1] < np.mean(thresh)*0.005) and (bin2<50):
        bin2+=1
    
        
    #print('bins',bin1,bin2)
    #print('values',values[0],values[1],values[2])
    # write out
    pin6.write(mixed_values[0])
    pin9.write(mixed_values[1])
    pin5.write(mixed_values[2])


    ### Plotting
    if run_spec:
        ax.set_ydata(Y)
        # bins
        ax_bin1.set_xdata([bin1]*2)
        ax_bin2.set_xdata([bin2]*2)
        plt.pause(seconds/10)
    if run_bar:
        for i,x in zip(range(len(ax)),[low,med,high]):
            ax[i].set_height(x)
        #plt.draw()
        plt.pause(seconds/10)

    ### Testing
    #for pin in [pin2,pin3,pin5,pin6,pin9,pin10,pin11]:
    #    pin.write(1)
    ##led.write(1)
    #time.sleep(1)
    #for pin in [pin2,pin3,pin5,pin6,pin9,pin10,pin11]:
    #    pin.write(0)
    ##led.write(0)
    #time.sleep(1)
