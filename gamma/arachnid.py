from web import Web

class Arachnid():
    def __init__(self, env, dm):
        self.webs = []
        self.env = env
        self.dm = dm
        self.inputFrames = []
    def getFrames(self, number):
        for i in range(number):
            actionSet = self.dm.getActionSet()
            newIats, newAats = self.env.runFrame(actionSet)
            allInputs = newIats + newAats
            self.inputFrames.append(allInputs)
    def spinRandomWeb(self, size):
        newWeb = Web(len(self.inputFrames[0]), size)
        # newWeb.linkSources_random()
        newWeb.activateFrameSet(self.inputFrames)
        self.webs.append(newWeb)
        # for logger in newWeb.loggers:
        #     print(logger.timeSeries)
        return newWeb.getBestStrokeByInputIndex(1)
