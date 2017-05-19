from palette import Palette

class Deluge():
    def __init__(self, env):
        self.env = env
        self.river = Palette()
        self.cascades = []
    def addCascadeFromRiver(self):
        cascade = self.river.clone()
        self.cascades.append(cascade)
