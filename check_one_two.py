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

fs = 44100
T = 1.0/fs
channels = 2
seconds = .02
N = int(fs*seconds)

sd.default.device = 4
sd.default.samplerate = fs
sd.default.channels = channels

stream = sd.InputStream()
stream.start()

de = collections.deque([0])
thresh_samples=[0]*10
thresh = 20
x=0

print('Ready!')


while True:
    ### color wheel
    for i in range(10):
        for led in [pin9,pin5,pin6]:
            # scale up
            for i in range(100):
                led.write(i/100)
                time.sleep(.01)
            # scale down
            for i in range(100):
                led.write((100-i)/100)
                time.sleep(.01)
    
    ### heartbeat
    
    
    
    
    
    
    
