#!/usr/bin/python3.5

from hyp import Hyp
from tt import TT

tt1 = TT([0,0,1,1])
tt2 = TT([0,0,1,1])

hyp = Hyp([tt1, tt2], [0, 1])
hyp.copy()
