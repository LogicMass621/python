#!/usr/bin/python3
import sys

if len(sys.argv) > 1:
    counter = sys.argv[1]
else:
    counter = input('Please enter a number:')

try:
    counter = int(counter)
except ValueError:
    print("Invalid argument: " + counter)
    
x = 1
while x <= counter:
    print(x)
    x = x+1
