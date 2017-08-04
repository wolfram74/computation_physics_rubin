import multiprocessing
import time
import random

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

def communicating_worker(pipe):
    message = random.random()
    proc_id = multiprocessing.current_process().name
    print('proc %d made %f' % (proc_id, message))
    pipe.send(message)
    recieved = pipe.recv()
    print('proc %d got %f' % (proc_id, recieved))

def piping_test():
    print('ran')
    processes = []
    pipes = multiprocessing.Pipe(duplex=True)
    for proc_id in range(2):
        processes.append(multiprocessing.Process(
            target=communicating_worker, args=(pipes[proc_id%2],),
            name=(proc_id+1)
            ))
        processes[-1].start()

if __name__ == '__main__':
    # speed_up_check()
    piping_test()
