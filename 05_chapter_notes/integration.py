'''
sample problem n(t)_dot = e^-t, N(1)=1-e^-1
x1) integrate arbitrary function using trapezoid, simpson and gaussian quadrature
x2) relative error |(numerical-exact)|/exact for each case at increasing n
    2, 10, 20, 40, 80, 160
x3) make log log plots of relative error vs N
    observe power laws
4) estimate power law of error relative to points
5.16.1
integrate sin(100x) and sin(100x)^x two different ways, describe challenges
5.16.2
Elliptic integral K(M) and approximation provided
5.16.3
evaluate integral numerically, compare with polynomial approximation
5.16.4
    a) calculate full pendulum period for several values of theta_0 with numerical methods
    b) use power series expression
    c) plot both results
5.16.5
    plot potential resulting from integral 5.85
    compare with 1/r
5.16.6
    calculate angular vector potential for current loop and plot

'''
import numpy
from matplotlib import pyplot

def trapezoid(y_vals, x_vals):
    y_vals[0]/=2.0
    y_vals[-1]/=2.0
    return numpy.sum(y_vals*x_vals[1])

def simpsons(y_vals, x_vals):
    pairs = (len(y_vals)-1)/2
    weights = numpy.tile([4,2], pairs)
    weights = numpy.delete(weights, -1)
    weights = numpy.append(weights, 1)
    weights = numpy.insert(weights,0,  1)
    return numpy.sum((weights*y_vals)*x_vals[1]/3.0)

def gaussian_leg(func, samples, interval):
    '''
    unlike other methods doesn't use evenly spaced inputs
    for n evaluation points, you would use the n solutions for the nth order legendre polynomial
    '''
    poly_coeffs = numpy.zeros(samples+1)
    poly_coeffs[-1]=1
    legendre = numpy.polynomial.legendre
    roots = legendre.legroots(poly_coeffs)
    poly_der_coeffs = legendre.legder(poly_coeffs)
    poly_der_vals = legendre.legval(roots, poly_der_coeffs)
    weights = []
    for index in range(len(roots)):
        weights.append(
            2.0/((1-roots[index]**2)*(poly_der_vals[index]**2))
            )
    slope = (interval[1]-interval[0])/2.0
    const = (interval[1]+interval[0])/2.0
    sample_points = map(lambda y: slope*y+const, roots)
    total = 0
    for index in range(len(sample_points)):
        total += func(sample_points[index])*slope*weights[index]
    return total

def error_comparisons():
    samples = [(2**num) for num in range(2,10)]
    samples = numpy.array(samples)
    exact = 1-numpy.exp(-1)
    trap_errs = []
    simp_errs = []
    gaus_errs = []
    for sample_count in samples:
        t_vals_even = numpy.linspace(0, 1, sample_count)
        ndot_vals_even = numpy.exp(-t_vals_even)
        t_vals_odd = numpy.linspace(0,1, sample_count-1)
        ndot_vals_odd = numpy.exp(-t_vals_odd)
        trapezoid_res = trapezoid(ndot_vals_even, t_vals_even)
        trapezoid_error = abs(trapezoid_res-exact)/exact
        simpsons_res = simpsons(ndot_vals_odd,t_vals_odd)
        simp_error = abs(simpsons_res-exact)/exact

        print('%d samples\t err_t %.12f \t err_s %.12f' % (sample_count, trapezoid_error, simp_error))
        gauss_result = gaussian_leg((lambda y: numpy.exp(-y)), sample_count, (0,1))
        gauss_err = abs(gauss_result-exact)/exact
        print('err_g %.16f' % gauss_err)
        trap_errs.append(trapezoid_error)
        simp_errs.append(simp_error)
        gaus_errs.append(gauss_err)
    log_samples = numpy.log(samples)
    pyplot.plot(log_samples, numpy.log(trap_errs))
    pyplot.plot(log_samples, numpy.log(simp_errs))
    pyplot.plot(log_samples, numpy.log(gaus_errs))
    pyplot.show()
    return

