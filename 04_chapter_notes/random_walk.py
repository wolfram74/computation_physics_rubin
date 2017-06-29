import random
from matplotlib import pyplot
import numpy

random.seed(None)

def make_step():
    stepx = random.random()-0.5
    stepy = random.random()-0.5
    normalizer = 1/(stepx**2+stepy**2)**.5
    return (stepx*normalizer, stepy*normalizer)

def random_walker(step_count, walk_count=1):
    distances = []
    for walk in range(walk_count):
        random.seed(None)
        position_x = [0]
        position_y = [0]
        distance = [0]
        for step in range(step_count-1):
            delta_r = make_step()
            position_x.append(position_x[-1]+delta_r[0])
            position_y.append(position_y[-1]+delta_r[1])
            distance.append(
                (position_x[-1]**2+position_y[-1]**2)**.5
                )
        pyplot.plot(position_x, position_y)
        distances.append(distance)
    # pyplot.show()
    steps = numpy.arange(step_count)
    root_steps = steps**.5
    mean_square_dist = 0
    for distance in distances:
        # print(len(root_steps))
        # print(len(distance))
        pyplot.plot(root_steps, distance)
        mean_square_dist += distance[-1]**2/walk_count
    print(mean_square_dist)
    # pyplot.show()
    return

total_steps = 10000
random_walker(total_steps, int(total_steps**.5))
