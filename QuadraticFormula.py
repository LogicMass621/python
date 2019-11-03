#!/usr/bin/python3
import math
import sys
a = float(input('What is A:'))
b = float(input('What is B:'))
c = float(input ('What is C:'))

sqroot = math.sqrt(b**2-4*a*c)

if sqroot<0:
    print('The answer is imaginary')
    sys.exit()

answer1 = (-b + sqroot) / (2*a)
answer2 = (-b - sqroot) / (2*a)

answer1 = round(answer1,4)
answer2= round(answer2,4)

answer1 = str(answer1)
answer2= str(answer2)

print('The answer is around '+answer1+' and '+answer2)
