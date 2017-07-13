'''
page 185
Ximplement rk2,
Xfind or implement rk4
Xverify accuracy of rk2
    compare results with SHO
Xcompare results with rk4
examine equations 8.41 and 8.42
'''
import numpy
from matplotlib import pyplot
import copy

def rk2(func_vec, init_vec, t_end, step_size = 0.1):
    '''
    takes in function list length n, init_vec length n+1 formatted like (t, variables)
    returns array of vectors formated like init_vec indicating
    '''
    init_vec = numpy.array(init_vec)
    path = [init_vec]
    while path[-1][0] < t_end:
        curr_vec = copy.copy(path[-1])
        k1 = numpy.array([])
        for index in range(len(curr_vec)):
            k1= numpy.append(k1, step_size*func_vec[index](curr_vec))
        k2 = numpy.array([])
        for index in range(len(curr_vec)):
            k2= numpy.append(k2, step_size*func_vec[index](curr_vec+k1/2))
        path.append(path[-1]+k2)
    return path

def rk4(func_vec, init_vec, t_end, step_size = 0.1):
    '''
    takes in function list length n, init_vec length n+1 formatted like (t, variables)
    returns array of vectors formated like init_vec indicating
    '''
    init_vec = numpy.array(init_vec)
    path = [init_vec]
    while path[-1][0] < t_end:
        curr_vec = copy.copy(path[-1])
        k1 = numpy.array([])
        for index in range(len(curr_vec)):
            k1= numpy.append(k1, step_size*func_vec[index](curr_vec))
        k2 = numpy.array([])
        for index in range(len(curr_vec)):
            k2= numpy.append(k2, step_size*func_vec[index](curr_vec+k1/2))
        k3 = numpy.array([])
        for index in range(len(curr_vec)):
            k3= numpy.append(k3, step_size*func_vec[index](curr_vec+k2/2))
        k4 = numpy.array([])
        for index in range(len(curr_vec)):
            k4= numpy.append(k4, step_size*func_vec[index](curr_vec+k3))
        path.append(path[-1]+((k1+2*k2+2*k3+k4)/6.0))
    return path

def rk45(func_vec, init_vec, t_end, step_size = 0.1, precision=10**-6):
    '''
    takes in function list length n, init_vec length n+1 formatted like (t, variables)
    returns array of vectors formated like init_vec indicating
    '''
    init_vec = numpy.array(init_vec)
    path = [init_vec]
    check_mode = False
    guess = numpy.zeros(len(init_vec))
    check = numpy.zeros(len(init_vec))
    while path[-1][0] < t_end:
        curr_vec = copy.copy(path[-1])
        k1 = numpy.array([])
        for index in range(len(curr_vec)):
            k1= numpy.append(k1, step_size*func_vec[index](curr_vec))
        k2 = numpy.array([])
        for index in range(len(curr_vec)):
            k2= numpy.append(k2, step_size*func_vec[index](curr_vec+k1/2))
        k3 = numpy.array([])
        for index in range(len(curr_vec)):
            k3= numpy.append(k3, step_size*func_vec[index](curr_vec+k2/2))
        k4 = numpy.array([])
        for index in range(len(curr_vec)):
            k4= numpy.append(k4, step_size*func_vec[index](curr_vec+k3))
        if not check_mode:
            guess = path[-1]+((k1+2*k2+2*k3+k4)/6.0)
            step_size /= 2.0
        else:
            check = path[-1]+((k1+2*k2+2*k3+k4)/6.0)
        if check_mode:
            rel_diff = abs((guess[1]-check[1])/check[1])
        if check_mode and rel_diff < precision:
            # path.append(path[-1]+((k1+2*k2+2*k3+k4)/6.0))
            path.append(guess)
            step_size *= 2.0
    return path



def plot_paths(paths):
    #takes array of arrays of points formatted (t, x, v)
    for path in paths:
        times = []
        pos = []
        for point in path:
            times.append(point[0])
            pos.append(point[1])
        pyplot.plot(times, pos)
    pyplot.show()
    return

def sho_calibration():
    '''
    f=-w0**2*x leads to trig functions x=A*cos(w0*t)
    w0=2pi means at t=1, back to initial conditions
    '''
    w0 = numpy.pi*2
    sho_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: -config[1]*(w0)**2)
    ]
    rk2_errors=[]
    rk4_errors=[]
    step_sizes = numpy.array([1.5**(-power) for power in range(1,20)])
    for step in step_sizes:
        rk2_trail = rk2(sho_funcs, [0, 1.0, 0], 1.0, step_size=step)
        rk2_errors.append(
            abs(numpy.cos(w0*rk2_trail[-1][0]) - rk2_trail[-1][1])/numpy.cos(w0*rk2_trail[-1][0])
                )
        rk4_trail = rk4(sho_funcs, [0, 1.0, 0], 1.0, step_size=step)
        rk4_errors.append(
            abs(numpy.cos(w0*rk4_trail[-1][0]) - rk4_trail[-1][1])/numpy.cos(w0*rk4_trail[-1][0])
            )
        # plot_paths([rk2_trail, rk4_trail])
    print(rk4_errors[-5:])
    pyplot.plot(numpy.log10(step_sizes), numpy.log10(rk2_errors))
    pyplot.plot(numpy.log10(step_sizes), numpy.log10(rk4_errors))
    pyplot.show()
    return

def eq841():
    '''
    2y*ypp+y**2-yp**2=0
    '''
    nle_funcs = [
        (lambda config: 1),
        (lambda config: config[2]),
        (lambda config: (config[2]**2-config[1]**2)/(2.0*config[1]))
    ]

    step_counts = [500, 1000, 5000]
    t_end = 4.0
    error_paths = []
    for count in step_counts:
        step_size = t_end/count
        # t_vals = numpy.linspace(0, t_end, count)
        # analytic_vals = 1+numpy.sin(t_vals**4)
        rk4_trail = rk4(nle_funcs, [0.0, 1.0, 1.0], t_end, step_size)
        error_path = []
        for index in range(len(rk4_trail)):
            analytic_val = 1+numpy.sin(rk4_trail[index][0])
            rel_err = abs(rk4_trail[index][1]-analytic_val)/abs(analytic_val)
            error_path.append([rk4_trail[index][0], numpy.log10(rel_err)])
        error_paths.append(error_path)
    plot_paths(error_paths)
    return

def main():
    # sho_calibration()
    eq841()

if __name__ == '__main__':
    main()
