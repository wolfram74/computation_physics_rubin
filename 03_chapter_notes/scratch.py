import numpy
from matplotlib import pyplot
from scipy import special
import sympy

def quad_solver(a, b, c):
    plus1 = -b + (b**2-4*a*c)**0.5
    minus1 = -b - (b**2-4*a*c)**0.5
    plus2 = b + (b**2-4*a*c)**0.5
    minus2 = b - (b**2-4*a*c)**0.5
    return [
        ( plus1/(2*a), minus1/(2*a)),
        (-2*c/plus2, -2*c/minus2)
        ]

def quad_explore():
    for n in range(1,17):
        solutions = quad_solver(1, 1, 10**(-n))
        print(n, solutions)
        print((solutions[0][0]-solutions[1][0])/solutions[0][0])
        print((solutions[0][1]-solutions[1][1])/solutions[0][1])
        print('\n')
    a, b, c, e = sympy.symbols('a b c epsilon', real=True)
    terms = [a,b,c]
    x1 = (- b + sympy.sqrt(b**2 - 4 * a * c))/(2*a)
    x2 = -2*c /(b - sympy.sqrt(b**2 - 4 * a * c))
    print('method 1')
    sympy.pprint(x1)
    print('method 2')
    sympy.pprint(x2)
    print('error squared 1')
    error1 = 0
    for term in terms:
        error1+= sympy.diff(x1, term)**2 * e**2
    # sympy.pprint(error1)
    sympy.pprint(error1.simplify())
    sympy.pprint(error1.simplify().subs([(a,1),(b,1),(c,0.1)]))
    sympy.pprint(error1.simplify().subs([(a,1),(b,1),(c,0.001)]))
    sympy.pprint(error1.simplify().subs([(a,1),(b,1),(c,0.00001)]))
    sympy.pprint(error1.simplify().subs([(a,1),(b,1),(c,0.000000001)]))
    print('error squared 2')
    error2 = 0
    for term in terms:
        error2+= sympy.diff(x2, term)**2 * e**2
    # sympy.pprint(error2)
    sympy.pprint(error2.simplify())
    sympy.pprint(error2.simplify().subs([(a,1),(b,1),(c,0.1)]))
    sympy.pprint(error2.simplify().subs([(a,1),(b,1),(c,0.001)]))
    sympy.pprint(error2.simplify().subs([(a,1),(b,1),(c,0.00001)]))
    sympy.pprint(error2.simplify().subs([(a,1),(b,1),(c,0.0000001)]))
    sympy.pprint(error2.simplify().subs([(a,1),(b,1),(c,0.000000001)]))
    return

def sum1(n):
    #eq 3.10
    total = 0
    for i in range(1,2*n+1):
        total += (-1)**i * (float(i)/(float(i)+1))
    return total

def sum2(n):
    #eq 3.11
    totalp = 0
    totalm = 0
    for i in range(1,n+1):
        totalp += (2*float(i)/(2*float(i)+1))
        totalm +=  ((2*float(i)-1)/(2*float(i)))
    return totalp-totalm

def sum3(n):
    #eq 3.12
    total = 0
    for i in range(1,n+1):
        total += 1.0/(2*i*(2*i+1))
    return total

def p312p2():
    term_count = numpy.array([int(2**(exp/3)) for exp in range(3,60)])
    results = []
    for terms in range(40):
        result = [
            sum1(terms),
            sum2(terms),
            sum3(terms)
        ]
        results.append(result)
    bad_sum = numpy.vectorize(sum1)(term_count)
    good_sum = numpy.vectorize(sum3)(term_count)
    delta = bad_sum-good_sum
    y_vals = numpy.log(numpy.abs(delta/good_sum))
    x_vals = numpy.log(term_count)
    pyplot.plot(x_vals, y_vals)
    pyplot.show()
    return

def sum_up(terms):
    #to inspect intermediate points, make array and update last term based on second to last term
    total = 0
    for n in range(1, terms+1):
        total += 1.0/n
    return total

def sum_down(terms):
    # to inspect intermediate points... fuck
    total = 0
    for n in range(terms, 0, -1):
        total += 1.0/n
    return total

