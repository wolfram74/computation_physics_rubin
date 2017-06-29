import random
import numpy
import copy
from matplotlib import pyplot
'''
solve for 3 weights suspended on chords from a beam
'''

def derivative_mat(functions, unknowns, constants, delta=0.01):
    mat_a = numpy.zeros([len(functions),len(functions)])
    for row_ind in range(len(functions)):
        for col_ind in range(len(functions)):
            delta_vec = copy.copy(unknowns)
            delta_vec[col_ind] += delta
            f0 = functions[row_ind](unknowns, constants)
            f1 = functions[row_ind](delta_vec, constants)
            mat_a[row_ind][col_ind]= (f1-f0)/delta
    return numpy.matrix(mat_a)

def f_eval(functions, unknowns, constants):
    return numpy.array([ functions[index](unknowns, constants) for index in range(len(functions))])

def plot(vec, params):
    x_vals = [0]
    y_vals = [0]
    for index in range(len(params['l'])):
        x_vals.append(x_vals[-1]+params['l'][index]*vec[index+3])
    for index in range(2):
        y_vals.append(y_vals[-1]-params['l'][index]*vec[index])
    y_vals.append(y_vals[-1]+params['l'][index]*vec[2])
    # print(len(x_vals), len(y_vals))
    pyplot.plot(x_vals, y_vals)
    pyplot.show()
    return


def weight3():
    weights = [10.0, 20.0]
    lengths = [3.0, 4.0, 4.0]
    span = 8.0
    params = {'w':weights, 'l':lengths, 'L':span}
    trigs = []
    for loop in range(3):
        theta = random.random()*3.14
        trigs.append(numpy.cos(theta))
        trigs.append(numpy.sin(theta))
    x_guess = numpy.array([random.random()+1 for loop in range(len(lengths)*3)])
    # x_guess = numpy.array(trigs + [random.random()*3 for loop in range(len(lengths))])
    # x_guess = [.5,.5,.5,.5,.5,.5, 1.0, 1.0, 1.0]
    weight3_constraints = [
        (lambda vec, params:
            params['l'][0]*vec[3]
            +params['l'][1]*vec[4]
            +params['l'][2]*vec[5]-params['L']),
        (lambda vec, params:
            params['l'][0]*vec[0]
            +params['l'][1]*vec[1]
            -params['l'][2]*vec[2]),
        (lambda vec, params:
            vec[6]*vec[0]-vec[7]*vec[1]
            -params['w'][0]),
        (lambda vec, params:
            vec[6]*vec[3]-vec[7]*vec[4]),
        (lambda vec, params:
            vec[7]*vec[1]+vec[8]*vec[2]
            -params['w'][1]),
        (lambda vec, params:
            vec[7]*vec[4]-vec[8]*vec[5]),
        (lambda vec, params:
            vec[0]**2+vec[3]**2-1),
        (lambda vec, params:
            vec[1]**2+vec[4]**2-1),
        (lambda vec, params:
            vec[2]**2+vec[5]**2-1),
    ]
    last_guess= x_guess
    delta_mag = 100
    count = 0
    # print(x_guess)
    while delta_mag > .01:
    # for i in range(5):
        fprime = derivative_mat(weight3_constraints, x_guess, params, delta=0.0001)
        f_guess = f_eval(weight3_constraints, x_guess, params)
        x_shift = numpy.linalg.solve(fprime, -f_guess)
        # x_shift = -numpy.linalg.inv(fprime)*f_guess.reshape(len(f_guess),1)
        # print(fprime)
        # print(f_guess)
        # print(x_shift)
        # x_shift = -numpy.dot(numpy.linalg.inv(fprime),f_guess)
        x_guess = last_guess+x_shift
        delta_guess = last_guess-x_guess
        delta_mag = numpy.dot(delta_guess, delta_guess)
        last_guess = x_guess
        count+=1
        # print(x_guess)
        # print(delta_guess, delta_mag)
        # print(count)
        # print('\n')
        if count > 20 and delta_mag>100:
            print('non-converging')
            break
    print(count, x_guess, delta_mag)
    print(f_eval(weight3_constraints, x_guess, params))
    plot(x_guess, params)
    return

def testing():
    x_vec = numpy.array([1.0, 2.0])
    funcs = [
        (lambda vec, params: vec[0]**2),
        (lambda vec, params: vec[1]*vec[0])
        ]
    f_guess = f_eval(funcs, x_vec, {})
    f_prime = derivative_mat(funcs, x_vec, {}, 0.0001)
    print(f_guess)
    print(f_prime)

def main():
    print('farts')
    # testing()
    weight3()

if __name__ == '__main__':
    main()
