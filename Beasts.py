import pygame
from Entities import Entity
from CSV import import_folder
from Settings import *


class Beasts(Entity):
    def __init__(self, posx, posy, group, name, obstacles):
        super().__init__(group)

        self.sprite_type = 'Beast'
        self.status = 'Left_Rest'

        self.left = pygame.image.load(f'Beasts/{name}/walk_left.png')
        self.right = pygame.image.load(f'Beasts/{name}/walk_right.png')
        self.up = pygame.image.load(f'Beasts/{name}/walk_up.png')
        self.down = pygame.image.load(f'Beasts/{name}/walk_down.png')

        self.right_walk = import_folder(f'Beasts/{name}/Right')
        self.current_right = 0

        self.left_walk = import_folder(f'Beasts/{name}/Left')
        self.current_left = 0

        self.down_walk = import_folder(f'Beasts/{name}/Down')
        self.current_down = 0

        self.up_walk = import_folder(f'Beasts/{name}/Up')
        self.current_up = 0

        # Up Attack
        self.up_attack = import_folder(f'Beasts/{name}/Up_attack')
        self.current_attack = 0

        # Down Attack
        self.down_attack = import_folder(f'Beasts/{name}/Down_attack')

        # Right Attack
        self.right_attack = import_folder(f'Beasts/{name}/Right_attack')

        # Left Attack
        self.left_attack = import_folder(f'Beasts/{name}/Left_attack')

        self.image = self.down
        if 'Left' in self.status:
            self.rect = self.image.get_rect(bottomright=(posx, posy))
        if 'Right' in self.status:
            self.rect = self.image.get_rect(topleft=(posx, posy))
        if 'Up' in self.status:
            self.rect = self.image.get_rect(bottomleft=(posx, posy))
        if 'Down' in self.status:
            self.rect = self.image.get_rect(topright=(posx, posy))
        self.hitbox = self.rect.inflate(0, -10)

        self.obstacles = obstacles
        self.name = name
        self.info = Beast_data[self.name]
        self.health = self.info['Health']
        self.attack = self.info['Attack']
        self.exp_drop = self.info['Exp_drop']
        self.knock_resistance = self.info['knock_resistance']
        self.range = self.info['Range']
        self.speed = self.info['Speed']
        self.notice_range = self.info['Notice_range']

        # Attack
        self.attack_ready = 'Ready'
        self.attack_time = 0
        self.attack_cooldown = self.info['Cooldown']

        self.vulnerable = True
        self.vulnerable_time = 0
        self.vulnerable_countdown = 300

    # Cycling Images
    def animations(self):
        if self.status == 'Right':
            self.current_right += self.cycle_speed

            if self.current_right >= len(self.right_walk):
                self.current_right = 0

            self.image = self.right_walk[int(self.current_right)]

        elif self.status == 'Left':
            self.current_left += self.cycle_speed

            if self.current_left >= len(self.left_walk):
                self.current_left = 0

            self.image = self.left_walk[int(self.current_left)]

        elif self.status == 'Down':
            self.current_down += self.cycle_speed

            if self.current_down >= len(self.down_walk):
                self.current_down = 0

            self.image = self.down_walk[int(self.current_down)]

        elif self.status == 'Up':
            self.current_up += self.cycle_speed

            if self.current_up >= len(self.up_walk):
                self.current_up = 0

            self.image = self.up_walk[int(self.current_up)]

        if self.status == 'Up_attack':
            self.current_attack += 0.22

            if self.current_attack >= len(self.up_attack):
                self.current_attack = 0
                if 'attack' in self.status:
                    self.attack_ready = 'Attacking'

            self.image = self.up_attack[int(self.current_attack)]

        if self.status == 'Down_attack':
            self.current_attack += 0.22

            if self.current_attack >= len(self.down_attack):
                self.current_attack = 0
                if 'attack' in self.status:
                    self.attack_ready = 'Attacking'

            self.image = self.down_attack[int(self.current_attack)]

        if self.status == 'Left_attack':
            self.current_attack += 0.22

            if self.current_attack >= len(self.left_attack):
                self.current_attack = 0
                if 'attack' in self.status:
                    self.attack_ready = 'Attacking'

            self.image = self.left_attack[int(self.current_attack)]

        if self.status == 'Right_attack':
            self.current_attack += 0.22

            if self.current_attack >= len(self.right_attack):
                self.current_attack = 0
                if 'attack' in self.status:
                    self.attack_ready = 'Attacking'

            self.image = self.right_attack[int(self.current_attack)]

        elif self.status == 'Right_Rest':
            self.image = self.right

        elif self.status == 'Left_Rest':
            self.image = self.left

        elif self.status == 'Up_Rest':
            self.image = self.up

        elif self.status == 'Down_Rest':
            self.image = self.down

    def movement_status(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        separation = (player_vector - enemy_vector).magnitude()

        if self.attack_ready == 'Attacking':
            self.direction = pygame.math.Vector2()

        if separation > 0:
            direction = (player_vector - enemy_vector).normalize()
            x_separation = abs(direction[0])
            y_separation = abs(direction[1])

        else:
            direction = pygame.math.Vector2((0, 0))
            x_separation = 0
            y_separation = 0

        # Move
        if separation <= self.range and self.attack_ready == 'Ready':
            self.attack_time = pygame.time.get_ticks()
            if 'attack' not in self.status:
                self.status = self.status + '_attack'

        elif separation <= self.notice_range:
            self.direction = direction
            if x_separation > y_separation:
                if self.direction.x > 0:
                    self.status = 'Right'
                else:
                    self.status = 'Left'
            else:
                if self.direction.y > 0:
                    self.status = 'Down'
                else:
                    self.status = 'Up'

        else:
            self.direction = pygame.math.Vector2()
            if 'Rest' not in self.status and 'Attack' not in self.status:
                self.status = self.status + '_Rest'

    def damage_dealt(self, attack_sprite, player):
        if self.vulnerable:
            if attack_sprite.sprite_type == 'Weapons':
                player_damage = player.playerstats['Attack']
                weapon_damage = Weapon_choice[player.weapon]['damage']
                self.health -= player_damage + weapon_damage

            self.vulnerable_time = pygame.time.get_ticks()
            self.vulnerable = False

    def kill_beast(self):
        if self.health <= 0:
            self.kill()

    def cooldown(self):
        if self.attack_ready == 'Attacking':
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attack_ready = 'Ready'

        if not self.vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.vulnerable_time >= self.vulnerable_countdown:
                self.vulnerable = True

    def knockback(self):
        if self.vulnerable:
            self.direction *= -self.knock_resistance

    # Only the beasts sprites require the player data, so another function
    def update_beasts(self, player):
        self.movement_status(player)

    def update(self):
        self.move(self.speed)
        self.animations()
        self.cooldown()
        self.kill_beast()
        self.knockback()
