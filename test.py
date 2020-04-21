import sounddevice as sd
import numpy as np
for i in np.arange(1000000,40000,-1):
    try:
        s = sd.rec(device=6,channels=1,frames=100,samplerate=i)
        print(i)
    except:
        pass
