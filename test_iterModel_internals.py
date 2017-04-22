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

ENV_NAME = '2_4Toggle'

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

for i in range(300):
    iterModel.consider()
for i in range(50):
    iterModel.considerReuse(1)

# iterModel.librarian.printFullCases()
print(iterModel)
