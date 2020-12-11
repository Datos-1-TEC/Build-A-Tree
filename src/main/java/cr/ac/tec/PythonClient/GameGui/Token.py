import sys
sys.path.append("..")
import json
from collections import namedtuple
from json import JSONEncoder
from types import SimpleNamespace

class Token():
    """********************************************************************************************
                            Instituto Tecnologico de Costa Rica
                                    Ing. en computadores
    @method __init__(): se encarga de establecer los valores, tamanos y puntos, cada uno de estos tiene su getter y setter.


    ********************************************************************************************"""
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
 





