import pygame
from Settings import *
from CSV import import_folder
from Entities import Entity


# Creating Player class
class Player(Entity):
    # Initialize
    def __init__(self, posx, posy, group, obstacles, weapon_draw, weapon_destroy, magic_draw):
        super().__init__(group)

        self.sprite_type = 'Protagonist'
        self.obstacles = obstacles
        self.status = 'down'

        # player at rest
        self.left = pygame.image.load('Player//characterwalkleft.png').convert_alpha()
        self.right = pygame.image.load('Player//characterwalkright.png').convert_alpha()
        self.up = pygame.image.load('Player//characterwalkup.png').convert_alpha()
        self.down = pygame.image.load('Player//characterwalkdown.png').convert_alpha()

        self.image = self.down
        self.rect = self.image.get_rect(topleft=(posx, posy))
        self.hitbox = self.rect.inflate(0, -26)

        # Right Walk
        self.right_walk = import_folder('Player/CharacterRight')
        self.current_right = 0

        # Left Walk
        self.left_walk = import_folder('Player/CharacterLeft')
        self.current_left = 0

        # Down Walk
        self.down_walk = import_folder('Player/CharacterDown')
        self.current_down = 0

        # Up Walk
        self.up_walk = import_folder('Player/CharacterUp')
        self.current_up = 0

        # Up Melee
        self.up_attack = import_folder('Player/UpAttack')
        self.current_attack = 0

        # Down Melee
        self.down_attack = import_folder('Player/DownAttack')

        # Right Melee
        self.right_attack = import_folder('Player/RightAttack')

        # Left Melee
        self.left_attack = import_folder('Player/LeftAttack')

        # Weapons
        self.weapon_draw = weapon_draw
        self.weapon_destroy = weapon_destroy
        self.weapon_number = 0
        self.weapon = list(Weapon_choice.keys())[self.weapon_number]

        # Attack
        self.attack = 'Ready'
        self.attack_cooldown = 60 + Weapon_choice[self.weapon]['cooldown']
        self.attack_time = 0

        # Magic
        self.magic_draw = magic_draw
        self.magic_number = 0
        self.magic = list(Magic_choice.keys())[self.magic_number]

        self.playerstats = {'Health': 100, 'Mana': 60, 'Attack': 10, 'Magic': 6, 'Speed': 5}
        self.Mana = 50
        self.Health = 70
        self.speed = self.playerstats['Speed']
        self.exp = 1

    # Start animation
    def character_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if 'Rest' not in self.status and 'Melee' not in self.status and 'Magic' not in self.status:
                self.status = self.status + '_Rest'

        if self.attack == 'Melee':
            self.direction.x = 0
            self.direction.y = 0
            if 'Melee' not in self.status and 'Magic' not in self.status:
                if 'Rest' in self.status:
                    self.status = self.status.replace('_Rest', '_Melee')
                else:
                    self.status = self.status + '_Melee'

        elif self.attack == 'Magic':
            self.direction.x = 0
            self.direction.y = 0
            if 'Melee' not in self.status and 'Magic' not in self.status:
                if 'Rest' in self.status:
                    self.status = self.status.replace('_Rest', '_Magic')
                else:
                    self.status = self.status + '_Magic'
        else:
            if 'Melee' in self.status:
                self.status = self.status.replace('_Melee', '')
            elif 'Magic' in self.status:
                self.status = self.status.replace('_Magic', '')

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

        if self.status == 'Up_Melee' or self.status == 'Up_Magic':
            self.current_attack += 0.35

            if self.current_attack >= len(self.up_attack):
                self.weapon_destroy()
                self.attack = 'Ready'
                self.destroy_animation()

            self.image = self.up_attack[int(self.current_attack)]

        elif self.status == 'Right_Melee' or self.status == 'Right_Magic':
            self.current_attack += 0.35

            if self.current_attack >= len(self.right_attack):
                self.weapon_destroy()
                self.attack = 'Ready'
                self.destroy_animation()

            self.image = self.right_attack[int(self.current_attack)]

        elif self.status == 'Left_Melee' or self.status == 'Left_Magic':
            self.current_attack += 0.35

            if self.current_attack >= len(self.left_attack):
                self.weapon_destroy()
                self.attack = 'Ready'
                self.destroy_animation()

            self.image = self.left_attack[int(self.current_attack)]

        elif self.status == 'Down_Melee' or self.status == 'Down_Magic':
            self.current_attack += 0.35

            if self.current_attack >= len(self.down_attack):
                self.weapon_destroy()
                self.attack = 'Ready'
                self.destroy_animation()

            self.image = self.down_attack[int(self.current_attack)]

        elif self.status == 'Right_Rest':
            self.image = self.right

        elif self.status == 'Left_Rest':
            self.image = self.left

        elif self.status == 'Up_Rest':
            self.image = self.up

        elif self.status == 'Down_Rest':
            self.image = self.down

    def destroy_animation(self):
        if 'Melee' in self.status:
            self.status = self.status.replace('_Melee', '')
        self.current_attack = 0

    # Getting Input
    def input(self):
        if self.attack == 'Ready':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'Up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'Down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'Left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'Right'
            else:
                self.direction.x = 0

            if keys[pygame.K_q]:
                self.attack = 'Melee'
                self.attack_time = pygame.time.get_ticks()
                self.weapon_draw()

            if keys[pygame.K_w]:
                self.attack = 'Magic'
                self.attack_time = pygame.time.get_ticks()
                type = list(Magic_choice.keys())[self.magic_number]
                effect = list(Magic_choice.values())[self.magic_number]['Effect'] + self.playerstats['Magic']
                mana_usage = list(Magic_choice.values())[self.magic_number]['Mana_usage']
                self.magic_draw(type, effect, mana_usage)

            if keys[pygame.K_LSHIFT]:
                self.speed = self.playerstats['Speed'] + 3
                self.cycle_speed = 0.3
            else:
                self.speed = self.playerstats['Speed']
                self.cycle_speed = 0.22

    def cooldown(self):
        current_tick = pygame.time.get_ticks()
        if current_tick - self.attack_time > self.attack_cooldown:
            self.attack = 'Ready'
            self.current_attack = 0
            self.weapon_destroy()

    # change in frame
    def update(self):

        self.input()
        self.cooldown()
        self.animations()
        self.character_status()
        self.move(self.speed)
