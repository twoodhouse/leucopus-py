#!/usr/bin/python3.5

from environments import TempButton, ToggleButton, TwoTempButton

tb = TwoTempButton()
print(tb.actionMethods)
print(tb.runFrame([0]))
print(tb.runFrame([1]))
print(tb.runFrame([1]))
print(tb.runFrame([1]))
print(tb.runFrame([0]))
print(tb.runFrame([1]))
print(tb.runFrame([0]))
print(tb.runFrame([0]))
print(tb.runFrame([1]))
