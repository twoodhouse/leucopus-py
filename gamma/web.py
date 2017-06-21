from node import Input, Stroke, Logger
import random

class Web():
    def __init__(self, numInputs, size):
        self.inputs = []
        self.strokes = []
        self.loggers = []
        unfinishedStrokes = []
        for i in range(numInputs):
            self.inputs.append(Input())
            logger = Logger()
            logger.setSourceNode(self.inputs[i])
            self.loggers.append(logger)
        for i in range(size):
            newStroke = Stroke(bool(random.getrandbits(1)))
            if random.uniform(0,1) > .8:
                choice = random.choice(self.inputs + self.strokes)
                newStroke.addSourceNode(choice)
                unfinishedStrokes.append(newStroke)
            else:
                choice1 = random.choice(self.inputs + self.strokes)
                newStroke.addSourceNode(choice1)
                choice2 = random.choice(self.inputs + self.strokes)
                newStroke.addSourceNode(choice2)
            self.strokes.append(newStroke)
            logger = Logger()
            logger.setSourceNode(self.strokes[i])
            self.loggers.append(logger)
        for unfinishedStroke in unfinishedStrokes:
            choice = random.choice(self.inputs + self.strokes)
            unfinishedStroke.addSourceNode(choice)
        self.availableNodes = self.inputs + self.strokes
    # def linkSources_random(self):
    #     for stroke in self.strokes:
    #         choice1 = random.choice(self.availableNodes)
    #         choice2 = random.choice(self.availableNodes)
    #         stroke.setSourceNodes([choice1, choice2])
    def activateFrameSet(self, inputFrames):
        for timeVal, inputFrame in enumerate(inputFrames):
            for i, inpt in enumerate(self.inputs):
                inpt.activate(timeVal, inputFrame[i])
            for i, inpt in enumerate(self.inputs):
                inpt.proceed(timeVal)
    def getBestStrokeByInputIndex(self, inputIndex):
        baselineTimeSeries = self.loggers[inputIndex].timeSeries
        bestStroke = self.strokes[0]
        numSuccessOfBest = 0
        for stroke in self.strokes:
            strokeLogger = findLogger(stroke)
            strokeTimeSeries = strokeLogger.timeSeries
            successPoints = 0
            for i, e in enumerate(baselineTimeSeries):
                if i != 0 and strokeTimeSeries[i-1] == e:
                    successPoints = successPoints + 1
            if successPoints > numSuccessOfBest:
                bestStroke = stroke
                numSuccessOfBest = successPoints
        score = float(numSuccessOfBest)/float(len(baselineTimeSeries)-1)
        return stroke, score

def findLogger(node):
    for sinkNode in node.sinkNodes:
        if isinstance(sinkNode, Logger):
            return sinkNode
