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
    #decision: rk45 as implemented is not appropriate for this purpose, numerov should be implemented
    # rk_comp.plot_paths([path1, flipped_path2], ['forward', 'back'])
    return

if __name__ == '__main__':
    backwards_test()
