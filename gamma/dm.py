from random import randint

class DM():
    def __init__(self, env):
        self.env = env
        self.deluge = None
    def setDeluge(self, deluge):
        self.deluge = deluge

class RandomDM(DM):
    def __init__(self, env):
        super().__init__(env)
    def getActionSet(self, isPrediction = False):
        actionSet = []
        for i in range(len(self.env.actionMethods)):
            actionSet.append(randint(0, 1))
        return actionSet
