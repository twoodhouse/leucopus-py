#!/usr/bin/python3.5
from library import Librarian
from collector import RandomCollector
import requests
from temporalCaseManager import ICHypothesis, TemporalCaseManager
from truthTable import TruthTable
from branch import Branch
from iterModel import IterModel
import yaml
import threading
import time

ENV_NAME = '2Toggle'

f = open('environments.yaml')
enviromentsInfo = yaml.safe_load(f)
#set environment HERE
chosenEnvInfo = enviromentsInfo[ENV_NAME]

def startEnv():
    exec(open("./"+chosenEnvInfo['location']+".py").read())
t1 = threading.Thread(target=startEnv, args=[])
t1.start()
time.sleep(1)

collector = RandomCollector()
iterModel = IterModel(collector = collector,
    resetRoute=chosenEnvInfo['reset'],
    infoRoutes=chosenEnvInfo['infos'],
    actionRoutes=chosenEnvInfo['actions'])

for i in range(50):
    iterModel.examine()

for i in range(400):
    iterModel.consider()

print(iterModel)
# print("depth: " + str(iterModel.tcmDict[chosenEnvInfo['infos'][0]].depth))
# print("case attributes: " + str(len(iterModel.tcmDict[chosenEnvInfo['infos'][0]].cases[0].attributes)))
iterModel.librarian.printFullCases()
print("----")
b1 = Branch(iterModel.librarian, [1], hypotheses = [iterModel.tcmDict[chosenEnvInfo['infos'][0]].bestHypothesis])
b2 = Branch(iterModel.librarian, [1], branch = b1)
b3 = Branch(iterModel.librarian, [1], branch = b2)
b4 = Branch(iterModel.librarian, [1], branch = b3)
b5 = Branch(iterModel.librarian, [0], branch = b4)
b6 = Branch(iterModel.librarian, [0], branch = b5)
b7 = Branch(iterModel.librarian, [0], branch = b6)
b8 = Branch(iterModel.librarian, [1], branch = b7)
b9 = Branch(iterModel.librarian, [1], branch = b8)
b10 = Branch(iterModel.librarian, [1], branch = b9)
b11 = Branch(iterModel.librarian, [0], branch = b10)
b12 = Branch(iterModel.librarian, [0], branch = b11)
b13 = Branch(iterModel.librarian, [0], branch = b12)
b14 = Branch(iterModel.librarian, [1], branch = b13)
b15 = Branch(iterModel.librarian, [0], branch = b14)
b16 = Branch(iterModel.librarian, [1], branch = b15)
