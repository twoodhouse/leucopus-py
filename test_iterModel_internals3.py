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
import random

# random.seed(1)

ENV_NAME = '2Temp4Temp8Temp'

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

iterModel.tryExplanation("http://env.i:5002/checklight1",
    [],
    ["http://env.i:5002/pushbutton1"],
    [TruthTable([0,1,1,0])],
    [0])

rh1 = iterModel.rhManager.newReuseHypothesis(iterModel.tcmDict["http://env.i:5002/checklight1"].bestHypothesis, 0)
rh1.infoRoutes = []
rh1.actionRoutes = ["http://env.i:5002/pushbutton2"]
iterModel.tryReuseExplanation("http://env.i:5002/checklight2",
    [rh1],
    [],
    [TruthTable([0,1,1,0])],
    [0])

# rhb2 = iterModel.rhManager.newReuseHypothesis(iterModel.tcmDict["http://env.i:5002/checklight2"].bestHypothesis, 0)
# rhb2.infoRoutes[0].actionRoutes = ["http://env.i:5002/pushbutton3"]
# rhb2.actionRoutes = []
# iterModel.tryReuseExplanation("http://env.i:5002/checklight3",
#     [rhb2],
#     [],
#     [TruthTable([0,1,1,0])],
#     [0])

for i in range(10):
    iterModel.consider()
print("!!!!!!!!!!!!!!!!!")
for i in range(0):
    iterModel.considerReuse(1)

# iterModel.librarian.printFullCases()
print(str(iterModel))

input("Press Enter to continue...")

iterModel.librarian.printFullCases()

print("****************")
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-17])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-16])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-15])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-14])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-13])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-12])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-11])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-10])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-9])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-8])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-7])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-6])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-5])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-4])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-3])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-2])
# print(iterModel.tcmDict[chosenEnvInfo['infos'][1]].bestHypothesis.icases[-1])
# print("****************")

hypotheses = []
for infoRoute in chosenEnvInfo['infos']:
    hypotheses.append(iterModel.tcmDict[infoRoute].bestHypothesis)
    # print(iterModel.tcmDict[infoRoute].bestHypothesis)
b1 = Branch(iterModel.librarian, hypotheses = hypotheses) #The actions on this first branch have no effect. Consider removing.
b2 = Branch(iterModel.librarian, actions = [0, 0, 1], branch = b1)
b3 = Branch(iterModel.librarian, actions = [0, 0, 1], branch = b2)
b4 = Branch(iterModel.librarian, actions = [0, 0, 1], branch = b3)
b5 = Branch(iterModel.librarian, actions = [0, 0, 1], branch = b4)
b6 = Branch(iterModel.librarian, actions = [0, 0, 1], branch = b5)
b7 = Branch(iterModel.librarian, actions = [1, 0, 1], branch = b6)
b8 = Branch(iterModel.librarian, actions = [1, 0, 1], branch = b7)
b9 = Branch(iterModel.librarian, actions = [1, 0, 1], branch = b8)
b10 = Branch(iterModel.librarian, actions = [1, 0, 1], branch = b9)
b11 = Branch(iterModel.librarian, actions = [1, 1, 1], branch = b10)
b12 = Branch(iterModel.librarian, actions = [1, 1, 1], branch = b11)
b13 = Branch(iterModel.librarian, actions = [1, 1, 1], branch = b12)
b14 = Branch(iterModel.librarian, actions = [1, 1, 1], branch = b13)
b15 = Branch(iterModel.librarian, actions = [1, 1, 1], branch = b14)
b16 = Branch(iterModel.librarian, actions = [1, 1, 1], branch = b15)
