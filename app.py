'''
file		app.py
author		Conner Brown
description	DJEsaac manager, live config, displays
date created	09/16/2019
'''
from tkinter import *
from tkinter import ttk


# define button actions
def reconfigure(*args):
    try:
        value = float(low_bin_in.get())
        low_bin_out.set(str(value))
    except ValueError:
        low_bin_out.set("Error")

def assign_color(*args):
    try:
        for color_val,pin in zip(color_vals,pins):
            pin.write(float(color_val))
    except ValueError:
        pass

# select real time plot: time, freq, RGB

# continuous plot
def plot(*args):
    if plot_var.get()=="Time"
        canvas.creat_line()
    elif plot_var.get()=="Freq":
        canvas.creat_line()
    elif plot_var.get()=="RGB":
        canvas.creat_line()

# init
root = Tk()
root.title("DJEsaac Manager")

# build frames
config_frame = ttk.Frame(root,padding="3 3 12 12")
config_frame.grid(column=0,row=0,sticky=(N,W,E,S))
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

### build widgets: buttons, labels, entry fields
# multiselect plot

plot_var = StringVar()
R1 = Radiobutton(root, text="Time", variable=plot_var, value="Time",
command=plot)
R1.pack( anchor = W )

R2 = Radiobutton(root, text="Freq", variable=plot_var, value="Freq", command=plot)
R2.pack( anchor = W )

R3 = Radiobutton(root, text="RGB", variable=plot_var, value="RGB", command=plot)
R3.pack( anchor = W)

canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.bind("<Button-1>", plot)

# entry and display
low_bin_in = StringVar()
low_bin_out = StringVar()

in_entry = ttk.Entry(config_frame, width=7, textvariable=low_bin_in)
in_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(config_frame, textvariable=low_bin_out).grid(column=2, row=2, sticky=(W, E))
ttk.Button(config_frame, text="Reconfigure", command=reconfigure).grid(column=3, row=3, sticky=W)

ttk.Label(config_frame, text="low_bin_in").grid(column=3, row=1, sticky=W)
ttk.Label(config_frame, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(config_frame, text="Out").grid(column=3, row=2, sticky=W)

for child in config_frame.winfo_children(): child.grid_configure(padx=5, pady=5)


#  run
root.mainloop()
