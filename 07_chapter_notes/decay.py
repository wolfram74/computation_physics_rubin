import numpy
from matplotlib import pyplot
'''
accepted value 2.6E-8
'''

def data_cleaner(x_vals, y_vals):
    cleaned_y = y_vals
    cleaned_x = x_vals
    index = 0
    while index < len(cleaned_y):
        if not numpy.isfinite(cleaned_y[index]):
            cleaned_y = numpy.delete(cleaned_y, index)
            cleaned_x = numpy.delete(cleaned_x, index)
            continue
        index+=1

    return cleaned_x, cleaned_y

def main():
    counts = numpy.array([32, 17, 21, 7, 8, 6, 5, 2, 3, 0, 4, 1])
    times = numpy.array([(step+0.5)*10*10**-9 for step in range(12)])
    sigma = 1.0
    # log_counts = numpy.log(counts/(times[1]-times[0]))

    log_counts = numpy.log(counts)
    pyplot.plot(times, log_counts)
    clean_times, clean_counts = data_cleaner(times, log_counts)
    S = len(clean_counts)*(1.0/sigma**2)
    Sx = sum(clean_times)/sigma**2
    Sxx = sum(clean_times**2)/sigma**2
    Sxy = sum(clean_counts*clean_times)/sigma**2
    Sy = sum(clean_counts)/sigma**2
    delta = S*Sxx-Sx**2
    slope = (S*Sxy-Sx*Sy)/delta
    const = (Sxx*Sy-Sx*Sxy)/delta
    print(const, slope, 1.0/slope)
    pyplot.plot(times, (times*slope+const))
    pyplot.show()
if __name__ == '__main__':
    main()
