import pygame
from CSV import import_folder


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)

        self.sprite_type = 'Weapons'
        self.player = player

        # Getting direction and importing weapons
        self.direction = player.status.split('_')[0]

        path = f'Weapons/{player.weapon}/{self.direction}'
        self.image_list = import_folder(path)
        self.current_melee = 0
        self.image = (self.image_list[self.current_melee]).convert_alpha()

        # Getting rectangle positions
        if 'Right' in player.status:
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(-28, -5))
        elif 'Left' in player.status:
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(14, -5))
        elif 'Down' in player.status:
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-28, -8))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-30, 38))

    # Cycling weapons
    def cycle_weapon(self):
        if self.player.attack == 'Melee':
            self.current_melee += 0.35

            if self.current_melee >= len(self.image_list):
                self.current_melee = 0

        self.image = (self.image_list[int(self.current_melee)]).convert_alpha()

    def update(self):
        self.cycle_weapon()
