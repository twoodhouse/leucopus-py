
class Environment():
    def __init__(self, infoMethods, actionMethods):
        self.infoMethods = infoMethods
        self.actionMethods = actionMethods
    def runFrame(self, actionVals):
        infoVals = []
        for infoMethod in self.infoMethods:
            boolResult = infoMethod()
            if boolResult:
                infoVals.append(1)
            else:
                infoVals.append(0)
        self.timestep() #is timestep in the correct portion of this order?
        for index, actionMethod in enumerate(self.actionMethods):
            if actionVals[index] == 1:
                actionMethod()
        return infoVals, actionVals

class TempButton(Environment):
    def __init__(self):
        super().__init__([self.checkLight], [self.pressButton])
        self.buttonJustPressed = False
    def timestep(self):
        self.buttonJustPressed = False
    def pressButton(self):
        self.buttonJustPressed = True
    def checkLight(self):
        return self.buttonJustPressed

class ToggleButton(Environment):
    def __init__(self):
        super().__init__([self.checkLight], [self.pressButton])
        self.currentLightStatus = False
    def timestep(self):
        pass
    def pressButton(self):
        self.currentLightStatus = not self.currentLightStatus
    def checkLight(self):
        return self.currentLightStatus

class TwoTempButton(Environment):
    def __init__(self):
        super().__init__([self.checkLight], [self.pressButton])
        self.buttonPressedOnce = False
        self.currentLightStatus = False
    def timestep(self):
        self.currentLightStatus = False
    def pressButton(self):
        if self.buttonPressedOnce:
            self.currentLightStatus = True
            self.buttonPressedOnce = False
        else:
            self.buttonPressedOnce = True
    def checkLight(self):
        return self.currentLightStatus
