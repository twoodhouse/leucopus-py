from datetime import datetime

initialTime = None
needsEnd = False
descriptor = ""

open('timeLog', 'w').close()

def tStart(descriptorIn):
    global initialTime, needsEnd, descriptor
    descriptor = descriptorIn
    initialTime = datetime.now()
    if needsEnd == True:
        raise ValueError("need to end timer before starting another")
    needsEnd = True

def tEnd(descriptorIn):
    global initialTime, needsEnd, descriptor
    if descriptor != descriptorIn:
        raise ValueError("start and end descriptions do not match")
    needsEnd = False
    endTime = datetime.now()
    f = open('timeLog', 'a')
    f.write(str(endTime-initialTime)+" -- " + descriptor + "\n")
