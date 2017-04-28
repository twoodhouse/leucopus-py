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
from truthTable import TruthTable

ENV_NAME = '2Temp4Temp'

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

for i in range(80):
    iterModel.examine()

iterModel.tryExplanation("http://env.h:5002/checklight1",
    ["http://env.h:5002/checklight1"],
    ["http://env.h:5002/pushbutton1"],
    [TruthTable([0,1,1,0,0,1,1,0])],
    [0])
#
rh1 = iterModel.rhManager.newReuseHypothesis(iterModel.tcmDict["http://env.h:5002/checklight1"].bestHypothesis, 0)
rh1.infoRoutes = ["http://env.h:5002/checklight2"]
rh1.actionRoutes = ["http://env.h:5002/pushbutton2"]
iterModel.tryReuseExplanation("http://env.h:5002/checklight2",
    ["http://env.h:5002/checklight2", rh1],
    [],
    [TruthTable([0,1,1,0,0,1,1,0])],
    [0])
iterModel.tryReuseExplanation("http://env.h:5002/checklight2",
    ["http://env.h:5002/checklight2", rh1],
    [],
    [TruthTable([0,1,1,0,0,1,1,0])],
    [1])

for i in range(0):
    iterModel.consider()
print("!!!!!!!!!!!!!!!!!")
for i in range(0):
    iterModel.considerReuse(1)

# iterModel.librarian.printFullCases()
print(str(iterModel))

input("Press Enter to continue...")

iterModel.librarian.printFullCases()

print("****************")

hypotheses = []
for infoRoute in chosenEnvInfo['infos']:
    hypotheses.append(iterModel.tcmDict[infoRoute].bestHypothesis)
    print(iterModel.tcmDict[infoRoute].bestHypothesis)
b1 = Branch(iterModel.librarian, [1, 1], hypotheses)
b2 = Branch(iterModel.librarian, [1, 1], branch = b1)
b3 = Branch(iterModel.librarian, [1, 1], branch = b2)
b4 = Branch(iterModel.librarian, [1, 1], branch = b3)
b5 = Branch(iterModel.librarian, [1, 1], branch = b4)
b6 = Branch(iterModel.librarian, [1, 1], branch = b5)
b7 = Branch(iterModel.librarian, [1, 1], branch = b6)
b8 = Branch(iterModel.librarian, [1, 1], branch = b7)
b9 = Branch(iterModel.librarian, [1, 1], branch = b8)
b10 = Branch(iterModel.librarian, [1, 1], branch = b9)
b11 = Branch(iterModel.librarian, [1, 1], branch = b10)
b12 = Branch(iterModel.librarian, [1, 1], branch = b11)
b13 = Branch(iterModel.librarian, [1, 1], branch = b12)
b14 = Branch(iterModel.librarian, [1, 1], branch = b13)
b15 = Branch(iterModel.librarian, [1, 1], branch = b14)
b16 = Branch(iterModel.librarian, [1, 1], branch = b15)
