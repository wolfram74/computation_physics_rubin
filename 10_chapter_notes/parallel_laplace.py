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

def child_laplace(space, fore_pipe, aft_pipe, parent_pipe):
    proc_id = multiprocessing.current_process().name
    fore_pipe.send(proc_id)
    aft_pipe.send(proc_id)
    fore_id = fore_pipe.recv()
    aft_id = aft_pipe.recv()
    bf_index = -1 if ((proc_id+1)%4)/2.0 > 1 else 0
    ba_index = -1 if proc_id/2.0 < 1 else 0
    is_finished = False
    print("%d has %d fore and %d aft" % (proc_id, fore_id, aft_id))
    while not is_finished:
        b_fore_aft = [[],[]]
        if proc_id%2 ==1:
            b_fore_aft[0] = [row[bf_index] for row in space] # extract col
        else:
            b_fore_aft[0] = space[bf_index] # extract row
        if proc_id%2 ==0:
            b_fore_aft[1] = [row[bf_index] for row in space] # extract col
        else:
            b_fore_aft[1] = space[bf_index] # extract row
        fore_pipe.send(b_fore_aft[0])
        aft_pipe.send(b_fore_aft[1])
        n_fore_aft = [[],[]]
        n_fore_aft[0] = fore_pipe.recv()
        n_fore_aft[1] = aft_pipe.recv()
        # if proc_id == 1: # checking if quadrant 1 and 2 are getting the right terms
        #     print(n_fore_aft[0], proc_id)
        # if proc_id == 2:
        #     print(n_fore_aft[1], proc_id)
        parent_pipe.send(1)
        is_finished = parent_pipe.recv()
    parent_pipe.send((proc_id, space))

    return

def stitch_together(set_of_spaces):
    sorted_spaces = sorted(set_of_spaces, key=(lambda space: space[0]))
    top_half = numpy.hstack((sorted_spaces[1][1], sorted_spaces[0][1]))
    bottom_half = numpy.hstack((sorted_spaces[2][1], sorted_spaces[3][1]))
    return numpy.vstack((top_half, bottom_half))

def parent_laplace():
    start_time = time.time()
    space_size = (10,10)
    threshold = 10**-4
    max_loops = 10**1
    # v0 = (lambda x: 100.0)
    v0 = (lambda x: numpy.cos(numpy.pi*x/space_size[0]))
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
    print(space)
    # while delta > threshold:
    #     space, delta = time_step(space)
    #     loops+=1
    #     if loops %10 == 0:
    #         print(loops, delta)
    # print(loops)
    # fig, axes = pyplot.subplots(1, 1)
    # axes.imshow(space)
    # # pyplot.show()
    # pyplot.savefig("%d.png" % int(time.time()))
    end_time = time.time()
    print('running time %f' % (end_time-start_time))
if __name__ == '__main__':
    parent_laplace()
