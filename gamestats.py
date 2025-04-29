class Gamestats():
    def __init__(self): #where the different types of points are kept track of
        self.unc_points = 0
        self.sigma_points = 0
    def addPoint(self, type): 
        if type == 0:
            self.sigma_points += 1
        elif type == 1:
            self.unc_points += 1
    def isGameOver(self): #checked after each round to see if end condition is completed
        if self.sigma_points >= 15 or self.unc_points >= 5:
            return True
    def didPlayerWin(self): #called after isGameOver to either show win or lose screen
        if self.sigma_points >= 15:
            return True
        if self.unc_points >= 5:
            return False
        return False
