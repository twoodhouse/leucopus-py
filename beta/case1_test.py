#!/usr/bin/python3.5

from case import Case
from hyp import Hyp
from tt import TT

tt1 = TT([0,1,1,0])

hyp = Hyp([], ["aUid1"], [tt1], [0])
c1 = Case(hyp, [], [1], [], rats = [], ratLocations = [], rCases = [])
# print(c1.genFullAttributes())
print(c1.genIat())
