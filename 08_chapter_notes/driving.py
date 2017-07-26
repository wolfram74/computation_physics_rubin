'''
implement driving in evolution
demonstrate mode locking with large driving force
demonstrate beating with driving force comparable to average restoring force
show beating is average of w0 and wd in SHO
plot max amplitude as a function of wd
explore beating in non-SHO systems, observe beating as alternative to resonance
include friction, observe peak broadening
make some observations bout driving effectiveness in higher order wells.
'''

import numpy
import time
from matplotlib import pyplot
import rk_comp

def mode_lock():
    w0 = numpy.pi*2
    f0 = w0*500
    wd = .5
    sho_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -config[1]*(w0)**2)
    ]
    drive_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -config[1]*(w0)**2+f0*numpy.sin(wd*config[0]))
    ]
    x0 = 1.0
    tfin = 50.0
    start = time.time()
    path0 = rk_comp.rk45(sho_funcs, [0, float(x0), 0], tfin, precision=10**-6)
    path1 = rk_comp.rk45(drive_funcs, [0, float(x0), 0], tfin, precision=10**-6)
    end = time.time()
    print(end-start)
    rk_comp.plot_paths([path0, path1])

def beating():
    w0 = numpy.pi*2
    f0 = w0**2
    wd = numpy.pi*2.5
    sho_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -config[1]*(w0)**2)
    ]
    drive_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -config[1]*(w0)**2+f0*numpy.sin(wd*config[0]))
    ]
    x0 = 1.0
    tfin = 50.0
    start = time.time()
    path0 = rk_comp.rk45(sho_funcs, [0, float(x0), 0], tfin, precision=10**-6)
    path1 = rk_comp.rk45(drive_funcs, [0, float(x0), 0], tfin, precision=10**-6)
    end = time.time()
    print(end-start)
    rk_comp.plot_paths([path0, path1])

def non_harmonic_beating():
    w0 = numpy.pi*2
    f0 = w0**2
    wd = numpy.pi*1.2
    drive_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -config[1]**5+3*numpy.sin(wd*config[0])-0.1*config[2])
    ]
    x0 = 1.5
    tfin = 150.0
    start = time.time()
    path1 = rk_comp.rk45(drive_funcs, [0, float(x0), 0], tfin, precision=10**-6)
    end = time.time()
    print(end-start)
    rk_comp.plot_paths([ path1])


def main():
    # mode_lock()
    # beating()
    non_harmonic_beating()

if __name__ == '__main__':
    main()
