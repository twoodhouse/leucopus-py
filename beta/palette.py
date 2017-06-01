import copy
from case import Case

class Palette(): #TODO: next, review this whole class thoroughly. Finish any missing portions
    def __init__(self, iats, aats, isFoundation = True, rats = None, cases = None, rCases = None, hyps = None):
        self.cases = []
        self.rCases = []
        self.iats = iats #list of single timestep attributes ordered by their original placement in the environment
        self.aats = aats
        self.rats = []
        self.nextPalette = None
        self.copiedFrom = None
        self.hyps = hyps
        self.attemptCounter = None
        self.scores = None
        if isFoundation:
            if len(hyps) != len(iats):
                raise ValueError("Length of hyps does not match length of iats")
            if hyps == None:
                raise ValueError("Must provide hyps if Palette is foundational")
            #create cases based on hyps and initial ats given
            #(will need to pull the correct infos)
            self.attemptCounter = []
            for hyp in hyps:
                self.attemptCounter.append(0)
                self.addCaseAndRatFromHyp(hyp)
        else:
            if cases == None or rCases == None:
                raise ValueError("Must provide both cases and rCases if Palette is non-foundational")
            if rats == None:
                raise ValueError("Must provide rats if non-foundational")
            #assign cases which were calculated by the prior palette
            self.rats = rats
            self.cases = cases
            self.rCases = rCases #NOTE: remember, rCases must always be pre-trained.
    def addCaseAndRatFromHyp(self, hyp, isRHyp = False): #This function will also create necessary reuse cases
        caseIats, caseAats = self.getAttributesForHypFromPalette(hyp, self)
        caseRats = []
        caseRCases = []
        for rHyp in hyp.rHyps:
            rCase = self.addCaseAndRatFromHyp(rHyp, isRHyp = True)
            caseRCases.append(rCase)
            caseRats.append(rHyp.iniRat)
        #Create new case, then append to the correct list
        newCase = Case(hyp, caseIats, caseAats, hyp.iniTats, caseRats, hyp.rHypLocations, caseRCases)
        if isRHyp:
            self.rats.append(newCase.hyp.iniRat)
            self.rCases.append(newCase)
        else:
            self.cases.append(newCase)
        return newCase
    def genNext(self, iats = None, aats = None):
        if aats == None:
            raise ValueError("Must input aats")
        cases = []
        predictionIats = []
        rCases = []
        rats = []
        if iats == None:
            for case in self.cases:
                predictionIats.append(case.genIat())
            iatsToUse = predictionIats
        else:
            iatsToUse = iats
        self.nextPalette = Palette(iats = iatsToUse, aats = aats, isFoundation = False, rats = rats, cases = cases, rCases = rCases)
        for rCase in self.rCases:
            caseIats, caseAats = self.getAttributesForHypFromPalette(rCase.hyp, self.nextPalette)
            rCases.append(rCase.genNext(nextIats = caseIats, nextAats = caseAats))
            rats.append(rCase.genIat())
        for case in self.cases:
            caseIats, caseAats = self.getAttributesForHypFromPalette(case.hyp, self.nextPalette)
            cases.append(case.genNext(nextIats = caseIats, nextAats = caseAats))
            # if iats == None:
            #     predictionIats.append(case.genIat())
        return self.nextPalette
    def getAttributesForHypFromPalette(self, hyp, palette):
        caseIats = []
        for index in hyp.infoIndeces:
            caseIats.append(palette.iats[index])
        caseAats = []
        for index in hyp.actionIndeces:
            caseAats.append(palette.aats[index-len(palette.iats)])
        return caseIats, caseAats
    def trainHypsUsingDownstreamAts(self):
        scores = []
        for caseIndex, case in enumerate(self.cases):
            attributes, classes = self.retrieveAttributesAndClasses(case, caseIndex)
            scores.append(case.hyp.fitAndScoreClf(attributes, classes))
        self.scores = scores
        return scores
    def trainDifferentHyp(self, modHyp, index): #TODO: test this function
        if self.hyps == None:
            raise ValueError("Can't train a new hyp unless this is listed as a foundationPalette (hyps != None)")
        #Get all actions / infos which were input
        subsequentIats = []
        subsequentAats = []
        palette = self.nextPalette
        while palette != None:
            subsequentIats.append(palette.iats)
            subsequentAats.append(palette.aats)
            palette = palette.nextPalette
        #Clear out all palettes/cases - they will be regenerated
        self.nextPalette = None
        self.cases = []
        self.rCases = []
        self.rats = []
        #Build current rats, rCases, and cases
        self.hyps[index] = modHyp
        for hyp in self.hyps:
            self.addCaseAndRatFromHyp(hyp)
        #Generate subsequent palette using actions/infos gained at the beginning
        palette = self
        for i in range(len(subsequentIats)):
            palette = palette.genNext(iats = subsequentIats[i], aats = subsequentAats[i])
        return self.trainHypsUsingDownstreamAts()
    def retrieveAttributesAndClasses(self, case, caseIndex):
        attributes = []
        classes = []
        currentPalette = self
        currentCase = case
        while not currentPalette.nextPalette == None:
            attributes.append(currentCase.genFullAttributes())
            classes.append(currentPalette.nextPalette.iats[caseIndex])
            currentCase = currentCase.nextCase
            currentPalette = currentPalette.nextPalette
        return attributes, classes
    def copy(self):
        cpy = copy.deepcopy(self)
        cpy.copiedFrom = self
        return cpy
    def __str__(self):
        st = "**************************************************Palette**************************************************\n"
        st += "Cases\n"
        for case in self.cases:
            st += str(case) + "\n"
        st += "RCases\n"
        for rCase in self.rCases:
            st += str(rCase) + "\n"
        st += "Iats: " + str(self.iats) + "\n"
        st += "Aats: " + str(self.aats) + "\n"
        st += "Rats: " + str(self.rats) + "\n"
        return st
    def infoPrint(self):
        print(self.iats, self.aats, self.rats)
    def infoPrintAll(self):
        palette = self
        while palette != None:
            palette.infoPrint()
            palette = palette.nextPalette
    def infoPrintCase(self, index):
        palette = self
        while palette != None:
            palette.cases[index].infoPrint()
            palette = palette.nextPalette
    def infoPrintAttClasses(self, index):
        case = self.cases[index]
        attributes, classes = self.retrieveAttributesAndClasses(case, index)
        for index, attribute in enumerate(attributes):
            print(attribute, classes[index])

    # def genNext_predict(self, aats): #NOTE: this function is ONLY used in a prediction use case.
    #     cases = []
    #     iats = []
    #     for case in self.cases:
    #         caseIats, caseAats = self.getAttributesForHyp(case.hyp)
    #         cases.append(case.genNext(nextIats = caseIats, nextAats = caseAats))
    #         iats.append(case.genIat())
    #     rCases = []
    #     rats = []
    #     for rCase in self.rCases:
    #         caseIats, caseAats = self.getAttributesForHyp(rCase.hyp)
    #         rCases.append(rCase.genNext(nextIats = caseIats, nextAats = caseAats))
    #         rats.append(rCase.genIat())
    #     return Palette(iats = iats, aats = aats, isFoundation = False, rats = rats, cases = cases, rCases = rCases)
