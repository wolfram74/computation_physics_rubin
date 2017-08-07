from matplotlib import pyplot
import numpy
import time


def time_step(tn):
    '''
    takes in a grid, returns a grid after 1 step of averaging and largest change
    '''
    tn1 = numpy.zeros(tn.shape)
    biggest_delta = 0
    x_max = tn.shape[1]-1
    y_max = tn.shape[0]-1
    for y_index in range(tn.shape[0]):
        for x_index in range(tn.shape[1]):
            if y_index in (0, y_max) or x_index in (0, x_max):
                tn1[y_index][x_index] = tn[y_index][x_index]
                continue
            tn1[y_index][x_index] = .25*(
                tn[y_index+1][x_index] +
                tn[y_index][x_index+1] +
                tn[y_index-1][x_index] +
                tn[y_index][x_index-1]
                )
            if tn1[y_index][x_index] !=0 and tn[y_index][x_index] != 0:
                delta = (tn1[y_index][x_index] - tn[y_index][x_index])/tn[y_index][x_index]
            else:
                delta = tn1[y_index][x_index]
            if delta > biggest_delta:
                biggest_delta = delta
    return tn1, biggest_delta

def print_space(space):
    for row in space:
        print(row)

def main():
    start_time = time.time()
    space_size = (100,100)
    v0 = (lambda x: 100.0)
    # v0 = (lambda x: numpy.cos(numpy.pi*x/space_size[0]))
    space = numpy.zeros(space_size)
    for x_index in range(space.shape[1]):
        space[0][x_index] = v0(x_index)
    loops = 0
    delta = 1
    while delta > 10**-4:
        space, delta = time_step(space)
        loops+=1
        if loops %10 == 0:
            print(loops, delta)
    print(loops)
    fig, axes = pyplot.subplots(1, 1)
    axes.imshow(space)
    # pyplot.show()
    pyplot.savefig("%d.png" % int(time.time()))
    end_time = time.time()
    print(end_time-start_time)

if __name__ == '__main__':
    main()
