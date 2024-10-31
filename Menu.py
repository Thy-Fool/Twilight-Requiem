import pygame
import cv2
from Settings import *
from Main import Game
from transition import Videoplayer


# The Menu Class
class Menu:
    def __init__(self, the_video):
        super().__init__()

        # Start
        pygame.init()

        self.the_video = the_video
        self.fpsvideo = self.the_video.fps

        # Screen, Clock and Caption
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Twilight Requiem')
        pygame.display.set_icon(pygame.image.load('Menu/Background/Logo.png'))
        self.all_surface = pygame.display.get_surface()

    # Run
    def run(self):
        # Screen Color
        self.screen.fill((0, 0, 0))

        # Tick And Update
        self.clock.tick(self.fpsvideo)

        # Playing the video
        self.the_video.play(self.all_surface)


# Main Class
class Change_state:
    def __init__(self):

        # Current state
        self.game_state = 'Menu_start'

        # Intro Video Call
        self.intro_vid = Videoplayer('Menu/Background/Video1.mp4', width / 2, height / 2, False)
        self.menu_start = Menu(self.intro_vid)

        # Story Video Call
        self.story_video = Videoplayer('Menu/Background/Video2.mp4', width / 2, 300, False)
        self.story = Menu(self.story_video)

        # Loop Video Call
        self.bg_video = Videoplayer('Menu/Background/Bg_loop_video.mp4', width / 2 - 30, 280, True)
        self.menu = Menu(self.bg_video)

        # Game Call
        self.main = Game()

        self.all_surface = pygame.display.get_surface()
        self.start_time = pygame.time.get_ticks()

        # Text status
        self.text_drawn = False
        self.show_text = True
        self.delay = 10000
        self.blink_time = 1000
        self.previous_blink = 0

        # Text
        self.start = pygame.font.Font(Main_font, 36).render('Press SPACEBAR to Start', True, (255, 255, 255))
        self.stop = pygame.font.Font(Main_font, 26).render('Press TAB to Quit', True, (255, 255, 255))

    # States handling
    def event_handle(self):
        current_tick = pygame.time.get_ticks()
        if self.game_state == 'Menu_start':
            self.menu_start.run()
            if self.intro_vid.video.get(cv2.CAP_PROP_POS_FRAMES) == self.intro_vid.video.get(cv2.CAP_PROP_FRAME_COUNT):
                self.game_state = 'Menu'

        if self.game_state == 'Menu':
            self.menu.run()

            # Allowing the text to be drawn after some period of time
            if current_tick - self.start_time >= self.delay:
                self.text_drawn = True

                # Text Blinking
                if current_tick - self.previous_blink >= self.blink_time:
                    self.show_text = not self.show_text
                    self.previous_blink = current_tick

                if self.show_text:
                    start_rect = self.start.get_rect(center=(448, 580))
                    stop_rect = self.stop.get_rect(center=(448, 600))
                    self.all_surface.blit(self.start, start_rect)
                    self.all_surface.blit(self.stop, stop_rect)

        if self.game_state == 'Story':
            self.story.run()
            if self.story_video.video.get(cv2.CAP_PROP_POS_FRAMES) == self.story_video.video.get(
                    cv2.CAP_PROP_FRAME_COUNT):
                self.game_state = 'Game'

        if self.game_state == 'Game':
            self.main.run()

    # run
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.text_drawn:
                        self.game_state = 'Story'
                    if event.key == pygame.K_TAB and self.text_drawn:
                        running = False

            self.event_handle()

            pygame.display.update()


Change_state().run()
