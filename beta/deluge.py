from palette import Palette

class Deluge():
    def __init__(self, env, initialActions):
        self.env = env
        hyps = []
        for infoMethod in env.infoMethods:
            hyps.append(Hyp(infoIndeces = [0], actionIndeces = [], tts = [], iniTats = [], rHyps = [], rHypLocations = [], iniRat = 0))
        initialIats, initialAats = env.runFrame(initialActions)
        #TODO: add a function which allows a foundational palette to make the next palette foundational
        self.river = Palette(iats = initialIats, aats = initialAats, isFoundation = True, hyps = hyps)
        self.cascades = []
    def addCascadeFromRiver(self):
        cascade = self.river.clone()
        self.cascades.append(cascade)
