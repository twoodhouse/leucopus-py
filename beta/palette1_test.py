#!/usr/bin/python3.5

from palette import Palette
from hyp import Hyp
from tt import TT

tt1 = TT([0,1,1,0])
hyp = Hyp(infoIndeces = [], actionIndeces = [0], tts = [tt1], iniTats = [0], rHyps = [], rHypLocations = [], iniRat = 0)

palette = Palette(iats = [0], aats = [0], isFoundation = True, hyps = [hyp])
print(str(palette))

palette2 = palette.genNext(iats = [0], aats = [1])
print(str(palette2))

palette3 = palette2.genNext(iats = [0], aats = [1])
print(str(palette3))

palette4 = palette3.genNext(iats = [0], aats = [1])
print(str(palette4))
