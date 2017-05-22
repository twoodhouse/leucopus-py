#!/usr/bin/python3.5

from palette import Palette
from hyp import Hyp
from tt import TT
from environments import TempButton, ToggleButton, TwoTempButton

env = TwoTempButton()

tt1 = TT([0,1,1,0])
hyp = Hyp(infoIndeces = [], actionIndeces = [0], tts = [tt1], iniTats = [0], rHyps = [], rHypLocations = [], iniRat = 0)

frameActions = [[0], [0], [1], [1], [1], [1], [1], [1], [1], [1], [0], [0], [0], [1], [1], [1], [1], [1], [0]]

initialIats, initialAats = env.runFrame(frameActions[0])
foundationPalette = Palette(iats = initialIats, aats = initialAats, isFoundation = True, hyps = [hyp])
print(foundationPalette.iats, foundationPalette.aats)
palette = foundationPalette
for frameAction in frameActions[1:]:
    newIats, newAats = env.runFrame(frameAction)
    palette = palette.genNext(iats = newIats, aats = newAats)
    print(palette.iats, palette.aats)

print("*******************")
foundationPalette.trainHypsUsingDownstreamAts()

pFrameActions = [[0], [0], [1], [1], [1], [1], [1], [1], [1], [1], [0], [0], [0], [1], [1], [1], [1], [1], [0]]

print(foundationPalette.iats, foundationPalette.aats)
palette = foundationPalette
for pFrameAction in pFrameActions[1:]:
    newIats, newAats = env.runFrame(pFrameAction)
    palette = palette.genNext(aats = newAats)
    print(palette.iats, palette.aats)

# print(str(palette))
#
# palette2 = palette.genNext(iats = [0], aats = [1])
# print(str(palette2))
#
# palette3 = palette2.genNext(iats = [0], aats = [1])
# print(str(palette3))
#
# palette4 = palette3.genNext(iats = [0], aats = [1])
# print(str(palette4))
#
#
# palette5 = palette4.genNext(aats = [1])
# print(palette5)
# palette6 = palette5.genNext(aats = [1])
# print(palette6)
# palette7 = palette6.genNext(aats = [1])
# print(palette7)
