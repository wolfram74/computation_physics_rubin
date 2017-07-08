import numpy
from matplotlib import pyplot
import sympy
# from scipy.interpolate import interp1d

def lagrange_interp(x_vals, y_vals):
    global_coeffs = numpy.zeros(len(x_vals))
    x = sympy.symbols('x', real=True)
    for ind_j in range(len(x_vals)):
        product = 1
        for ind_i in range(len(x_vals)):
            if ind_i == ind_j:
                continue
            product *= (x-x_vals[ind_i])/(x_vals[ind_j]-x_vals[ind_i])
        product *= y_vals[ind_j]
        coeffs = sympy.Poly(product.expand(), x, domain='QQ').coeffs()
        float_coeffs = numpy.array([float(sympy.N(c)) for c in coeffs])
        deficit = len(x_vals)-len(float_coeffs)
        if deficit > 0:
            float_coeffs = numpy.pad(float_coeffs, (0, deficit), 'constant')
        global_coeffs += float_coeffs

    return global_coeffs

def cubic_spline(x_vals, y_vals):
    #referencing this https://www.math.ntnu.no/emner/TMA4215/2008h/cubicsplines.pdf
    #and also https://en.wikipedia.org/wiki/Spline_(mathematics)#Algorithm_for_computing_natural_cubic_splines
    delx_vals = []
    dely_vals = []
    slope_vals = []
    for index in range(len(x_vals)-1):
        delx_vals.append(x_vals[index+1]-x_vals[index])
        dely_vals.append(y_vals[index+1]-y_vals[index])
        slope_vals.append(float(dely_vals[-1])/float(delx_vals[-1]))
    print('delx', delx_vals[0:5])
    print('slopes', slope_vals[0:5])
    v_vals = []
    u_vals = []
    for index in range(1, len(slope_vals)):
        v_vals.append(2*(delx_vals[index]+delx_vals[index-1]))
        u_vals.append(6*(slope_vals[index]-slope_vals[index-1]))
    print('v', v_vals[0:5])
    print('u', u_vals[0:5])
    matrix = numpy.zeros((len(v_vals),len(v_vals)))
    matrix[0][0] = v_vals[0]
    for index in range(1, len(v_vals)):
        matrix[index][index] = v_vals[index]
        matrix[index-1][index] = delx_vals[index-1]
        matrix[index][index-1] = delx_vals[index-1] #candidate for fuckery
    if len(v_vals) <5:
        print(matrix)
    z_vals = numpy.linalg.solve(matrix, numpy.array(u_vals))
    z_vals = numpy.append(z_vals, 0)
    z_vals = numpy.insert(z_vals, 0, 0)
    print('z', z_vals[0:5])
    interval_funcs = cubic_intervals(z_vals, x_vals, y_vals, delx_vals)
    print(len(interval_funcs))
    print(interval_funcs[0](0.5))
    print(interval_funcs[-1](0.5))
    def interpolator(x_in, x_vals):
        if x_in <= x_vals[0]:
            return interval_funcs[0](x_in)
        if x_in > x_vals[-1]:
            return interval_funcs[-1](x_in)
        index = 0

        while True:
            if x_in <= x_vals[index+1] and x_in >= x_vals[index]:
                break
            index+=1
        # print(index)
        # print(x_vals[index], x_in, x_vals[index+1])
        a = z_vals[index+1]/(6.0*delx_vals[index])
        b = z_vals[index]/(6.0*delx_vals[index])
        c = y_vals[index+1]/delx_vals[index]-a
        d = y_vals[index]/delx_vals[index]-b
        print([a,b,c,d])
        result = (a*(x_in-x_vals[index])**3
                    +b*(x_vals[index+1]-x_in)**3
                    +c*(x_in-x_vals[index])
                    +d*(x_vals[index+1]-x_in))
        return result
    return interpolator

def cubic_intervals(z_vals, x_vals, y_vals, delx_vals):
    intervals = []
    for index in range(len(delx_vals)):
        a = z_vals[index+1]/(6.0*delx_vals[index])
        b = z_vals[index]/(6.0*delx_vals[index])
        c = y_vals[index+1]/delx_vals[index]-a
        d = y_vals[index]/delx_vals[index]-b
        intervals.append(
            (lambda x: a*(x-x_vals[index])**3
                        +b*(x_vals[index+1]-x)**3
                        +c*(x-x_vals[index])
                        +d*(x_vals[index+1]-x))
            )
    return intervals

def max_and_full_width(x_vals, y_vals):
    max_index = 0
    max_val = -1000.0
    for x_index in range(len(x_vals)):
        if y_vals[x_index]>max_val:
            max_index = x_index
            max_val = y_vals[x_index]
    shift = 1
    left_half = False
    right_half = False
    while shift+max_index < len(x_vals) and max_index-shift > -1:
        if y_vals[max_index+shift]/max_val <= .5 and not right_half:
            right_half = max_index+shift
            print('found right')
        if y_vals[max_index-shift]/max_val <= .5 and not left_half:
            left_half = max_index-shift
            print('found left')
        shift+=1
        if right_half and left_half:
            break
    av_width = (x_vals[right_half]-x_vals[left_half])
    return (max_val, av_width)

def main():
    energy = [0,25,50,75,100,125,150,175,200]
    cross_section = [10.6,16.0,45.0,83.5,52.8,19.9,10.8,8.25,4.7]
    print(len(cross_section))
    cross_section_err = [9.34,17.9,41.5,85.5,51.5,21.5,10.8,6.29,4.14]

    lagrange_coeffs = lagrange_interp(energy, cross_section)
    points = 200
    smooth_energy = numpy.linspace(energy[0], energy[-1], points)
    interpolated = numpy.zeros(points)
    order = len(lagrange_coeffs)-1
    for coeff_index in range(order+1):
        interpolated += smooth_energy**(order-coeff_index)*(lagrange_coeffs[coeff_index])
    max_width = max_and_full_width(smooth_energy, interpolated)
    print(max_width, 'vs', (78, 55))

    pyplot.scatter(energy, cross_section)
    pyplot.plot(smooth_energy, interpolated)

    # cubic_sol = interp1d(energy, cross_section, kind='cubic')
    cubic_sol = cubic_spline(energy, cross_section)
    cubic_interp = []
    for value in smooth_energy:
        cubic_interp.append(cubic_sol(value, energy))
    # cubic_interp = numpy.vectorize(cubic_sol)(smooth_energy, energy)
    test = cubic_spline([0.9, 1.3, 1.9, 2.1], [1.3, 1.5, 1.85, 2.1])
    test(.91, [0.9, 1.3, 1.9, 2.1])
    test(1.31, [0.9, 1.3, 1.9, 2.1])
    pyplot.plot(smooth_energy, cubic_interp)
    # pyplot.show()
    return

if __name__ == '__main__':
    main()
