uidCounter = 0

class Node():
    def __init__(self):
        global uidCounter
        self.uid = uidCounter
        uidCounter = uidCounter + 1
        self.sinkNodes = []
        self.completedTimeVal = None
        self.proceedingComplete = False
    def setSinkNode(self, sinkNode):
        self.sinkNodes.append(sinkNode)

class Input(Node):
    def __init__(self):
        super().__init__()
    def activate(self, timeVal, signalState):
        self.storedAttribute = signalState
        sendSignalToAllSinkNodes(signalState, timeVal, self.sinkNodes)
        self.completedTimeVal = timeVal
    def proceed(self, timeVal):
        for sinkNode in self.sinkNodes:
            sinkNode.proceed(timeVal)

class Stroke(Node):
    def __init__(self, iniStoredAttribute):
        super().__init__()
        self.storedAttribute = iniStoredAttribute
        self.sourceNodes = []
        self.numReceived = 0
        self.trueReceived = 0
    def addSourceNode(self, sourceNode): #allows for bi-directional linked list
        sourceNode.setSinkNode(self)
        self.sourceNodes.append(sourceNode)
    def activate(self, timeVal, signalState):
        self.proceedingComplete = False
        if len(self.sourceNodes) != 2:
            raise ValueError("Must set sourceNodes before activation")
        if signalState:
            self.trueReceived = self.trueReceived + 1
        self.numReceived = self.numReceived + 1
        if self.numReceived == 2:
            if self.trueReceived == 0 or self.trueReceived == 1:
                sendSignalToAllSinkNodes(True, timeVal, self.sinkNodes)
                self.storedAttribute = True
            elif self.trueReceived == 2:
                sendSignalToAllSinkNodes(False, timeVal, self.sinkNodes)
                self.storedAttribute = False
            self.completedTimeVal = timeVal
            self.numReceived = 0
            self.trueReceived = 0
    def proceed(self, timeVal): #return value indicates whether function needs run again
        if not self.proceedingComplete:
            if timeVal != self.completedTimeVal: #current node lacks an input
                signalStates = []
                #find source(s) which did not activate
                for sourceNode in self.sourceNodes:
                    if sourceNode.completedTimeVal != timeVal:
                        signalStates.append(sourceNode.storedAttribute)
                #activate self on behalf of source
                for signalState in signalStates:
                    self.activate(timeVal, signalState)
            #continute proceeding for all sink nodes.
            self.proceedingComplete = True
            for sinkNode in self.sinkNodes:
                result = sinkNode.proceed(timeVal)
        # if not self.proceedingComplete:
        #     self.proceedingComplete = True
        #     if timeVal != self.completedTimeVal:
        #         signalStates = []
        #         #find source(s) which did not activate
        #         for sourceNode in self.sourceNodes:
        #             if sourceNode.completedTimeVal != timeVal:
        #                 signalStates.append(sourceNode.storedAttribute)
        #         #activate self on behalf of source
        #         for signalState in signalStates:
        #             self.activate(timeVal, signalState)
        #         return True
        #     else :
        #         #continute proceeding for other nodes. (ONLY if no conflicts in the current)
        #         trueResultFlag = False
        #         for sinkNode in self.sinkNodes:
        #             result = sinkNode.proceed(timeVal)
        #             if result:
        #                 trueResultFlag = True
        #         return trueResultFlag

def sendSignalToAllSinkNodes(signalState, timeVal, sinkNodes):
    for sinkNode in sinkNodes:
        sinkNode.activate(timeVal, signalState)

class Logger(Node):
    def __init__(self):
        super().__init__()
        self.timeSeries = []
        self.sourceNodes = []
    def setSourceNode(self, sourceNode): #allows for bi-directional linked list
        self.sourceNode = sourceNode
        sourceNode.setSinkNode(self)
    def activate(self, timeVal, signalState):
        if signalState:
            self.timeSeries.append(1)
        else:
            self.timeSeries.append(0)
    def proceed(self, timeVal):
        pass
