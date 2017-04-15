import math

class TruthTable():
    def __init__(self, outputs):
        if math.log(len(outputs), 2)%1 != 0:
            raise ValueError("Invalid number of outputs")
        self.outputs = outputs
        self.numInputs = int(math.log(len(outputs), 2))
    def retrieve(self, inputs):
        if len(inputs) != int(math.log(len(self.outputs), 2)):
            raise ValueError("Length of inputs to truthTable does not match the necessary number for determining output")
        out = 0
        for bit in inputs:
            out = (out << 1) | bit
        return self.outputs[out]
    def copy(self):
        return TruthTable(self.outputs)
    def __str__(self):
        binaryStr = ""
        for output in self.outputs:
            binaryStr = binaryStr + str(output)
        return "TruthTable("+binaryStr+")"
