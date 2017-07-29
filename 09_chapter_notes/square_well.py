'''
implement matching function like eq9.11
implement eigenvalue solver using matching subroutine
have searcher print out each iterations result, stop with convergence at 4 digit
    have limit to iterations depth and include warning
plot resulting wave function + potential +eigenvalue
    decide whether or not it's a ground state based on node count
search out other eigenvalues
compare with analytic results from previous exercise
notes:
psi(x)''-(c V(x)+k**2)**psi(x)=0
c= 2m/hbar**2 = .0483/(MeV fm**2)

k**2 = c*abs(E)
observation: when E+V<0
'''

import numpy
from matplotlib import pyplot
import rk_comp

def numerov(start, steps, end, ksqr_func, poten_func):
    #wanted output, path with form of points [x, psi]
    #intended for use to be able to calculate psi' values at end, so one extra step must be taken
    #decide if going forward or back
    #
    delta = float(end-start)/steps
    path = [[start, 0], [start+delta, 10**-6]]
    for step in range(2, steps+2):
        kn1 = ksqr_func(path[-2][0], poten_func)
        k = ksqr_func(path[-1][0], poten_func)
        kp1 = ksqr_func(path[-1][0]+delta, poten_func)
        psi = path[-1][1]
        psin1 = path[-2][1]
        numer1 = 2.0*(1.0-5.*delta**2*k/12.)*psi
        numer2 = (1.0+delta**2*k/12.)*psin1
        denom = (1.+delta**2*kp1)/12.0
        psip1 = (numer1+numer2)/denom
        path.append([start+step*delta, psip1])
    return path

def time_reverser(t0, path):
    #path comprised of (t, x, v)
    # output = map(lambda point: [t0-point[0], point[1], point[2]], path)
    return map(lambda point: [t0-point[0], point[1], point[2]], path)

def backwards_test():
    w0 = numpy.pi*2
    forward_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -config[1]*(w0)**2)
    ]
    backward_funcs = [
        (lambda config: +1),
        (lambda config: -config[2]),
        (lambda config: +config[1]*(w0)**2)
    ]
    path1 = rk_comp.rk45(forward_funcs, [0, 1., 0], 5.0)
    path2 = rk_comp.rk45(backward_funcs, [0, path1[-1][1], path1[-1][2]], path1[-1][0])
    flipped_path2 = time_reverser(path1[-1][0], path2)
    ordered_path2 = sorted(flipped_path2, key=(lambda point:point[0]))
    print(len(path1), len(ordered_path2))
    print(path1[0], ordered_path2[0:3])
    #results: reversed path has 4 times as many points in it?! by nature of rk45, path2 does not actually include t=0, does get within 10**-13, though
    #decision: rk45 as implemented is messy for this purpose, numerov should be implemented
    # rk_comp.plot_paths([path1, flipped_path2], ['forward', 'back'])
    return

def plot_q_sys(waves, potential, k2_func=None):
    #waves are a set of wave functions with points [x, psi]
    min_x = 0
    max_x = 0
    axes = pyplot.subplot(111)
    for wave in waves:
        print(wave[0], wave[-1])
        if wave[0][0]<min_x:
            min_x=wave[0][0]
        if wave[-1][0]<min_x:
            min_x=wave[-1][0]
        if wave[-1][0]>max_x:
            max_x=wave[-1][0]
        if wave[0][0]>max_x:
            max_x=wave[0][0]
    print(min_x, max_x)
    x_vals = numpy.linspace(min_x, max_x, 200)
    PE_vals = map(potential, x_vals)
    axes.plot(x_vals, PE_vals)
    if k2_func:
        k_vals =[]
        for x in x_vals:
            k_vals.append(k2_func(x, potential))
        axes.plot(x_vals, k_vals)
    for wave in waves:
        # print(wave[:2])
        x_vals = []
        psi_vals = []
        for point in wave:
            x_vals.append(point[0])
            psi_vals.append(point[1])
        # print(x_vals[:2])
        # print(psi_vals[:2])
        axes.plot(x_vals, psi_vals)
    # axes.set_ylim((-2, 2))
    pyplot.show()
    return

def simple_square():
    v0 =-1
    scale = .0483 #/(MeV fm**2)
    E = -.5
    width = .5
    match = .5
    points =1000
    x_max = 10.0
    U_func = (lambda x: v0 if abs(x)<width else 0)
    k2_func = (lambda x, U_func: scale*(E-U_func(x)))
    left_side = numerov(-x_max, points, match, k2_func, U_func )
    right_side = numerov(x_max, points, match, k2_func, U_func )
    print(left_side[:3], left_side[0][0]-left_side[1][0], left_side[1][0]-left_side[2][0])
    print(right_side[:3], right_side[0][0]-right_side[1][0], right_side[1][0]-right_side[2][0])
    print(left_side[-3:])
    print(right_side[-3:])
    plot_q_sys([left_side, right_side], U_func, k2_func)
    return

if __name__ == '__main__':
    # backwards_test()
    simple_square()
