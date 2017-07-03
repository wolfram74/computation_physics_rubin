import numpy
from matplotlib import pyplot
'''
page 142
'''

def bisection(func, bounds=[0.0,1.0], threshold=(10**-4), delta = 10.0):
    if func(bounds[0])*func(bounds[1]) > 0:
        return False
    mid = (bounds[0]+bounds[1])/2
    new_delta = abs(func(bounds[0]) - func(bounds[1]))
    if delta < new_delta:
        return float('NaN')
    if func(mid)<threshold:
        return mid
    if func(mid)*func(bounds[0])<0:
        return bisection(func, [bounds[0], mid], threshold)
    else:
        return bisection(func, [mid, bounds[1]], threshold)

def newton_raphson(func, guess, threshold=(10**-4)):
    print('newt ran %f gives %f' % (guess,func(guess)))
    if func(guess) < threshold:
        return guess
    fprime = (func(guess+threshold)-func(guess))/threshold
    new_guess = guess - func(guess)/fprime
    return newton_raphson(func, new_guess, threshold)

def bound_states(V_0 = 10.0):
    # even = (lambda E: (V_0-E)**.5*numpy.tan((V_0-E)**.5)-(E)**.5)
    even = (lambda E:
        ((V_0-E)**.5*numpy.sin((V_0-E)**.5)
            -numpy.cos((V_0-E)**.5)*(E)**.5)
        )
    # odd = (lambda E: ((V_0-E)**.5)/numpy.tan((V_0-E)**.5)-(E)**.5)
    odd = (lambda E:
        ((V_0-E)**.5)*numpy.cos((V_0-E)**.5)
        -numpy.sin((V_0-E)**.5)*(E)**.5
        )
    step = .1
    guesses = numpy.linspace(0, V_0, int(V_0)*100)
    even_eval = numpy.vectorize(even)(guesses)
    # pyplot.plot(guesses, even_eval)
    # pyplot.ylim((-5, 5))
    # pyplot.show()
    even_states = []
    newt_even = []
    odd_states = []
    newt_odd = []
    for E_guess in numpy.linspace(0, V_0, int(V_0)/step):
        if even(E_guess)*even(E_guess+step) < 0:
            even_states.append(bisection(even, [E_guess, E_guess+step], threshold=10**-7))
            newt_even.append(newton_raphson(even, E_guess, threshold=10**-7))
        if odd(E_guess)*odd(E_guess+step) < 0:
            odd_states.append(bisection(odd, [E_guess, E_guess+step], threshold=10**-7))
            newt_odd.append(newton_raphson(odd, E_guess, threshold=10**-7))
    print('bound states for a %f deep well' % V_0)
    print(even_states)
    print((numpy.array(even_states)- numpy.array(newt_even))/numpy.array(newt_even))
    # print(numpy.array(even_states)-numpy.roll(even_states,1))
    print(odd_states)
    all_states = []
    for state in even_states+odd_states:
        if state > 0:
            all_states.append(abs(V_0-state))
    all_states = sorted(all_states)
    # print(all_states)
    deltas = numpy.array(all_states)-numpy.roll(all_states,1)
    # pyplot.plot(range(1,len(all_states)+1), all_states)
    # pyplot.show()


bound_states(10)
# bound_states(20.0)
# bound_states(30.0)
# bound_states(300.0)
# bound_states(2400.0)
