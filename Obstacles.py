import pygame
from Settings import *


# Creating Obstacles class
class Obstacles(pygame.sprite.Sprite):
    def __init__(self, posx, posy, group, item_type, surface=pygame.Surface((obstacles_size, obstacles_size))):
        super().__init__(group)

        self.sprite_type = item_type
        self.image = surface
        if self.sprite_type == 'border_128':
            self.rect = self.image.get_rect(topright=(posx, posy - obstacles_size))
        if self.sprite_type == 'objects':
            self.rect = self.image.get_rect(topleft=(posx, posy - obstacles_size))
        else:
            self.rect = self.image.get_rect(topleft=(posx, posy))
        self.hitbox = self.rect.inflate(0, -10)
