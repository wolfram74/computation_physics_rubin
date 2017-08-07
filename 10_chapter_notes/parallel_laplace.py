'''
Design notes:
    child_solvers number 1-4
    they are the four quadrants going counter-clockwise
    definitions
        BC: boundary condition, fixed
        BF: border fore, the border with child next in the loop
        BA: border aft, the border with the child behind in the loop
        NF: fore neighbors border (neighbor's BA)
        NA: aft neighbors border (neighbor's BF)
    as they are each different orientations row 0, col 0, row -1 and col -1 are different things
    child 1 row 0 and col -1 are BC's, col 0 is BF (reference NF), row -1 is BA (reference NA)
    child 2 row 0 and col 0 are BC's, row -1 is BF (reference NF), col -1 is BA (reference NA)
    child 3 row -1 and col 0 are BC's, col -1 is BF (reference NF), row 0 is BA (reference NA)
    child 4 row -1 and col -1 are BC's, row 0 is BF (reference NF), col 0 is BA (reference NA)
child_solver will have as arguments
    space_quadrant
    aft_pipe
    fore_pipe
    parent_pipe
will consist primarily of a loop
    send BF through fore_pipe and BA through aft_pipe
    recieve NF through  fore_pipe and NA through aft_pipe
    generate space_p1
    iterate through local space averaging, save biggest relative delta
        when to leave space alone and when to reference N(F/A) is the hard part
    send biggest delta through parent_pipe
    receive continuation signal through parent_pipe
    set space to space_p1
    increment loop counter
    if loop>threshold or end_signal, break
send space and proc id through parent_pipe
syntax notes:
    numpy.hstack((q2, q1)) -> top_half
    numpy.hsplit(top_half, 2) -> [q2, q1]

'''
import numpy
import multiprocessing
import time
from matplotlib import pyplot

