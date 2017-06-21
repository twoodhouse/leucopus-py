#!/usr/bin/python3.5

from node import Stroke, Logger, Input

# construct web
i1 = Input()

s1 = Stroke(False)
s2 = Stroke(False)
s3 = Stroke(False)
s4 = Stroke(False)
s5 = Stroke(False)
s6 = Stroke(False)
s7 = Stroke(False)
# s8 = Stroke(False)


l1 = Logger()
l1.setSourceNode(s1)
l2 = Logger()
l2.setSourceNode(s2)
l3 = Logger()
l3.setSourceNode(s3)
l4 = Logger()
l4.setSourceNode(s4)
l5 = Logger()
l5.setSourceNode(s5)
l6 = Logger()
l6.setSourceNode(s6)
l7 = Logger()
l7.setSourceNode(s7)
# l8 = Logger()
# l8.setSourceNode(s8)

s1.setSourceNodes([i1, i1])
s2.setSourceNodes([i1, s1]) #constant
s3.setSourceNodes([s7, s2])
s4.setSourceNodes([s3, s3])
s5.setSourceNodes([s3, s4]) #constant
s6.setSourceNodes([s5, i1])
s7.setSourceNodes([s6, s6])
# s8.setSourceNodes([])

i1Values = [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1]
for i, iVal in enumerate(i1Values):
    bVal = bool(iVal)
    i1.activate(i, iVal)
    i1.proceed(i)

print(i1Values)
print()
print(l1.timeSeries)
print(l2.timeSeries)
print(l3.timeSeries)
print(l4.timeSeries)
print(l5.timeSeries)
print(l6.timeSeries)
print(l7.timeSeries)
# print(l8.timeSeries)