def p516_1():
    for power in range(1,20):
        samples = 2+2**power
        interval_eve = numpy.linspace(0, 2*numpy.pi, samples)
        interval_odd = numpy.linspace(0, 2*numpy.pi, samples-1)
        func1 = numpy.sin(100*interval_eve)
        # func2 = func1**interval #negative number to <1 power leads to imaginary results
        interval_eve2 = numpy.linspace(0, numpy.pi, samples)
        interval_odd2 = numpy.linspace(0, numpy.pi, samples-1)
        func2_eve =( numpy.sin(200*interval_eve2)**2)**interval_eve2
        func2_odd = (numpy.sin(200*interval_odd2)**2)**interval_odd2
        #evaluating at 2*interval agrees with wolfram alpha to several digits
        # print(func1[0:5])
        # print(func2_eve[0:5])
        trap_result = trapezoid(func1, interval_eve)
        simp_result = simpsons(numpy.sin(100*interval_odd), interval_odd)
        # print(samples, trap_result, simp_result)

        trap_result2 = trapezoid(func2_eve, interval_eve2)
        simp_result2 = simpsons(func2_odd, interval_odd2)
        print(samples, trap_result2, simp_result2)

def elliptic_aprox(m):
    m1 = 1-m
    a0, a1, a2 = (1.3862944, 0.1119723, 0.0725296)
    b0, b1, b2 = (0.5, 0.1213478, 0.0288729)
    return (a0+a1*m1+a2*m1**2)-(b0+b1*m1+b2*m1**2)*numpy.log(m1)

def elliptic_num(m, res = 3):
    the_vals = numpy.linspace(0, numpy.pi/2, 2**res+1)
    y_vals = (1-m*(numpy.sin(the_vals))**2)**(-0.5)
    # print(y_vals[0:5])
    return simpsons(y_vals, the_vals)

def elliptic_integrand(thet_m, thet):
    a = (numpy.sin(thet_m/2))**2
    b = (numpy.sin(thet/2))**2
    # print(a, b, a-b)
    return (a-b)**(-0.5)

def first_elliptic(m, theta):
    return (1-m*(numpy.sin(theta))**2)**(-0.5)

def second_elliptic(m, theta):
    return (1-m*(numpy.sin(theta))**2)**(0.5)


def ideal_pendu(thet_0, terms=3):
    numer = 1.0
    denom = 1.0
    total = 1.0
    for n in range(1, terms+1):
        # print n
        numer *= (2*n-1)
        denom *= (2*n)
        total += (numer/denom)**2*numpy.sin(thet_0/2)**(2*n)
    return total
    # return (1
    #     + (1.0/2.0)**2*numpy.sin(thet_0/2)**2
    #     + (3.0/8.0)**2*numpy.sin(thet_0/2)**4
    #     + (15.0/32.0)**2*numpy.sin(thet_0/2)**6
    #     )

def p516_3():
    m_vals = numpy.linspace(0, .95*numpy.pi,100)
    resolutions = range(2, 9)
    print(resolutions)
    for resolution in resolutions:
        errors = []
        for m in m_vals:
            apprx = elliptic_aprox(m)
            numer = elliptic_num(m, resolution)
            if abs(m-.4)<.01:
                print('%d %.3f %.12f' % (resolution, m, numer))
            errors.append(abs(apprx-numer)/abs(apprx))
        pyplot.plot(m_vals, numpy.log(errors))
    pyplot.show()
    return

