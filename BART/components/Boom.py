import pygame

class Boom():

    def __init__(self, screen):
        self.screen = screen

        self.startimage = pygame.image.load('img/boom.png')
        self.startimage_w, self.startimage_h = self.startimage.get_size()

        self.image = pygame.transform.smoothscale(self.startimage, (250, 250))
        self.image_w, self.image_h = self.image.get_size()
        self.x_position = self.screen.get_width()/2 - self.image_w/2
        self.y_position = self.screen.get_height()/2 - self.image_h/2

        self.rect = pygame.Rect(self.x_position, self.y_position,
                                self.image_w, self.image_h)

    def blitme(self):
        draw_pos = self.image.get_rect()
        draw_pos = draw_pos.move(self.x_position, self.y_position)
        self.screen.blit(self.image, draw_pos)