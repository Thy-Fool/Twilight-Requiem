import pygame
from Settings import *
from Obstacles import Obstacles
from Player import Player
from CSV import import_files, import_folder
from Weapons import Weapon
from Info_display import UI
from Beasts import Beasts


# Creating Level class
class Grassland:
    # Initialize
    def __init__(self):

        # Getting All Images At Once
        self.all_surface = pygame.display.get_surface()

        # Sprites Groups
        self.visible = Camera()
        self.obstacles = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.attacking_sprites = pygame.sprite.Group()

        self.drawn_attack = None

        # Info Display
        self.ui = UI()

    # Map Function
    def grassland(self):
        layouts = {'OuterBoundary': import_files('map/Map_OuterBoundary.csv'),
                   'WallBoundary': import_files('map/Map_WallBoundary.csv'),
                   'border_64': import_files('map/Map_Border_64.csv'),
                   'border_128': import_files('map/Map_Border_128.csv'),
                   'grass': import_files('map/Map_Grass.csv'),
                   'objects': import_files('map/Map_Objects.csv'),
                   'Entities': import_files('map/Map_Beasts.csv')}

        graphics = {'grass': import_folder('Graphics/Grass'),
                    'border_64': import_folder('Graphics/Border_64'),
                    'border_128': import_folder('Graphics/Border_128'),
                    'objects': import_folder('Graphics/Objects')
                    }

        for sprite_type, layout in layouts.items():
            for row, row_content in enumerate(layout):
                for column, column_content in enumerate(row_content):
                    if column_content != '-1':
                        x = column * obstacles_size
                        y = row * obstacles_size
                        if sprite_type == 'OuterBoundary':
                            Obstacles(x - 32, y - 48, self.obstacles, 'invisible')
                        if sprite_type == 'WallBoundary':
                            Obstacles(x - 32, y - 64, self.obstacles, 'invisible')
                        if sprite_type == 'grass':
                            grass_img = (graphics['grass'][int(column_content)]).convert_alpha()
                            Obstacles(x - 32, y - 32, [self.visible, self.obstacles, self.attackable_sprites], 'Grass', grass_img)
                        if sprite_type == 'border_64':
                            border64_img = (graphics['border_64'][int(column_content)]).convert_alpha()
                            Obstacles(x - 32, y - 32, [self.visible, self.obstacles], 'border_64', border64_img)
                        if sprite_type == 'border_128':
                            border128_img = (graphics['border_128'][int(column_content)]).convert_alpha()
                            Obstacles(x - 64, y - 128, [self.visible, self.obstacles], 'border_128', border128_img)
                        if sprite_type == 'objects':
                            object_img = (graphics['objects'][int(column_content)]).convert_alpha()
                            Obstacles(x - 32, y - 64, [self.visible, self.obstacles], 'objects', object_img)
                        if sprite_type == 'Entities':
                            if column_content == '3':
                                self.player = Player(x, y, self.visible, self.obstacles, self.weapon_draw,
                                                     self.weapon_destroy,
                                                     self.magic_draw)
                            else:
                                n = None
                                if column_content == '0':
                                    n = 'Dark_Knight'
                                Beasts(x, y, [self.visible, self.attackable_sprites], n, self.obstacles)

    def weapon_draw(self):
        self.drawn_attack = Weapon(self.player, [self.visible, self.attacking_sprites])

    def weapon_destroy(self):
        if self.drawn_attack:
            self.drawn_attack.kill()
        self.drawn_attack = None

    def magic_draw(self, type, effect, mana_usage):
        pass

    def player_attack_logic(self):
        if self.attacking_sprites:
            for attack_sprite in self.attacking_sprites:
                sprites_collide = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if sprites_collide:
                    for target_sprite in sprites_collide:
                        if target_sprite.sprite_type == 'Grass':
                            target_sprite.kill()
                        else:
                            target_sprite.damage_dealt(attack_sprite, self.player)
                            target_sprite.knockback()

    # Run
    def run(self):
        self.visible.create(self.player)
        self.visible.update()
        self.visible.beast_update(self.player)
        self.ui.run_ui(self.player)
        self.player_attack_logic()


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.all_surface = pygame.display.get_surface()
        self.center_x = 448
        self.center_y = 320
        self.offset = pygame.math.Vector2()

        path = f'map/grassland.png'
        self.level_image = pygame.image.load(path).convert_alpha()
        self.level_rect = self.level_image.get_rect(topleft=(0, 0))

    def create(self, player):
        self.offset.x = player.rect.centerx - self.center_x
        self.offset.y = player.rect.centery - self.center_y
        self.all_surface.blit(self.level_image, self.level_rect.topleft - self.offset)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.all_surface.blit(sprite.image, sprite.rect.center - self.offset)

    def beast_update(self, player):
        beast_sprites = []
        for beast in self.sprites():
            if beast.sprite_type == 'Beast':
                beast_sprites.append(beast)
        for item in beast_sprites:
            item.update_beasts(player)


class Area_2:
    def __init__(self):
        pass