def child_laplace(space, fore_pipe, aft_pipe, parent_pipe):
    proc_id = multiprocessing.current_process().name
    x_max = space.shape[1]-1
    y_max = space.shape[0]-1
    fore_pipe.send(proc_id)
    aft_pipe.send(proc_id)
    fore_id = fore_pipe.recv()
    aft_id = aft_pipe.recv()
    bf_index = -1 if (proc_id%4)/2.0 >= 1 else 0
    ba_index = -1 if (proc_id-1)/2.0 < 1 else 0
    is_finished = False
    print("%d has %d fore and %d aft" % (proc_id, fore_id, aft_id))
    print("%d has %d fore and %d aft" % (proc_id, bf_index, ba_index))
    while not is_finished:
        b_fore_aft = [[],[]]
        if proc_id%2 ==1:
            b_fore_aft[0] = [row[bf_index] for row in space] # extract col
        else:
            b_fore_aft[0] = space[bf_index] # extract row
        if proc_id%2 ==0:
            b_fore_aft[1] = [row[ba_index] for row in space] # extract col
        else:
            b_fore_aft[1] = space[ba_index] # extract row
        fore_pipe.send(b_fore_aft[0])
        aft_pipe.send(b_fore_aft[1])
        n_fore_aft = [[],[]]
        n_fore_aft[0] = fore_pipe.recv()
        n_fore_aft[1] = aft_pipe.recv()
        # print(proc_id, b_fore_aft)
        # print(proc_id, n_fore_aft)
        space_p1 = numpy.zeros(space.shape)
        # if proc_id == 1: # checking if quadrant 1 and 2 are getting the right terms
        #     print(n_fore_aft[0], proc_id)
        # if proc_id == 2:
        #     print(n_fore_aft[1], proc_id)
        biggest_delta = 0.0
        for y_index in range(space.shape[0]):
            for x_index in range(space.shape[1]):
                #account for boundary conditions
                if y_index == (0, y_max)[int((proc_id-1)/2.0)]:
                    space_p1[y_index][x_index]= space[y_index][x_index]
                    continue
                if x_index == (x_max, 0)[int((proc_id)%4/2.0)]:
                    space_p1[y_index][x_index]= space[y_index][x_index]
                    continue
                #account for bulk tiles
                if y_index not in (0, y_max) and x_index not in (0, x_max):
                    space_p1[y_index][x_index] = .25*(
                        space[y_index+1][x_index] +
                        space[y_index][x_index+1] +
                        space[y_index-1][x_index] +
                        space[y_index][x_index-1]
                        )
                #account for fringes
                else:
                    if proc_id==1:
                        if x_index == 0  and y_index == y_max:
                            space_p1[y_index][x_index] = .25*(
                                n_fore_aft[1][x_index] +
                                space[y_index][x_index+1] +
                                space[y_index-1][x_index] +
                                n_fore_aft[0][y_index]
                                )
                        elif x_index == 0:
                            space_p1[y_index][x_index] = .25*(
                                space[y_index+1][x_index] +
                                space[y_index][x_index+1] +
                                space[y_index-1][x_index] +
                                n_fore_aft[0][y_index]
                                )
                        elif y_index == y_max:
                            space_p1[y_index][x_index] = .25*(
                                n_fore_aft[1][x_index] +
                                space[y_index][x_index+1] +
                                space[y_index-1][x_index] +
                                space[y_index][x_index-1]
                                )
                    if proc_id==2:
                        if x_index == x_max  and y_index == y_max:
                            space_p1[y_index][x_index] = .25*(
                                n_fore_aft[0][x_index] +
                                n_fore_aft[1][y_index] +
                                space[y_index-1][x_index] +
                                space[y_index][x_index-1]
                                )
                        elif x_index == x_max:
                            space_p1[y_index][x_index] = .25*(
                                space[y_index+1][x_index] +
                                n_fore_aft[1][y_index] +
                                space[y_index-1][x_index] +
                                space[y_index][x_index-1]
                                )
                        elif y_index == y_max:
                            space_p1[y_index][x_index] = .25*(
                                n_fore_aft[0][x_index] +
                                space[y_index][x_index+1] +
                                space[y_index-1][x_index] +
                                space[y_index][x_index-1]
                                )
                    if proc_id==3:
                        if x_index == x_max  and y_index == 0:
                            space_p1[y_index][x_index] = .25*(
                                space[y_index+1][x_index] +
                                n_fore_aft[0][y_index] +
                                n_fore_aft[1][x_index] +
                                space[y_index][x_index-1]
                                )
                        elif x_index == x_max:
                            space_p1[y_index][x_index] = .25*(
                                space[y_index+1][x_index] +
                                n_fore_aft[0][y_index] +
                                space[y_index-1][x_index] +
                                space[y_index][x_index-1]
                                )
                        elif y_index == 0:
                            space_p1[y_index][x_index] = .25*(
                                space[y_index+1][x_index] +
                                space[y_index][x_index+1] +
                                n_fore_aft[1][x_index] +
                                space[y_index][x_index-1]
                                )
                    if proc_id==4:
                        if x_index == 0  and y_index == 0:
                            space_p1[y_index][x_index] = .25*(
                                space[y_index+1][x_index] +
                                space[y_index][x_index+1] +
                                n_fore_aft[0][x_index] +
                                n_fore_aft[1][y_index]
                                )
                        elif x_index == 0:
                            space_p1[y_index][x_index] = .25*(
                                space[y_index+1][x_index] +
                                space[y_index][x_index+1] +
                                space[y_index-1][x_index] +
                                n_fore_aft[1][y_index]
                                )
                        elif y_index == 0:
                            space_p1[y_index][x_index] = .25*(
                                space[y_index+1][x_index] +
                                space[y_index][x_index+1] +
                                n_fore_aft[0][x_index] +
                                space[y_index][x_index-1]
                                )
                #fucking fringes
                if space[y_index][x_index]!=0:
                    delta = (
                        space_p1[y_index][x_index]
                        - space[y_index][x_index]
                        )/space[y_index][x_index]
                else:
                    delta = space_p1[y_index][x_index]
                if delta > biggest_delta:
                    biggest_delta = delta

        parent_pipe.send(biggest_delta)
        is_finished = parent_pipe.recv()
        space = space_p1
    parent_pipe.send((proc_id, space))

    return