def p312p3():
    term_count = numpy.array([2**exp for exp in range(24)])
    upwards = numpy.vectorize(sum_up)(term_count)
    downwards = numpy.vectorize(sum_down)(term_count)
    delta = upwards-downwards
    sum_val = numpy.abs(upwards)+numpy.abs(downwards)
    y_vals = numpy.log(numpy.abs(delta/sum_val))
    x_vals = numpy.log(term_count)
    print(term_count)
    print(delta/sum_val)
    pyplot.plot(x_vals, y_vals)
    pyplot.show()
    return

def bessel_calculator_up(x, terms = 25):
    coeffs = numpy.zeros(terms)
    coeffs[0] = numpy.sin(x)/x
    coeffs[1] = numpy.sin(x)/x**2 - numpy.cos(x)/x
    for term in range(1, terms-1):
        coeffs[term+1] = (
            (2*term+1)*coeffs[term]/x
            -coeffs[(term-1)]
            )
        # print(coeffs)
    print(coeffs)
    return coeffs

def bessel_calculator_down(x, terms = 25):
    coeffs = numpy.zeros(terms)
    coeffs[-1] = 1.0
    coeffs[-2] = 1.0
    for term in range(terms-2, 0, -1):
        coeffs[(term-1)] = (
            (2.0*term+1.0)*coeffs[term]/x
            -coeffs[(term+1)]
            )
    # print(coeffs)
    scale = (numpy.sin(x)/x)/coeffs[0]
    normed_coeffs = coeffs*scale
    # print(normed_coeffs)
    return normed_coeffs

def p321(x_val = 0.1):
    terms = 25
    down_coeffs = bessel_calculator_down(x_val, terms)
    up_coeffs = bessel_calculator_up(x_val, terms)
    library_coeffs = special.spherical_jn(
        numpy.arange(terms),
        x_val
        )
    # print('library values')
    # print(library_coeffs)
    # print('down rel differences')
    # print((down_coeffs-library_coeffs)/library_coeffs)
    # print('up rel differences')
    # print((up_coeffs-library_coeffs)/library_coeffs)
    library_total = numpy.sum(library_coeffs)
    down_total = numpy.sum(down_coeffs)
    up_total = numpy.sum(up_coeffs)
    print('error compared with library result at %f' % x_val)
    print("down error %.10f" % ((down_total-library_total)/library_total))
    print("up error %.10f" % ((up_total-library_total)/library_total))
    print('relative difference at %f' %x_val)
    print( numpy.abs(down_total-up_total)/(
        numpy.abs(down_total)+numpy.abs(up_total)
        ) )
    return

def home_sin(x):
    prev_term = 1*x
    total = prev_term
    terms = [total]
    sums = [total]
    error = 10**-7
    count = 1
    while abs(prev_term/total) > error:
        count+=1
        denom = (2*count-1)*(2*count-2)
        term = (-x**2)*prev_term/denom
        total += term
        terms.append(term)
        sums.append(total)
        prev_term = term
    return {'sin':total, 'terms':terms, 'steps':sums, 'x': x}

def error_calc_sin(run_data):
    actual = numpy.sin(run_data['x'])
    log_errors = [numpy.log(abs((step-actual)/actual)) for step in run_data['steps']]
    return log_errors

def p331():
    print('evaluated at x=1.5^-1.5')
    try1 = home_sin(1.5**-1.0)['sin']
    print(
        'home_sin gets %.7f while numpy.sin gets %.7f, difference %.10f' %
        (try1, numpy.sin(1.5**-1.0), try1 - numpy.sin(1.5**-1.0))
        )
    print('evaluated 9.3~=3pi')
    try2 = home_sin(9.3)
    print('terms %s' % ', '.join([str(term) for term in try2['terms']]) )
    print('sum %.7f compared with %.7f' % (try2['sin'], numpy.sin(9.3)) )
    print('evaluating from %.7f to %.7f' % (1.5**-1, 1.5**12))
    trys = []
    for power in range(-1, 13):
        arg = 1.5**power
        trys.append(home_sin(arg))
        print(
            'comparing numpy with home sin at %.7f\n np %.7f hms %.7f' % (
                arg,
                numpy.sin(arg),
                trys[-1]['sin']
                )
            )
        print('')
    for trial in trys:
        errors = error_calc_sin(trial)
        term_numbers = range(1, len(errors)+1)
        pyplot.plot(term_numbers, errors)
        pyplot.ylim((-15,15))
        pyplot.xlim((0,30))
    pyplot.show()
    return

# quad_explore()
# p312p2()
# p312p3()
p321(.1)
for exp in range(-3, 6):
    p321(2.0**exp)

# p331()
