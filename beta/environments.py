
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
        self.reset()
    def reset(self):
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
        self.reset()
    def reset(self):
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
        self.reset()
    def reset(self):
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

class TwoTempButtonFourTempButton(Environment):
    def __init__(self):
        super().__init__([self.checkLight1, self.checkLight2], [self.pressButton1, self.pressButton2])
        self.reset()
    def reset(self):
        self.button1PressCount = 0
        self.button2PressCount = 0
        self.currentLight1Status = False
        self.currentLight2Status = False
    def timestep(self):
        self.currentLight1Status = False
        self.currentLight2Status = False
    def pressButton1(self):
        self.button1PressCount += 1
        if self.button1PressCount == 2:
            self.currentLight1Status = True
            self.button1PressCount = 0
    def checkLight1(self):
        return self.currentLight1Status
    def pressButton2(self):
        self.button2PressCount += 1
        if self.button2PressCount == 2:
            self.currentLight2Status = True
            self.button2PressCount = 0
    def checkLight2(self):
        return self.currentLight2Status
