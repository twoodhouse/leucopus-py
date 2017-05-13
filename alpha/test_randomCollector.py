#!/usr/bin/python3.5
from library import Librarian
from collector import RandomCollector
import requests
from temporalCaseManager import ICHypothesis, TemporalCaseManager
from truthTable import TruthTable
from branch import Branch

requests.get("http://buttonlight02.env:5001/resetall")
librarian = Librarian(infoRoutes=["http://buttonlight02.env:5001/checklight"], actionRoutes=["http://buttonlight02.env:5001/pushbutton"])
rc = RandomCollector(librarian)
# cases = rc.collect(masterRoute="http://buttonlight02.env:5001/checklight", count=100, allRoutes = False, chosenInfoRoutes = [], chosenActionRoutes = ["http://buttonlight02.env:5001/pushbutton"])
cases = rc.collectCases(masterRoute="http://buttonlight02.env:5001/checklight", count=90, allRoutes = True)
# tcm = TemporalCaseManager(cases, depth=1, allRoutes = False, chosenInfoRoutes = [], chosenActionRoutes = ["http://buttonlight02.env:5001/pushbutton"])
tcm = TemporalCaseManager(cases, depth=2, allRoutes = True)
tcm.iterate(2000, 1000)
for icase in tcm.bestHypothesis.icases:
    print(icase)
for truthTable in tcm.bestHypothesis.truthTables:
    print(truthTable)
print(tcm.getAccuracy())
b1 = Branch(librarian, [1], hypotheses = [tcm.bestHypothesis])
b2 = Branch(librarian, [0], branch = b1)
b3 = Branch(librarian, [0], branch = b2)
b4 = Branch(librarian, [1], branch = b3)
b5 = Branch(librarian, [1], branch = b4)
b6 = Branch(librarian, [1], branch = b5)
b7 = Branch(librarian, [1], branch = b6)



# requests.get("http://buttonlight01.env:5000/resetall")
# librarian = Librarian(infoRoutes=["http://buttonlight01.env:5000/checklight"], actionRoutes=["http://buttonlight01.env:5000/pushbutton", "http://buttonlight01.env:5000/resetbutton"])
# rc = RandomCollector(librarian)
# cases = rc.collect(masterRoute="http://buttonlight01.env:5000/checklight", count=1000)
# tcm = TemporalCaseManager(cases, 1)
# tcm.iterate(1000, 10)
# print(tcm.getAccuracy())

# requests.get("http://buttonlight02.env:5001/resetall")
# librarian = Librarian(infoRoutes=["http://buttonlight02.env:5001/checklight"], actionRoutes=["http://buttonlight02.env:5001/pushbutton"])
# rc = RandomCollector(librarian)
# cases = rc.collect(masterRoute="http://buttonlight02.env:5001/checklight", count=100)
# tcm = TemporalCaseManager(cases, 1)
# tcm.iterate(1000, 10)
# print(tcm.getAccuracy())
# b1 = Branch([0], hypothesis = tcm.bestHypothesis)
