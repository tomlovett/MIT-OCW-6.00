'1.1 - F \
1.2 - F  \
1.3 - F  \
1.4 - T  \
1.5 - F'

#2.
'100000, 100000, 100000 \
T T T'

#3.
'y1 - BL \
y2 - TR  \
y3 - BR  \
y4 - TL  '

#4.
'Rectangle with area 6'
'Square with area 36'
'Circle with diameter 2'
'Rectangle with area 6'
'Square with area 36'
'Circle with diameter 2'

5.
import random

def simThrows(numFlips):
    flips, fours, counter = [], [], 0
    for i in range(numFlips):
        temp = []
        fours.append(0)
        for i in range(10):
            temp.append(random.randint(0,1))
        flips.append(temp)
    for f in flips:
        for i in range(7):
            if fourSquare(f, i) is True:
                fours[counter] = 1
        counter += 1
    return sum(fours)/float(numFlips)
        
def fourSquare(L, index):
    if L[index] == 1 and L[index + 1] == 1 and L[index + 2] == 1 and L[index + 3] == 1:
        return True
    else:
        return False
# A 1/0 probability, or how many per? I think he wants 1/0

1/16 * 6
1/(2**4)

6.
'Yes, fitting both nth degree and an (n+1th) degree will most likely give you \
one good fit. Assuming one does not consider a n**1 function a polynomial. \
Which one fits better depends whether the polynomial is even or odd degree. \
This is because there are two basic shapes to polynomial functions, the parabola \
or the horizontal S-curve. Because this applies to the original function and the \
polyfit functions alike, if one uses polyfit with n and n+1 degree, one of the two \
will match.'

7.
'data abstraction - D - O(n)        \
merge sort - B -divide and conquer  \
polymorphism - G -mutability        \
hashing - E - O(1) (d O(n))         '
