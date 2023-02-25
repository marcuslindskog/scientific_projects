import pygame
from pygame.sprite import Sprite


class Balloon(Sprite):

    def __init__(self, screen):
        Sprite.__init__(self)
        self.screen = screen
        self.startimage = pygame.image.load('img/balloon_new.png')
        self.startimage_w, self.startimage_h = self.startimage.get_size()

        self.image = pygame.transform.smoothscale(self.startimage, (100, 100))
        self.image_w, self.image_h = self.image.get_size()
        self.x_position = self.screen.get_width()/2 - self.image_w/2
        self.y_position = self.screen.get_height()/2 - self.image_h/2

        self.update_rect()


    def update(self, scale):
        image_w, image_h = self.image.get_size()
        self.image = pygame.transform.smoothscale(self.startimage, (int(image_w*scale), int(image_h*scale)))
        image_w, image_h = self.image.get_size()
        self.x_position = self.screen.get_width()/2 - image_w/2
        self.y_position = self.screen.get_height()/2 - image_h/2

    def blitme(self):
        draw_pos = self.image.get_rect()
        draw_pos = draw_pos.move(self.x_position, self.y_position)
        self.screen.blit(self.image, draw_pos)

    def update_rect(self):
        self.rect = pygame.Rect(self.x_position, self.y_position,
                                self.image_w, self.image_h)
