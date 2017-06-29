from matplotlib import pyplot

def lin_cong(a, c, M, r):
    # M, r and a should have few common factors
    r1 = r
    cycle=0
    while True:
        yield r
        r = (a*r+c)%M
        cycle+=1
        if(r1 == r or cycle > M):
            break

def part3():
    part2 = [element for element in lin_cong(57,1,256, 10)]
    # part2 = [element for element in lin_cong(11,3,210, 13)]
    print(len(part2))
    # print(part2)
    x = []
    y = []
    for pair_num in range(len(part2)/2):
        x.append(part2[2*pair_num])
        y.append(part2[2*pair_num+1])
    pyplot.scatter(x,y)
    pyplot.show()
    # pyplot.plot(range(len(part2)), part2)
    # pyplot.show()
    return

# generator = [result for result in lin_cong(4,1, 9, 3)]
generator = lin_cong(4,1, 9, 3)
print(generator)
# for result in generator:
#     print(result)
# part3()