def p516_4():
    thet_m_set = numpy.linspace(0.05, (numpy.pi-0.15), 11, endpoint=False)
    for thet_m in thet_m_set:
        m = (numpy.sin(thet_m/2))**2
        delta = 1
        n = 2
        last_series_guess =0
        while delta > 10**-5:
            series = ideal_pendu(thet_m, n)
            # print(series)
            delta = abs(series-last_series_guess)
            n+=1
            last_series_guess = series
        print("theta_m = %.3f, %d terms, series result %.6f" % (
            thet_m, n, last_series_guess
            ))
        delta = 1
        last_gauss_guess = 0
        n = 1
        while delta > 10**-5:
            n+=1
            gauss= gaussian_leg(
                (lambda x: first_elliptic(m, x)),
                # (lambda x: elliptic_integrand(thet_m, x)),
                # n, (0, thet_m))/numpy.pi
                n, (0,  numpy.pi/2))/(0.5*numpy.pi)
            delta = abs(last_gauss_guess-gauss)
            last_gauss_guess = gauss
        print("theta_m = %.3f, %d terms, gauss result %.6f" % (
            thet_m, n, last_gauss_guess
            ))
        print('ratio %.4f' % (last_gauss_guess/last_series_guess))
    thet_m_set = numpy.linspace(0.05, (numpy.pi-0.05), 31, endpoint=False)
    periods = []
    for thet_m in thet_m_set:
        m = (numpy.sin(thet_m/2))**2
        delta = 1
        n = 2
        while delta > 10**-6:
            n+=1
            gauss= gaussian_leg(
                (lambda x: first_elliptic(m, x)),
                # (lambda x: elliptic_integrand(thet_m, x)),
                # n, (0, thet_m))/numpy.pi
                n, (0,  numpy.pi/2))/(0.5*numpy.pi)
            delta = abs(last_gauss_guess-gauss)
            last_gauss_guess = gauss
        print(n, last_gauss_guess)
        periods.append(last_gauss_guess)
    pyplot.plot(thet_m_set, periods)
    pyplot.show()
    return

def p516_5():
    z_vals = numpy.linspace(0.05, 50.0, 100)
    V_0=1.0
    cut_radius = 1.0
    k_vals = 2*cut_radius*(z_vals**2+4*cut_radius**2)**(-1/2)
    phi_vals = []
    print(k_vals[0:5])
    for k_index in range(len(k_vals)):
        k = k_vals[k_index]
        z = z_vals[k_index]
        elliptic_result = gaussian_leg(
            (lambda phi: first_elliptic(k, phi)),
            20, (0, numpy.pi/2)
            )

        phi = (V_0/2.0)*(1-(k*z/numpy.pi*cut_radius)*elliptic_result)
        phi_vals.append(phi)
    pyplot.plot(z_vals, phi_vals)
    pyplot.plot(z_vals, V_0/z_vals)
    pyplot.ylim(0, 2)
    pyplot.show()
    return

def p516_6():
    current = 3.0
    loop_radius = 1.0
    mu_0 = 1.0
    figure, subplots = pyplot.subplots(1,2)

    def lead_coeff(I, a, r, tht):
        return 4*I*a/(a**2 + r**2 + 2*a*r*numpy.sin(tht))**.5

    def ksquared(a, r, tht):
        return 4*a*r*numpy.sin(tht)/(a**2 + r**2 + 2*a*r*numpy.sin(tht))

    thetas = numpy.linspace(0, 2*numpy.pi, 180)
    rad_0 = 1.1
    vec_pot_theta = []
    for theta in thetas:
        term1 = lead_coeff(current, loop_radius, rad_0, theta)
        kk = ksquared(loop_radius, rad_0, theta)
        term2 = gaussian_leg(
            (lambda x: first_elliptic(kk, x)), 20, (0, numpy.pi/2)
            )
        term3 = gaussian_leg(
            (lambda x: second_elliptic(kk, x)), 20, (0, numpy.pi/2)
            )
        vec_pot_theta.append(
            mu_0*term1*((2-kk)*term2-2*term3)/kk
            )
    subplots[0].plot(thetas, vec_pot_theta)

    radii = numpy.linspace(0, 15*loop_radius, 300)
    thet_0 = numpy.pi/3
    vec_pot_rad = []
    for radius in radii:
        term1 = lead_coeff(current, loop_radius, radius, thet_0)
        kk = ksquared(loop_radius, radius, thet_0)
        term2 = gaussian_leg(
            (lambda x: first_elliptic(kk, x)), 20, (0, numpy.pi/2)
            )
        term3 = gaussian_leg(
            (lambda x: second_elliptic(kk, x)), 20, (0, numpy.pi/2)
            )
        vec_pot_rad.append(
            mu_0*term1*((2-kk)*term2-2*term3)/kk
            )
    subplots[1].plot(radii, vec_pot_rad)

    pyplot.show()
    return

error_comparisons()
# print(gaussian_leg((lambda y: numpy.exp(-y)), 4, (0,1)))
# p516_1()
# p516_3()
# p516_4()
# p516_5()
# p516_6()
