##1.
##T F T F F
##
##2.
##11
##
##3.
##100000
##100000
##
##4.
##'num6 = 0:' (9/10)**10
##'num6 = 1:' (9/10)**9 * (1/10) .38
##"not all 6's:" 1 - 1/(10**10)
##
##5.
##y1 = (3*i)**5   Figure 2
##y2 = i**3       Figure 1
##y3 = 3**i       Figure 3
##
##6.
##16  #(16.0)
##'Circle with radius 4'
##'Circle with radius 8'
##
##7.
import random
maxVal = 1000
magNum = random.randint(0, maxVal)


def cmpGuess(guess, maxVal):
    if guess == magNum:
        return 0
    elif guess > magNum:
        return 1
    elif guess < magNum:
        return -1

def findNumber(maxVal):
    guess = round(maxVal/2)
    high = maxVal
    low = 0
    result = cmpGuess(guess, maxVal)
    while result!= 0:
        if result == -1:
            low = guess
        if result == 1:
            high = guess
        guess = genGuess(high, low)
        print "guess =", guess
        result = cmpGuess(guess, maxVal)
    return guess

def genGuess(high, low):
    return int((high+low)/2)

L = [0,1,2,3,4,5,6]
random.shuffle(L)

def merge_sort(L):
    pre = L[:]
    post = []

def tester():
    for i in range(10):
        yield i


gausses = []
for i in range(1000):
    gausses.append(round(random.gauss(0.0,.1), 4))

def gauss_gen(x, gausses=gausses):
    return x * random.choice(gausses)
def stdDev_gen(x, stdDev):
    return x + (random.choice(gausses)-1) * stdDev









