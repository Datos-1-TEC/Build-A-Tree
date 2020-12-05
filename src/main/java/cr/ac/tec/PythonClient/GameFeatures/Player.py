class Player():
    def __init__(self, ID, currentToken = null, score = 0, treeList = []):
        super().__init__()
        self.ID = ID
        self.lives = 3
        self.currentToken = currentToken
        self.score = score
        self.treeList = treeList
        self.currentPowerUp = currentPowerUp
    
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
    
    def getCurrentPowerUp (self):
        return self.currentPowerUp

    def setLives(self, lives):
        self.lives = lives

    def setCurrentToken(self, currentToken):
        self.currentToken = currentToken

    def setScore(self, score):
        self.score = score

    def setTreeList(self, treeList):
        self.treeList = treeList 

    def setCurrentPowerUp (self, currentPowerUp):
        self.currentPowerUp = currentPowerUp   