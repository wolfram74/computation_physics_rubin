'''
initial conditions, vary impact parameter and v_y
some possible parameters for scanning are given
plot a few cartesian (x,y) trajectories of interesting nature
plot a few configuration-space trajectories (x,vx), (v,vy)
    note scattering and non-scattering paths
experiment with attractive potentials as well as repulsive
time delay measurements?
notes:
to determine cross section as a function of deflection:
    I need to be able to do deflection as a function impact parameter
    define a function that generates deflection based on possible parameters
    then curry everything but impact parameter
potential:
    C^2*x^2*y^2*e^-(x^2+y^2) has peak of .13*C^2
    limiting a mass 1 particle to KE=v^2/2<.13*C^2
        v<(.23)^1/2*C ~ .52*C
    potential decays by a factor of 10**10 by distance of 5
    starting at []

'''

import numpy
from matplotlib import pyplot
import rk_comp
import time

def column(matrix, col_index):
    return [row[col_index] for row in matrix]

def deflection(scattering_func, y0=.5, v0=.5):
    path = rk_comp.rk45(scattering_func, [0, -5.5, y0, v0, 0], 15.0)
    theta = numpy.arctan2(path[-1][4], path[-1][3])
    return theta


def pather_drawing():
    target = [
        (lambda state: 1),
        (lambda state: state[3]),
        (lambda state: state[4]),
        (lambda state: -2*state[1]*state[2]**2*(1-state[1]**2)*numpy.exp(-(state[1]**2+state[2]**2))),
        (lambda state: -2*state[1]**2*state[2]*(1-state[2]**2)*numpy.exp(-(state[1]**2+state[2]**2)))
    ]
    runs = 4
    # b_vals = numpy.linspace(.9, .25, runs)
    b_vals = numpy.linspace(.9, .25, runs-1)
    b_vals = numpy.append(b_vals, 2.3)
    fig, axes = pyplot.subplots(runs,3)
    for b_index in range(len(b_vals)):
        b = b_vals[b_index]
        path = rk_comp.rk45(target, [0, -5.5,b , .5, 0], 25.0)
        x_vals = column(path, 1)
        y_vals = column(path, 2)
        vx_vals = column(path, 3)
        vy_vals = column(path, 4)
        axes[b_index][0].scatter([1, 1, -1, -1], [1, -1, 1, -1], facecolor='r')
        axes[b_index][0].scatter(x_vals, y_vals)
        axes[b_index][1].scatter(x_vals, vx_vals)
        axes[b_index][2].scatter(y_vals, vy_vals)
    # axes.set_ylim([-2.5, 2.5])
    # axes.set_xlim([-2.5, 2.5])
    pyplot.savefig("%d.png" % int(time.time()))
    # pyplot.show()


if __name__ == '__main__':
    pather_drawing()
