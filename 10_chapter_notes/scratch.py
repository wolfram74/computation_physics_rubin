import multiprocessing
import time
import random

'''
behaviors needed to do simulation:
    Xpassing data between child processes
    Xpassing data up stream to parent process
    Xpassing go/nogo data downstream to child processes
    Xgetting resulting data out of child processes to be stitched back together
'''

def square(x):
    return x**2

def collatz_length(x):
    n = 0
    while x != 1:
        if x%2 == 0:
            x/=2
        else:
            x = 3*x + 1
        n+=1
    return n

def speed_up_check():
    pool = multiprocessing.Pool(4)
    t = range(1,100000)
    print(type(t), len(t))
    pool_start = time.time()
    p_out = pool.map(collatz_length, t)
    pool_end = time.time()

    naive_start = time.time()
    n_out = map(collatz_length, t)
    naive_end = time.time()

    print(naive_end-naive_start)
    print(pool_end-pool_start)
    print(n_out == p_out)

def communicating_worker(pipe, parent_pipe):
    proc_id = multiprocessing.current_process().name
    loops = 0
    done = False
    lowest_val = 1.0
    while loops < 100 and not done:
        message = random.random()
        if message < lowest_val:
            lowest_val = message
        print('proc %d made %f on loop %d' % (proc_id, message, loops))
        print('proc %d has low of %f' % (proc_id, lowest_val))
        pipe.send(message)
        recieved = pipe.recv()
        print('proc %d got %f' % (proc_id, recieved))
        parent_pipe.send(lowest_val)
        done = parent_pipe.recv()
        print('proc %d is done %s on loop %d' % (proc_id, done, loops))

        loops+=1
    print('finished proc %d' % (proc_id))
    parent_pipe.send((proc_id, lowest_val))
    return

def piping_test():
    print('ran')
    processes = []
    pipes = multiprocessing.Pipe(duplex=True)
    children_pipes = []
    threshold = .1
    loops = 0
    is_finished = False
    for proc_id in range(2):
        control_pipe = multiprocessing.Pipe(duplex=True)
        processes.append(multiprocessing.Process(
            target=communicating_worker,
            args=(pipes[proc_id%2],control_pipe[0]),
            name=(proc_id+1)
            ))
        children_pipes.append(control_pipe[1])
        processes[-1].start()
    while not is_finished:
        low_vals = []
        for pipe in children_pipes:
            low_vals.append(pipe.recv())
        is_finished = all( [num < threshold for num in low_vals])
        for pipe in children_pipes:
            pipe.send(is_finished)
        loops+=1
        print('on loop %d and is finished %s' % (loops, is_finished))
    print('donezo')
    results = [pipe.recv() for pipe in children_pipes]
    print(results)
if __name__ == '__main__':
    # speed_up_check()
    piping_test()
