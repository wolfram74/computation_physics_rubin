import random
from matplotlib import pyplot
import numpy

def decay_process(n0, decay_chance):
    population = [n0]
    while population[-1]>0:
        random.seed(None)
        decays = 0
        for roll in range(population[-1]):
            if random.random() <= decay_chance:
                decays += 1
        population.append(population[-1]-decays)
    time_steps = numpy.arange(len(population))
    return numpy.array(population), time_steps


lambda1 = .05
time_steps = 500
population, generation = decay_process(10000, .025)
decays = population-numpy.roll(population, 1)
pyplot.plot( generation, numpy.log(population))
pyplot.plot(generation, numpy.log(-decays))
# pyplot.plot(generation, population)
# pyplot.plot(generation, decays)
pyplot.show()


