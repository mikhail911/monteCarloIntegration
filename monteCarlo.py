import numpy
import random
import time

def integral_function(x): 
    return(1/(numpy.cos(x) + 2))
    # result: https://www.wolframalpha.com/input/?i=integrate+1%2F(cos(x)+%2B+2)+from+0+to+6

def monte_carlo(xmin, xmax, ymin, ymax, N):
    whole_area = (xmax - xmin) * (ymax - ymin)
    points = 0 

    time_start = time.time()

    for i in range(N):
        x = xmin + (xmax - xmin) * random.random()
        y = ymin + (ymax - ymin) * random.random()

        if integral_function(x) > 0 and y > 0 and y <= integral_function(x):
            points += 1

    time_stop = time.time()
    total_time = time_stop - time_start
    result = whole_area * points / N
    
    return {'result': result, 'time': total_time, 'N': N}

# define limits
xmin = 0
xmax = 6
ymin = 0
x = numpy.linspace(xmin, xmax, 1000)
ymax = max(integral_function(x)) + 0.5 * max(integral_function(x))
Nmin = 100
Nmax = 10000

while Nmin <= Nmax:
    calc = monte_carlo(xmin, xmax, ymin, ymax, Nmin)
    print("Result: ", calc['result'], "Total time:", calc['time'], "N = ", calc['N']) 
    Nmin = Nmin * 10 
