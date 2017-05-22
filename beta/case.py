import copy

# Case represents a SINGLE time step generator of a SINGLE Palette iat
# genNext(aat) generates the next Case within this Palette iat
# genIat()
class Case():
    def __init__(self, hyp, iats, aats, tats, rats, ratLocations, rCases = []):
        if len(rats) != len(ratLocations):
            raise ValueError("length of reuse attributes (" + str(len(rats)) + ") does not match length of reuse attribute locations (" + str(len(ratLocations)) + ")")
        if len(rats) != len(rCases):
            raise ValueError("length of reuse attributes (" + str(len(rats)) + ") does not match length of reuse Cases (" + str(len(rCases)) + ")")
        #NOTE: for high performance, these next checks should be removed
        priorLocation = -1
        for ratLocation in ratLocations:
            if priorLocation >= ratLocation:
                raise ValueError("ratLocations are not in increasing order (no repetition allowed): " + str(ratLocations))
            priorLocation = ratLocation
            if ratLocation < 0:
                raise ValueError("ratLocation cannot be less than index 0")
            if ratLocation > len(iats)+len(aats)+len(rats):
                raise ValueError("ratLocation ("+str(ratLocation)+")is greater than max value ("+str(len(iats)+len(aats)+len(rats))+")")
        self.rCases = rCases
        self.hyp = hyp
        # common attributes
        self.iats = iats #Info Attributes
        self.aats = aats #ActionAttributes
        # derived attributes
        self.rats = rats #Reuse Attributes
        self.nextCase = None
        self.ratLocations = ratLocations #location to place reuse attributes
        if tats == None:
            self.tats = hyp.iniTats #Table Attributes
        else:
            self.tats = tats #Table Attributes
    def getInfoIndeces(self):
        return self.hyp.infoIndeces
    def getActionIndeces(self):
        return self.hyp.actionIndeces
    def genIat(self):
        inputs = self.genFullAttributes() #NOTE: may increase efficiency by storing this result
        return self.hyp.predictFromClf(inputs)
    def genNext(self, nextIats, nextAats):
        rats = []
        for rCase in self.rCases:
            rats.append(rCase.genIat())
        tats = []
        inputs = self.genFullAttributes() #NOTE: may increase efficiency by storing this result
        for tt in self.hyp.tts:
            tats.append(tt.retrieve(inputs))
        self.nextCase = Case(self.hyp, nextIats, nextAats, tats, rats, self.ratLocations, rCases = self.rCases)
        return self.nextCase
    def genFullAttributes(self):
        ats = []
        appendCounter = 0
        ratCounter = 0
        for iat in self.iats:
            while ratCounter < len(self.ratLocations) and appendCounter == self.ratLocations[ratCounter]:
                ats.append(self.rats[ratCounter])
                ratCounter = ratCounter + 1
                appendCounter = appendCounter + 1
            ats.append(iat)
            appendCounter = appendCounter + 1
        for aat in self.aats:
            while ratCounter < len(self.ratLocations) and appendCounter == self.ratLocations[ratCounter]:
                ats.append(self.rats[ratCounter])
                ratCounter = ratCounter + 1
                appendCounter = appendCounter + 1
            ats.append(aat)
            appendCounter = appendCounter + 1
        while ratCounter < len(self.ratLocations) and appendCounter == self.ratLocations[ratCounter]:
            ats.append(self.rats[ratCounter])
            ratCounter = ratCounter + 1
            appendCounter = appendCounter + 1
        for tat in self.tats:
            ats.append(tat)
        return ats
    def copy(self):
        return copy.deepcopy(self)
