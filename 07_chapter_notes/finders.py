def bisection(func, bounds=[0.0,1.0], threshold=(10**-4), delta = 10.0):
    if func(bounds[0])*func(bounds[1]) > 0:
        return False
    mid = (bounds[0]+bounds[1])/2
    # print('bisect ran %f gives %f' % (mid, func(mid)))
    new_delta = abs(func(bounds[0]) - func(bounds[1]))
    if delta < new_delta:
        return float('NaN')
    if abs(func(mid))<threshold:
        return mid
    if func(mid)*func(bounds[0])<0:
        return bisection(func, [bounds[0], mid], threshold)
    else:
        return bisection(func, [mid, bounds[1]], threshold)

def newton_raphson(func, guess, threshold=(10**-4)):
    # print('newt ran %f gives %f' % (guess,func(guess)))
    if abs(func(guess)) < threshold:
        return guess
    fprime = (func(guess+threshold)-func(guess))/threshold
    new_guess = guess - func(guess)/fprime
    return newton_raphson(func, new_guess, threshold)
