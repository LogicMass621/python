#!/usr/bin/python
numerator1=input('please enter the numerator of the first fraction:')
denominator1=input('please enter the denominator of the first fraction:')

print '{}/{}'.format(numerator1,denominator1)

numerator2=input('please enter the numerator of the second fraction:')
denominator2=input('please enter the denominator of the second fraction:')

print '{}/{}'.format(numerator2,denominator2)

numerator3 = numerator1 * numerator2
denominator3 = denominator1 * denominator2

print 'the answer is {}/{}'.format(numerator3,denominator3)