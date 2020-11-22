import json 
import pygame
from pygame import sprite



class PowerUp(pygame.sprite.Sprite):
    def __init__(self,PowerUP_ID,PowerUpCategory,UsageTime,Image):
        pygame.sprite.Sprite.__init__(self)
        self.PowerUP_ID = PowerUP_ID
        self.PowerUpCategory = PowerUpCategory
        self.UsageTime = UsageTime
        self.Image = Image
        

    @classmethod
    def from_json(cls,json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<Power Up {self.PowerUpCategory}>'


power_ups_list = []
file_path = 'JsonResources/powerUps.json'
with open(file_path,'r') as json_file:
    data = json.loads(json_file.read())
    for p in data:
        power_ups_list.append(PowerUp(**p))

print(power_ups_list)




