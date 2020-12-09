import sys
sys.path.append("..")
import json
from collections import namedtuple
from json import JSONEncoder
from types import SimpleNamespace

class Token():
    def __init__(self, val, shape, points):
        super().__init__()
        self.val = val
        self.shape = shape
        self.points = points

    def getVal(self):
        return self.val
    
    def getShape(self):
        return self.shape

    def getPoints(self):
        return self.points  

    def getPoints(self):
        return self.points
 





