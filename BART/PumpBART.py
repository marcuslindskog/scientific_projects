import pygame
from pygame.sprite import Sprite


class PumpBART(Sprite):

    def __init__(self, screen, settings):

        Sprite.__init__(self)
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('pump.png').convert_alpha()
        self.image_w, self.image_h = self.image.get_size()

        self.image = pygame.transform.smoothscale(self.image, (settings.screen_width/10, settings.screen_height/3))

        self.x_position = settings.screen_width/10
        self.y_position = self.screen.get_height() - settings.scoreboard_height - settings.screen_height/3


        self.update_rect()

    def blitme(self):
        draw_pos = self.image.get_rect().move(self.x_position, self.y_position)
        self.screen.blit(self.image, draw_pos)

    def update_rect(self):
        self.rect = pygame.Rect(self.x_position-self.image_w/2, self.y_position-self.image_h/2,
                                self.image_w, self.image_h)