def stitch_together(set_of_spaces):
    sorted_spaces = sorted(set_of_spaces, key=(lambda space: space[0]))
    top_half = numpy.hstack((sorted_spaces[1][1], sorted_spaces[0][1]))
    bottom_half = numpy.hstack((sorted_spaces[2][1], sorted_spaces[3][1]))
    return numpy.vstack((top_half, bottom_half))

def print_space(space):
    for row in space:
        print('-'.join(["%03.f" % num for num in row]))

def draw_space(space):
    fig, axes = pyplot.subplots(1, 1)
    axes.imshow(space)
    # pyplot.show()
    pyplot.savefig("%d.png" % int(time.time()))

def parent_laplace():
    start_time = time.time()
    space_size = (100,100)
    threshold = 10**-4
    max_loops = 10**4
    v0 = (lambda x: 100.0)
    # v0 = (lambda x: numpy.cos(numpy.pi*x/space_size[0]))
    space = numpy.zeros(space_size)
    for x_index in range(space.shape[1]):
        space[0][x_index] = v0(x_index)
    top_half, bottom_half = numpy.vsplit(space, 2)
    q2, q1 = numpy.hsplit(top_half, 2)
    q3, q4 = numpy.hsplit(bottom_half, 2)
    children_spaces = [q1, q2, q3, q4]
    inter_child_pipes = [multiprocessing.Pipe(duplex=True) for loop in range(4)]
    processes = []
    child_control_pipes =[]
    loops = 0
    is_finished = False
    #processor set up
    for proc_index in range(4):
        control_pipe = multiprocessing.Pipe(duplex=True)
        processes.append(
            multiprocessing.Process(
                target=child_laplace,
                name=(proc_index+1),
                args=(
                    children_spaces[proc_index],
                    inter_child_pipes[(proc_index+1)%4][0],
                    inter_child_pipes[(proc_index)%4][1],
                    control_pipe[1]
                    )
                )
            )
        child_control_pipes.append(control_pipe[0])
        processes[-1].start()

    #processor monitoring
    while not is_finished:
        loops+=1
        max_deltas = []
        for pipe in child_control_pipes:
            max_deltas.append(pipe.recv())
        is_finished = all( [num < threshold for num in max_deltas])
        if loops > max_loops:
            is_finished = True
        if loops%10 == 0:
            print(loops, max_deltas)
        for pipe in child_control_pipes:
            pipe.send(is_finished)

    print('donezo')
    results = [pipe.recv() for pipe in child_control_pipes]
    space = stitch_together(results)
    # print_space(space)
    draw_space(space)
    end_time = time.time()
    print(loops)
    print('running time %f' % (end_time-start_time))
if __name__ == '__main__':
    parent_laplace()

'''
timing observations:
    when children do nothing and goes through 1E4 loops as fast as possible, takes a bout .4 seconds or 40 micro seconds per cycle of communication
serial laplace with constant edge at 10x10 takes 120 loops ~0.27 seconds
    same but 100x100 take 6085 loops ~ 208.60 seconds
parallel laplace with constant edge at 10x10 takes 124 loops ~.28 seconds
    100x100 took 6085 cyclesand about ~72.8 seconds

rewrite ideas:
    rotate pre-processing approach, rotate each sub-space so they're oriented the same, then instead of having 4-sets of logic for the unique cases, it'd be one set of logic that works on each.
    class based approach, each node is given it's \pm x or y pipes, or defineds whether or not those are BC's and on the update cycle, figure out if each neighbor is part of the bulk or a neighbors, then use those temp stored values instead of doing it in one swoop. Use getter and setter methods so it's amenable to testing.
'''
