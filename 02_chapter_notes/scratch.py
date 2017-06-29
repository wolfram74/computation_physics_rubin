import math
from matplotlib import pyplot
import numpy

def p243():
    low = 1.0
    high = 1.0
    for i in range(1100):
        low /= 2
        high *= 2
        print('loop: %d \n low:%f \n high: %f\n\n' % (i, low, high))
    pass

def p25(x, verbose=False):
    prev_term = 1*x
    total = prev_term
    error = 10**-8
    count = 1
    template = 'term %d, total %f, contribution %f, difference %f'
    while abs(prev_term/total) > error:
        count+=1
        denom = (2*count-1)*(2*count-2)
        term = (-x**2)*prev_term/denom
        total += term
        prev_term = term
        if(verbose):
            print( template % (count, total, term, math.sin(x)-total))
    return template % (count, total, term, math.sin(x)-total)

def fourier_coefficient(k_val, x_vals):
    del_x = x_vals[1]
    indices = numpy.arange(0, len(x_vals))
    #result of integrating over narrow band discussed in section 2
    basis = (
        numpy.cos(k_val*numpy.pi*indices*del_x)
        -numpy.cos(k_val*numpy.pi*(indices+1)*del_x)
        )/(k_val*numpy.pi)
    basis2 = numpy.sin(k_val*numpy.pi*x_vals)
    pyplot.plot(x_vals, basis)
    pyplot.plot(x_vals, basis2)
    pyplot.show()
    return
    # return 2*numpy.dot(basis, y_vals)


p243()
# input_val = 49.4 # converges on wrong value
# input_val = 149.4
for x_val in range(1, 50):
    argument = float(x_val)
    print('sin evaluated at %f and %f mod 2pi' % (argument, argument%(math.pi*2)))
    print(p25(argument) )
    print( p25(argument%(math.pi*2)))
    print('')
# fourier_coefficient(5, numpy.linspace(0.0, 1.0, 1001))
