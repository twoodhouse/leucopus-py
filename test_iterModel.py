#!/usr/bin/python3.5
from library import Librarian
from collector import RandomCollector
import requests
from temporalCaseManager import ICHypothesis, TemporalCaseManager
from truthTable import TruthTable
from branch import Branch
from iterModel import IterModel

collector = RandomCollector()
iterModel = IterModel(collector = collector,
    resetRoute="http://buttonlight02.env:5001/resetall",
    infoRoutes=["http://buttonlight02.env:5001/checklight"],
    actionRoutes=["http://buttonlight02.env:5001/pushbutton"])

for i in range(100):
    iterModel.examine()

for i in range(1000):
    iterModel.consider()

print(iterModel)
