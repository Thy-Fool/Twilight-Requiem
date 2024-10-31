import pygame
from Settings import *
from Level import Grassland


# Creating Game CLass
class Game:
    # Initialize
    def __init__(self):
        super().__init__()

        # Start
        pygame.init()

        # Screen, Clock and Caption
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Twilight Requiem')
        pygame.display.set_icon(pygame.image.load('Menu/Background/Logo.png'))

        # Calling Level
        self.level = Grassland()
        self.level.grassland()

    # Run
    def run(self):


            # Screen Color
            self.screen.fill((0, 0, 0))

            # Calling Level Run
            self.level.run()

            # Tick And Update
            self.clock.tick(fps)

            pygame.display.update()

