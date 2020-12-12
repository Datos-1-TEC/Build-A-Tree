
#Esta clase es una réplica del jugador en java
class PlayerSocket(object):
    def __init__(self, ID, score = 0, treeList = []):
        super().__init__()
        self.ID = ID
        self.lives = 3
        self.score = score
        self.treeList = treeList
    
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

    def setLives(self, lives):
        self.lives = lives

    def setScore(self, score):
        self.score = score

    def setTreeList(self, treeList):
        self.treeList = treeList 


