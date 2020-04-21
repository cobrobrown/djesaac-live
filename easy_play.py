'''
file		easy_play.py
author		Conner Brown
description	simple light show with manual config
date created	09/12/2019
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

# audio params
fs = 48484 # sampling frequency, choose max per mic
T = 1.0/fs
channels = 1
seconds = .02
N = int(fs*seconds)

print(sd.query_devices())

# use info printed to set params
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
fade_gain = .5
#mixing = [[0.5,0.5,0],[0.5,0,0.5],[0,0.5,0.5]]
mixing = [[1,0,0],[0,1,0],[0,0,1]]
mixed_values = {0:0,1:0,2:0}

qs = {x:collections.deque(np.zeros(10000)+1e-6) for x in range(3)}

thresh = [.1,.07,.06]#np.ones(3)

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
    
    # binning
    low = np.sum(Y[:bin1])
    med = np.sum(Y[bin1:bin2])
    high = np.sum(Y[bin2:])
    
    # update params
    values = {0:low,1:med,2:high}
    for i in range(3):
        print(i)
        print('pre {:0.6f}'.format(values[i]))
        # thresholding
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
            values[i] += fade_gain*(fade_thresh-values[i])/2.0

        print('post {:0.6f}'.format(values[i]))
            
        # shift q
        if values[i]:
            qs[i].pop()
            qs[i].appendleft(values[i])
            
    # write out
    pin6.write(values[0])
    pin9.write(values[1])
    pin5.write(values[2])

    ### Testing
    '''
    for pin in [pin5,pin6,pin9]:
        pin.write(1)
        time.sleep(3)
        pin.write(0)
        time.sleep(1)
        ''';
