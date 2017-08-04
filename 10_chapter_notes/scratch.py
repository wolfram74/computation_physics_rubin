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
    messge = random.random()
    proc_id = multiprocessing.current_process().name
    print('proc %d made %f' % (proc_id, message))

def piping_test():
    print('ran')

if __name__ == '__main__':
    # speed_up_check()
    piping_test()
