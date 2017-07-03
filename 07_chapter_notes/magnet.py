import finders
from matplotlib import pyplot
import numpy
import time

'''
eq 7.20 = m-tanh(m/t)
treat t as a constant, find zeros
1: 6 digit bisection solution at 0.5
2: compare with NR
3: compare speed
4: make plot of m vs t
'''

def magnetization(t=0.5):
    return (lambda m: numpy.tanh(m/t)-m)

def magnetization_plot():
    delta_t = 0.025
    t = 0.0
    t_vals = []
    m_vals = []
    while True:
        t += delta_t
        reduced_mag = magnetization(t)
        if reduced_mag(.01)<0:
            break
        t_vals.append(t)
        m_vals.append(finders.newton_raphson(reduced_mag, 3.0, threshold=10**-6))
    pyplot.plot(t_vals, m_vals)
    pyplot.ylim((0,1.5))
    pyplot.show()



def main():
    reduced_mag = magnetization()
    bisection_result = finders.bisection(reduced_mag, [0.2,5.0], threshold=10**-9)
    newt_result = finders.newton_raphson(reduced_mag, 3.0, threshold=10**-9)
    print(bisection_result, newt_result, (bisection_result-newt_result)/newt_result)
    loops = 10**3
    bisect_start = time.time()
    for loop in range(loops):
        bisection_result = finders.bisection(reduced_mag, [0.2,5.0], threshold=10**-9)
    bisect_end = time.time()
    average_bisect = (bisect_end-bisect_start)/loops
    newt_start = time.time()
    for loop in range(loops):
        newt_result = finders.newton_raphson(reduced_mag, 3.0, threshold=10**-9)
    newt_end = time.time()
    average_newt = (newt_end-newt_start)/loops
    print('bisection took on average %.5f per calc' % average_bisect )
    print('newton raphson took on average %.5f per calc' % average_newt)
    print('in this case newton was %2.3f times faster' % (average_bisect/average_newt))
    magnetization_plot()


if __name__ == '__main__':
    main()
