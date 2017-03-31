class Case():
    def __init__(self, attributes, clss):
        self.attributes = attributes
        self.clss = clss
    def __str__(self):
        attributeStr = ''
        for attribute in self.attributes:
            attributeStr = attributeStr + str(attribute)+ ", "
        return "Case({"+str(self.clss)+"} ["+attributeStr + "])"

class ICase():
    def __init__(self, case, depth, iAttributes):
        if depth != len(iAttributes):
            raise ValueError("depth does not match number of iAttributes")
        self.fullAttributes = case.attributes + iAttributes
        self.clss = case.clss
        self.depth = depth
        self.case = case
    def __str__(self):
        attributeStr = ''
        for attribute in self.fullAttributes:
            attributeStr = attributeStr + str(attribute)+ ", "
        return "ICase(d" + str(self.depth) + " {"+str(self.clss)+"} ["+attributeStr + "])"
