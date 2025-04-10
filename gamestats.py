class Gamestats():
    def __init__(self):
        self.unc_points = 0
        self.sigma_points = 0
    def addPoint(self, type):
        if type == 0:
            self.sigma_points += 1
        elif type == 1:
            self.unc_points += 1
    def isGameOver(self):
        if self.sigma_points >= 15 or self.unc_points >= 5:
            return True
    def didPlayerWin(self):
        if self.sigma_points >= 15:
            return True
        if self.unc_points >= 5:
            return False
