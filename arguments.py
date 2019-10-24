#!/usr/bin/python
import sys
print sys.argv
l = len(sys.argv)

for i in range(l):
    print ("argument " + str(i) + " is: " + sys.argv[i])
