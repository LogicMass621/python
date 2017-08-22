#!/usr/bin/python
a, b = 0, 1
while b < 10:
	print("BEFORE: ",a,b)
	a, b = b, a+b
	print("AFTER: ",a,b)

