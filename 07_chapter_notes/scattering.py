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
    # a+b(x-xi)**1+c(x-xi)**2+d(x-xi)**3
    # a maps to y vals
    # len(y_vals) = n+1, produces n intervals
    point_count = len(x_vals)
    delx_vals = [] #somtimes referred as h
    dely_vals = []
    alpha_vals = [0] #akin to 2nd derivative
    for index in range(point_count-1):
        delx_vals.append(float(x_vals[index+1]-x_vals[index]))
        dely_vals.append(float(y_vals[index+1]-y_vals[index]))
        if index > 0:
            alpha_vals.append(
                3*(
                    dely_vals[index]/delx_vals[index]
                    -dely_vals[index-1]/delx_vals[index-1]
                    )
                )
    print('delx', delx_vals[0:5])
    print('alpha', alpha_vals[0:5])
    c_vals = numpy.zeros(point_count)
    b_vals = numpy.zeros(point_count)
    d_vals = numpy.zeros(point_count)
    l_vals = numpy.zeros(point_count)
    u_vals = numpy.zeros(point_count)
    z_vals = numpy.zeros(point_count)
    l_vals[0]=1.0
    for index in range(1, point_count-1):
        l_vals[index] = 2*(x_vals[index+1]-x_vals[index-1])-delx_vals[index-1]*u_vals[index-1]
        u_vals[index] = delx_vals[index]/l_vals[index]
        z_vals[index] = (alpha_vals[index]-delx_vals[index-1]*z_vals[index-1])/l_vals[index]
    print('z', z_vals[0:5])
    l_vals[-1]=1.0
    for index in range(point_count-2, -1, -1):
        c_vals[index] = z_vals[index]-u_vals[index]*c_vals[index+1]
        b_vals[index] = (
            dely_vals[index]/delx_vals[index]
            - delx_vals[index]*(c_vals[index+1]+2*c_vals[index])/3.0
            )
        d_vals[index] = (c_vals[index+1]-c_vals[index])/(3*delx_vals[index])
    print('last cs', c_vals[-5:])


    def interpolator(x_in, x_vals):
        found = False
        index = 0
        if x_in <= x_vals[0]:
            index = 0
            found = True
        if x_in > x_vals[-1]:
            index = len(x_vals)-2
            found = True

        while not found:
            if x_in <= x_vals[index+1] and x_in >= x_vals[index]:
                break
            index+=1
        a = y_vals[index]
        b = b_vals[index]
        c = c_vals[index]
        d = d_vals[index]
        return (
            a + b*(x_in-x_vals[index])
            +c*(x_in-x_vals[index])**2
            +d*(x_in-x_vals[index])**3)
    return interpolator

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
    # test = cubic_spline([0.9, 1.3, 1.9, 2.1], [1.3, 1.5, 1.85, 2.1])
    # test(.91, [0.9, 1.3, 1.9, 2.1])
    # test(1.31, [0.9, 1.3, 1.9, 2.1])
    pyplot.plot(smooth_energy, cubic_interp)
    pyplot.show()
    return

if __name__ == '__main__':
    main()
