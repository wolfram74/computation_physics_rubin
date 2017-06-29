import random
import numpy
import mod_cycles

def moment_check(samples, check_count=4):
    results = []
    sample_size = len(samples)
    deviation = 1.0/(sample_size**.5)
    chi_square = 0
    for k in range(1,check_count+1):
        results.append(
            sum(
                map(lambda x: x**k, samples)
                )/sample_size
            )
        expected = 1.0/(k+1)
        chi_square += (
                (results[-1]-expected)/deviation
            )**2

    return results, chi_square

def near_correlation(samples, check_count = 4):
    sample_size = len(samples)
    results = []
    numpy_samples = numpy.array(samples)
    for check in range(check_count):
        shift = int(random.random()*sample_size)
        results.append(
            (
                shift,
                sum(numpy_samples*numpy.roll(numpy_samples,shift))/sample_size
                )
            )
    return results

def ling_cong_comparisons():
    dec_randos = [float(element)/787 for element in mod_cycles.lin_cong(57,1,787, 10)]
    bad_randos = [float(element)/858 for element in mod_cycles.lin_cong(58,1,858, 10)]
    print(dec_randos[0:10])
    print(bad_randos[0:10])
    dec_moments = moment_check(dec_randos)
    bad_moments = moment_check(bad_randos)
    print(dec_moments)
    print(bad_moments)
    return

randos = [random.random() for count in range(1000)]
moments = moment_check(randos)
print(moments)
correlations = near_correlation(randos)
print(correlations)
'''
consider:
solar panels have finite life span
batteries have finite life span
annual end of life mass budget to deal with for 3E8 peoples worth of power?
'''
