import finders
from matplotlib import pyplot
import numpy

'''
eq 7.20 = m-tanh(m/t)
treat t as a constant, find zeros
1: 6 digit bisection solution at 0.5
2: compare with NR
3: compare speed
4: make plot of m vs t
'''

def magnetization(t=0.5):
    return (lambda m: m-numpy.tanh(m/t))

def main():
    reduced_mag = magnetization()
    bisection_result = finders.bisection(reduced_mag, [0.2,5.0], threshold=10**-9)
    newt_result = finders.newton_raphson(reduced_mag, 3.0, threshold=10**-9)
    print(bisection_result, newt_result)


if __name__ == '__main__':
    main()
