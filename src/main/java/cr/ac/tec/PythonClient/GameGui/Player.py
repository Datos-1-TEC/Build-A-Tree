
#Esta clase es una réplica del jugador en java
class Player(object):
    def __init__(self, ID):
        super().__init__()
        self.ID = ID
        self.lives = 3
        self.score = 0
        self.accumulatedScore = 0
        self.treeList = []
    
    def getID(self):
        return self.ID

    def getLives(self):
        return self.lives
    
    def getCurrentToken(self):
        return self.currentToken

    def getScore(self):
        return self.score
    
    def getTreeList(self):
        return self.treeList

    def getAcumulatedScore(self):
        return self.accumulatedScore

    def setLives(self, lives):
        self.lives = lives

    def setScore(self, score):
        self.score = score

    def setTreeList(self, treeList):
        self.treeList = treeList 
    
    def setAcummulatedScore(self, accumulatedScore):
        self.accumulatedScore = accumulatedScore


