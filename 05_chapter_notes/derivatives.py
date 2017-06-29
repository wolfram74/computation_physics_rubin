'''
problem 5.5.1
using forward, central and extrapolated differences, do derivatives of
 cos(t) and e^t at t = .1, 1, 100
 a) print out numerical derivative and relative error e as functions of h
 b) plot log error vs log h, compared with derived estimates agree for minimal error
 c) determine where modeling errors dominate and where rounding errors dominate
problem 5.6.1 page 90 pdf 114
    write a program to calculate second derivative of cos(t) using
    eq5.22 and 5.23, start with h=pi/10 and continue till h is at machine precision
    note any differences
'''

import numpy
from matplotlib import pyplot

def forward_diff(func, argument, step_size):
    return (func(argument+step_size)-func(argument))/step_size

def central_diff(func, argument, step_size):
    return (
        func(argument+step_size/2)-func(argument-step_size/2)
        )/step_size

def extrapolated_diff(func, argument, step_size):
    return (
        (4*central_diff(func, argument, step_size/2)*step_size)
        -(central_diff(func, argument, step_size)*step_size)
        )/(3*step_size)

def dcos(x):
    return -numpy.sin(x)

def ddeq22(func, arg,step_size):
    return (
        (func(arg+step_size)-func(arg))
        -(func(arg)-func(arg-step_size))
        )/step_size**2

def ddeq23(func, arg,step_size):
    return (
        func(arg+step_size)
        +func(arg-step_size)
        -2*func(arg)
        )/step_size**2

def p551():
    '''
    generate 6 plots: 2 functions at 3 arguments,
        each plot contains errors vs step_size of the 3 different methods

    '''
    step_sizes = numpy.array([.8**num for num in range(30)])
    args = [.1, 1.0, 100.0]
    diff_methods = [forward_diff, central_diff, extrapolated_diff]
    base_function = [numpy.cos, numpy.exp]
    base_label = ['cos', 'exp']
    derivs = [dcos, numpy.exp]
    figure, subplots = pyplot.subplots(2,3)
    for subject_ind in range(len(base_function)):
        print(base_function[subject_ind])
        for arg_ind in range(len(args)):
            arg = args[arg_ind]
            num_errors = []
            for method in diff_methods:
                errors = []
                for size in step_sizes:
                    num_diff = method(base_function[subject_ind] ,arg,size)
                    analytic_diff = derivs[subject_ind](arg)
                    errors.append(
                        abs(num_diff-analytic_diff)/abs(analytic_diff)
                        )
                errors = numpy.array(errors)
                num_errors.append(errors)
                subplots[subject_ind, arg_ind].plot(numpy.log10(step_sizes), numpy.log10(errors))
                subplots[subject_ind, arg_ind].set_title(
                    'log of errors for %s at %.2f' % (base_label[subject_ind],arg)
                    )
    pyplot.show()
    return

def p561():
    step_sizes = numpy.array([.75**num for num in range(90)])
    arg = numpy.pi/4
    analytic = -numpy.cos(arg)
    print(analytic)
    err22 = []
    err23 = []
    for step in step_sizes:
        # print(ddeq22(numpy.cos, arg, step))
        # print(ddeq22(numpy.cos, arg, step)-analytic)
        err22.append(
            abs(ddeq22(numpy.cos, arg, step)-analytic)/abs(analytic)
            )
        err23.append(
            abs(ddeq23(numpy.cos, arg, step)-analytic)/abs(analytic)
            )
    # err22 = numpy.array(err22)
    # print(len(step_sizes), len(err22), numpy.log10(err22))
    pyplot.plot(numpy.log10(step_sizes), numpy.log10(err22))
    pyplot.plot(numpy.log10(step_sizes), numpy.log10(err23))
    pyplot.show()
    return

p551()
# p561()
