import pygame
import cv2


# Video Player
class Videoplayer:
    def __init__(self, vid, posx, posy, will_loop=False):

        self.video = cv2.VideoCapture(vid)

        # Extracting frames
        self.success, self.video_image = self.video.read()
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.will_loop = will_loop
        self.pos = (posx, posy)

    # Play
    def play(self, screen):
        self.success, self.video_image = self.video.read()
        # Converting Frames
        if self.success:
            video_surf = pygame.image.frombuffer(
                self.video_image.tobytes(), self.video_image.shape[1::-1], "BGR")
            video_rect = video_surf.get_rect(center=self.pos)
            screen.blit(video_surf, video_rect)
        else:
            if self.will_loop:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
