import pygame
from Settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.direction = pygame.math.Vector2()

        self.cycle_speed = 0.22

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprites in self.obstacles:
                if sprites.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprites.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprites.hitbox.right

        if direction == 'vertical':
            for sprites in self.obstacles:
                if sprites.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprites.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprites.hitbox.bottom


