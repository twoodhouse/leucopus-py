import copy
from case import Case

class Palette(): #TODO: next, review this whole class thoroughly. Finish any missing portions
    def __init__(self, iats, aats, isFoundation = True, rats = None, cases = None, rCases = None, hyps = None):
        self.cases = []
        self.rCases = []
        self.iats = iats #list of single timestep attributes ordered by their original placement in the environment
        self.aats = aats
        self.rats = []
        if isFoundation:
            if len(hyps) != len(iats):
                raise ValueError("Length of hyps does not match length of iats")
            if hyps == None:
                raise ValueError("Must provide hyps if Palette is foundational")
            #create cases based on hyps and initial ats given
            #(will need to pull the correct infos)
            for hyp in hyps:
                self.addCaseAndRatFromHyp(hyp)
        else:
            if cases == None or rCases == None:
                raise ValueError("Must provide both cases and rCases if Palette is non-foundational")
            if rats == None:
                raise ValueError("Must provide rats if non-foundational")
            #assign cases which were calculated by the prior palette
            self.rats = rats
            self.cases = cases
            self.rCases = rCases
    def addCaseAndRatFromHyp(self, hyp, isRHyp = False): #This function will also create necessary reuse cases
        caseIats, caseAats = self.getAttributesForHyp(hyp)
        caseRats = []
        caseRCases = []
        for rHyp in hyp.rHyps:
            rCase = self.addCaseFromHyp(self, rHyp, isRHyp = True)
            caseRCases.append(rCase)
            caseRats.append(rHyp.iniRat)
        #Create new case, then append to the correct list
        newCase = Case(hyp, caseIats, caseAats, hyp.iniTats, caseRats, hyp.rHypLocations, caseRCases)
        if not isRHyp:
            self.cases.append(newCase)
        else:
            self.rats.append(newCase.hyp.iniRat)
            self.rCases.append(newCase)
        return newCase
    def genNext(self, iats = None, aats = None):
        if aats == None:
            raise ValueError("Must input aats")
        cases = []
        predictionIats = []
        for case in self.cases:
            caseIats, caseAats = self.getAttributesForHyp(case.hyp)
            cases.append(case.genNext(nextIats = caseIats, nextAats = caseAats))
            if iats == None:
                predictionIats.append(case.genIat())
        rCases = []
        rats = []
        for rCase in self.rCases:
            caseIats, caseAats = self.getAttributesForHyp(rCase.hyp)
            rCases.append(rCase.genNext(nextIats = caseIats, nextAats = caseAats))
            rats.append(rCase.genIat())
        if iats == None:
            iatsToUse = predictionIats
        else:
            iatsToUse = iats
        return Palette(iats = iatsToUse, aats = aats, isFoundation = False, rats = rats, cases = cases, rCases = rCases)
    def getAttributesForHyp(self, hyp):
        caseIats = []
        for index in hyp.infoIndeces:
            caseIats.append(self.iats[index])
        caseAats = []
        for index in hyp.actionIndeces:
            caseAats.append(self.aats[index-len(self.iats)])
        return caseIats, caseAats
    def trainHyps(self):
        pass #TODO: this is next
    def copy(self):
        copy.deepcopy(self)
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
