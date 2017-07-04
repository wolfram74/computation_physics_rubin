import numpy
from matplotlib import pyplot
import sympy

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

    pyplot.scatter(energy, cross_section)
    pyplot.plot(smooth_energy, interpolated)
    pyplot.show()
    return

if __name__ == '__main__':
    main()
