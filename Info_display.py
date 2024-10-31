import pygame
from Settings import *


class UI:
    def __init__(self):
        super().__init__()
        self.all_surface = pygame.display.get_surface()

        self.Health_bar_img = pygame.image.load('Graphics/UI/Health_Bar.png').convert_alpha()
        self.Mana_bar_img = pygame.image.load('Graphics/UI/Mana_Bar.png').convert_alpha()
        self.Exp_img = pygame.image.load('Graphics/UI/Exp.png').convert_alpha()
        self.Health_bar = pygame.Rect(24, 11, Healthbar_length, Healthbar_width)
        self.Mana_bar = pygame.Rect(48, 88, Manabar_length, Manabar_width)
        self.font = pygame.font.Font(Main_font, 30)
        self.font_exp = pygame.font.Font(Main_font, 42)

    def draw_bar(self, background_bar, remaining, max_amount, color, x, y):
        pygame.draw.rect(self.all_surface, bar_color, background_bar, 0, 5)

        remaining_bar = background_bar.copy()
        remaining_bar.width = (remaining / max_amount) * background_bar.width
        display_text = str(int(remaining)) + '/' + str(int(max_amount))

        pygame.draw.rect(self.all_surface, color, remaining_bar, 0, 5)
        pygame.draw.rect(self.all_surface, (0, 0, 0), background_bar, 2, 5)
        info_text = self.font.render(display_text, False, text_color)
        text_rect = info_text.get_rect(topleft=(x, y))
        self.all_surface.blit(info_text, text_rect)

    def show_exp(self, exp):
        exp_text = self.font_exp.render(str(int(exp)), False, text_color)
        text_rect = exp_text.get_rect(center=(839, 596))

        pygame.draw.rect(self.all_surface, bar_color, text_rect.inflate(50, 25))
        self.all_surface.blit(exp_text, text_rect)
        pygame.draw.rect(self.all_surface, (0, 0, 0), text_rect.inflate(50, 25), 3)

    def selected_item(self, box_size, left, top):
        box_rect = pygame.Rect(left, top, box_size, box_size)
        pygame.draw.rect(self.all_surface, bar_color, box_rect)
        pygame.draw.rect(self.all_surface, (0, 0, 0), box_rect, 3)

    def melee_display(self, weapon):
        self.selected_item(80, 10, 550)

        full_path = f'Weapons/{weapon}/Full_img.png'
        weapon_full_img = pygame.image.load(full_path).convert_alpha()
        weapon_rect = weapon_full_img.get_rect(topleft=(10, 550))
        self.all_surface.blit(weapon_full_img, weapon_rect)

    def magic_display(self, magic):
        self.selected_item(40, 70, 590)

        full_path = f'Magic/{magic}/Full_img.png'
        magic_full_img = pygame.image.load(full_path).convert_alpha()
        magic_rect = magic_full_img.get_rect(topleft=(70, 590))
        self.all_surface.blit(magic_full_img, magic_rect)

    def run_ui(self, player):
        self.all_surface.blit(self.Health_bar_img, (10, 5))
        self.all_surface.blit(self.Mana_bar_img, (10, 74))
        self.draw_bar(self.Health_bar, player.Health, player.playerstats['Health'], Health_color1, 53, 28)
        self.draw_bar(self.Mana_bar, player.Mana, player.playerstats['Mana'], Mana_color, 53, 98)

        self.show_exp(player.exp)
        self.all_surface.blit(self.Exp_img, (767, 574))

        self.melee_display(player.weapon)
        self.magic_display(player.magic)
