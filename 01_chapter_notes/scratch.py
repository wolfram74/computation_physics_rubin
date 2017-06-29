import numpy
from PIL import Image, ImageDraw
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

"""
=====
Decay
=====

This example showcases a sinusoidal decay animation.
"""

def data_gen(t=0):
    cnt = 0
    while cnt < 100:
        cnt += 1
        t += 0.1
        yield t, numpy.sin(2*numpy.pi*t) * numpy.exp(-t/10.)


def init():
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(0, 5)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

fig, ax = pyplot.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []


def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

# ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
#                               repeat=False, init_func=init)

def source_data(t=0):
    count = 0
    frequencies = numpy.linspace(1, 4, 100)
    while count < 100:
        count += 1
        t = 2.0*numpy.pi*(count/100.0)
        yield t, numpy.cos(t*frequencies), frequencies

def frame_gen(data):
    t, amplitudes, frequencies = data
    line.set_data(frequencies, amplitudes)
    # print(amplitudes[0:5])
    return line

movie = animation.FuncAnimation(fig, frame_gen, source_data,
    repeat=False, interval=10, init_func=init)
movie.save('saveTest.mp4')
# movie.to_html5_video() # needs python 3
# pyplot.show() #plots in terminal
