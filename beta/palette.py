import copy

class Palette():
    def __init__(self, iats, aats, isFoundation = True, cases = None, rCases = None, hyps = None):
        self.cases = []
        self.rCases = []
        if isFoundation:
            if hyps == None:
                raise ValueError("Must provide hyps if Palette is foundational")
            #create cases based on hyps and initial ats given
            #(will need to pull the correct infos)
        else:
            if cases == None or rCases == None:
                raise ValueError("Must provide both cases and rCases if Palette is non-foundational")
            #assign cases which were calculated by the prior palette
            self.cases = cases
            self.rCases = rCases
        self.iats = iats #list of single timestep attributes ordered by their original placement in the environment
        self.aats = aats
    def genNext_predict(aats): #TODO: test this function NOTE: this function is ONLY used in a prediction use case.
        cases = []
        iats = []
        for case in self.cases:
            cases.append(case.genNext())
            iats.append(case.genIat())
        rCases = []
        for rCase in self.rCases:
            rCases.append(rCase.genNext())
        return Palette(iats, aats, cases, rCases)
    def genNext(iats, aats):
        cases = []
        for case in self.cases:
            cases.append(case.genNext())
        rCases = []
        for rCase in self.rCases:
            rCases.append(rCase.genNext())
        return Palette(iats, aats, cases, rCases)
    def copy():
        copy.deepcopy(self)
