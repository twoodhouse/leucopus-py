#!/usr/bin/python3.5

from case import Case
from hyp import Hyp
from tt import TT

tt1 = TT([0,1,1,0])

hyp = Hyp([], [0], [tt1], [0])
c1 = Case(hyp, [], [1], None, rats = [], ratLocations = [], rCases = [])
print(c1.genFullAttributes())

c2 = c1.genNext([], [0])
print(c2.genFullAttributes())

c3 = c2.genNext([], [0])
print(c3.genFullAttributes())

c4 = c3.genNext([], [0])
print(c4.genFullAttributes())

c5 = c4.genNext([], [1])
print(c5.genFullAttributes())

c6 = c5.genNext([], [1])
print(c6.genFullAttributes())
