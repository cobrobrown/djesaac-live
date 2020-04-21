'''
plot real time audio input
'''

import sounddevice as sd
import numpy as np

import tkinter as Tkinter
import time
import threading
import random
import queue as Queue

class GuiPart:
    def  __init__(self, master, queue, endCommand):
        self.queue = queue
        # Set up the GUI
        console = Tkinter.Button(master, text='Done', command=endCommand)
        console.pack(  )
        # frame
        
        #

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                print(msg)
            except Queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = Queue.Queue(  )

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming(  )
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        # set up audio stream
        N = 512
        stream = sd.InputStream(device=6,channels=1,samplerate=48484)
        stream.start()
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            time.sleep(rand.random(  ) * 1.5)
            msg = rand.random(  )
            
            
            
            
            y,_ = stream.read(N)
            msg = np.max(y)
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0

rand = random.Random(  )
root = Tkinter.Tk(  )

client = ThreadedClient(root)
root.mainloop(  )







'''
# radio options
plot_var = StringVar()
R1 = Radiobutton(root, text="Time", variable=plot_var, value="Time",
command=plot)


R2 = Radiobutton(root, text="Freq", variable=plot_var, value="Freq", command=plot)




# configure
low_bin_in = StringVar()
low_bin_out = StringVar()

low_bin_entry = ttk.Entry(mainframe,width=7,textvariable=low_bin_in)
low_bin_entry.grid(column=2,row=1,sticky=(W,E))

ttk.Label(mainframe,textvariable=low_bin_out).grid(column=2,row=2,sticky=(W,E))
ttk.Button(mainframe, text="Configure", command=configure).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="new low_bin").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="current").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="low_bin").grid(column=3, row=2, sticky=W)

# audio output
#amplitude = StringVar()
#ttk.Label(mainframe,textvariable=amplitude)


'''
