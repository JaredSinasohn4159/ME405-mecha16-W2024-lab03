"""!
@file main.py
This file contains the testing and running of the CLController class.
The file creates a motor object, an encoder object, and a CLController
object.  The program then runs P control, gets motor position and time
data, and plots the step response.

@author Jared Sinasohn, Sydney Ulvick, Sean Nakashimo
@date 22-Feb-2024
"""

import time
import tkinter
from random import random
import serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

def plot(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    This function is a way to embed a plot into a GUI.
    The data is read through the USB-serial port and processsed to make two lists which
    will contain both our time and voltage readings.
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas, also supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    """
    # Opening a serial port
    #https://friendlyuser.github.io/posts/tech/2023/Using_PySerial_in_Python_A_Comprehensive_Guide/
    ser=serial.Serial('COM3',115200, timeout=.001) #assign port name and read rate (bps), timeout is the delay
    ser.write(b'\x04') #soft reset, executes main again, can be accomplished by plugging in and out again
    #creating empty lists for our data
    time = [] 
    pos = []
    i = 0
    #iterating through each line, removing/ modifying bad data
    while True:
        line = ser.readline().decode('utf-8')  # reads a line of data and decodes it as
        line = line.split(",")
        if len(line)<2:
            continue
        line = [line[0], line[1]]
        line[0] = (line[0].strip()).replace(" ", "")
        line[1] = (line[1].strip()).replace(" ", "")
        try:
            print(line)
            time.append(float(line[0]))
            voltage.append(float(line[1]))
        except:
            continue
        if float(line[0]) == 1990:
            break

    
# Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(time, pos)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_axes.plot(time, tvoltage)
    #plot_axes.legend("Experimental", "Theoretical")
    plot_canvas.draw() #ensures updated plot 

def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot.
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
# Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)
# Create a Matplotlib
    fig = Figure()
    axes = fig.add_subplot()
# Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()
# Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
    text="Quit",
    command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
    text="Clear",
    command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
    text="Run Test",
    command=lambda: plot_function(axes, canvas, xlabel, ylabel))
    kp = 0
    ser=serial.Serial('COM3',115200, timeout=.001)
    kp_text = tkinter.Entry(tk_root,textvariable=kp)
    ser.write((f"{kp_text}\n").encode('utf-8'))
# Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)
    kp_text.grid(row=2, column=3)
# This function runs the program until the user decides to quit
    tkinter.mainloop()
# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program

if __name__ == "__main__":
    tk_matplot(plot,
    xlabel="Time (ms)",
    ylabel="Voltage (V)",
    title="Voltage vs Time")

