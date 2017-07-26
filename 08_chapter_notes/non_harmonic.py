'''
given potentials of the form a/p*x**p, p=(2:12)
Xverify numerical solutions produce max velocities at origin and 0 velocity at max displacement
Xdevise algorithm for calculating period
explore shapes and periods for different powers and strength of asymmetry
X~make some graphs of period as a function of amplitude: decided to do energy instead
X in a metastable well, find the energy that approaches the seperatrix
stretch:
calculate KE and PE, plot E over 50 periods
plot relative error based on initial energy, aim for 11 digits of accuracy
numerically verify virial theorem
'''

import numpy
import time
from matplotlib import pyplot
import rk_comp

def period_finder(path):
    '''
    takes a path with points formatted as (time, pos, velocity)
    determines times the follow a zero crossing with positive velocity
    method chosen over considering all zero crossings to accommodate asymmetric oscillators
    '''
    crossing_times = []
    for index in range(1,len(path)):
        if path[index][1]*path[index-1][1]<0 and path[index][2]>0:
            crossing_times.append(path[index][0])
    if len(crossing_times)<=0:
        return None
    period = 0
    for index in range(1, len(crossing_times)):
        period+=(crossing_times[index]-crossing_times[index-1])
    return period/(len(crossing_times)-1)

def max_displace(path, count=1):
    '''
    will find count number of points that are furthest from the origin assuming points in path are (t, x, v)
    '''
    extrema = sorted(path[0:count], key=lambda point: abs(point[1]))
    for point_index in range(count, len(path)):
        point = path[point_index]
        if abs(point[1]) > abs(extrema[0][1]):
            extrema.append(point)
        if len(extrema) > count:
            extrema = sorted(extrema, key=lambda point: abs(point[1]))
            extrema.pop(0)
    return extrema

def min_veloc(path, count=1):
    '''
    will find count number of points that are slowest moving assuming points in path are (t, x, v)
    '''
    extrema = sorted(path[0:count], key=lambda point: abs(point[2]))
    for point_index in range(count, len(path)):
        point = path[point_index]
        if abs(point[2]) < abs(extrema[-1][2]):
            extrema.append(point)
        if len(extrema) > count:
            extrema = sorted(extrema, key=lambda point: abs(point[2]))
            extrema.pop()
    return extrema

def compare_extremas(max_dist, min_vel):
    print(sorted(max_dist, key=lambda point: point[0]))
    print(sorted(min_vel, key=lambda point: point[0]))
    return

def sho_tester():
    w0 = numpy.pi*2
    sho_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -config[1]*(w0)**2)
    ]
    calculated_periods = []
    for x0 in range(1,3):
        path = rk_comp.rk45(sho_funcs, [0, float(x0), 0], 20.0, precision=10**-5)
        print(len(path))
        calculated_periods.append(period_finder(path))
        compare_extremas(max_displace(path, count=3), min_veloc(path, count=3))
    print(calculated_periods)
    return

def period_vs_totalE():
    '''
    amplitudes selected to compare total energy to total energy
    '''
    energies = 1.25**numpy.arange(-5, 7)
    sets_of_periods = []
    for power in range(5):
        p = 2*power + 1
        periods = []
        well_funcs = [
            (lambda config: 1),
            (lambda config: config[2]),
            (lambda config: -p*config[1]**p)
        ]
        for energy in energies:
            x0 = energy**(1.0/p)
            path = rk_comp.rk45(well_funcs, [0, x0, 0], 20.0, precision=10**-5)
            periods.append(period_finder(path))
        pyplot.plot(energies, periods)
    pyplot.show()
    return

def metastable_seperatrix():
    a, b = 4.0, 3.0
    well_func = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -a*config[1]-b*config[1]**2.0)
    ]
    print(-a/b)
    seperatrix = -a/b
    # seperatrix = -a/(2.*b)
    starts = numpy.linspace(seperatrix*.01, seperatrix, 20)-seperatrix*.000001
    periods = []
    for x0 in starts:
        print(x0)
        path = rk_comp.rk45(well_func, [0,x0, 0], 20.0, precision=10**-5)
        periods.append(period_finder(path))
    pyplot.plot(starts, periods)
    pyplot.show()
    return

def energy_conservation_tester():
    w0 = numpy.pi*2
    sho_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -config[1]*(w0)**2)
    ]
    x0 = 1.0
    tfin = 50.0
    start = time.time()
    path = rk_comp.rk45(sho_funcs, [0, float(x0), 0], tfin, precision=10**-10)
    end = time.time()
    print(len(path), tfin/len(path))
    print('took %.3f seconds' % (end-start))
    times = map(lambda point: point[0], path)
    potential = map(lambda point: (w0**2/2.)*point[1]**2, path)
    kinetic = map(lambda point: point[2]**2/2, path)
    total = numpy.array(potential)+numpy.array(kinetic)
    # pyplot.plot(times, potential)
    # pyplot.plot(times, kinetic)
    # pyplot.plot(times, total)
    error = abs(total-total[0])/total[0]
    pyplot.plot(times, numpy.log10(error))
    #-5 got about 4.8 digits, -6 got 5.9, -7 got 6.5, -8 got 7.7
    #-9 got 8.3 digits -10 get 9.6 digit after 6 minutes
    pyplot.show()
    return

def main():
    # sho_tester()
    # period_vs_totalE()
    metastable_seperatrix()
    # energy_conservation_tester()
    return

if __name__ == '__main__':
    main()
