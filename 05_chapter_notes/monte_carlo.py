'''
5.14.1
use monte carlo to determine the area of the unit circle, A=pi
determine pairs of numbers between -1 and 1 to determine locations
tabulate which ones have displacement greater than 1, figure out at what point accuracy exceeds 3 digits
5.17.2 10D monte carlo
    based on eq 5.89 (sum(x_{1-10}))^2 |_0^1
    1) average the result of 16 trials
    2) take powers of 2 up to 2^13 as sample sizes
    3) plot relative error vs 1/n^.5 to look for linear behavior
    4) accuracy estimate?
    5) compare with quadrature methods for error
'''
import random
import numpy
from matplotlib import pyplot

def p514_1():
    power = 1
    def random_point():
        xi, yi = random.random(), random.random()
        return [xi*2-1, yi*2-1]
    while True:
        samples = 2**power
        hits = 0
        for run in range(samples):
            point = random_point()
            mag = point[0]**2+point[1]**2
            if mag < 1:
                hits+=1
        area = 4*(float(hits)/samples)
        error = abs(area-numpy.pi)/numpy.pi
        print('%d samples resulted in %.5f error' %(samples, error))
        if error < 10**-5:
            break
        power += 1
    return

def p517_1():
    exact = 156.0/6
    average_result = []
    average_error = []
    trials = 1
    max_power = 21
    powers = range(1,max_power)
    print(exact)
    for power in powers:
        tally = 0
        for loop in range(trials):
            for sample in range(2**power):
                x_vec = sum([random.random() for i in range(10)])
                tally += x_vec**2
        average_result.append(tally/(trials*2**power))
        average_error.append(abs(average_result[-1]-exact)/exact)
    print(average_error)
    inv_root_samples = [1.0/(trials*2**num)**0.5 for num in powers]
    pyplot.plot(powers, average_error)
    pyplot.plot(powers, inv_root_samples)
    pyplot.show()
    return
# p514_1()
p517_1()

