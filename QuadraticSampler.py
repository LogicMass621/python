#!/usr/bin/python3
import math
import sys

a = float(input('What is A:'))
b = float(input('What is B:'))
c = float(input ('What is C:'))

domain1 = float(input('What is the lower number in the domain:'))
domain2 = float(input('What is the higher number in the domain:'))
interval = float(input('What is the interval you want to sample:'))

x = domain1

while x <= domain2:
    y = a * (x**2) + b * x + c
    print(repr(round(x,4)).rjust(6),        #column x
          '|',                                                         # divider
          repr(round(y,4)).rjust(6))             # column y
    x = x +interval
