import sys
sys.path.append("..")
import json
from collections import namedtuple
from json import JSONEncoder
from Player import*
from types import SimpleNamespace

class Token():
    def __init__(self, val, shape):
        super().__init__()
        self.val = val
        self.shape = shape
        self.points = 0

    def getVal(self):
        return self.val
    
    def getShape(self):
        return self.shape

    def getPoints(self):
        return self.points  

    def setPoints(self, points):
        self.points = points




