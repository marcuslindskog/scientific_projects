import pygame, sys

class Star():

    def __init__(self, screen, settings, starn):
        self.screen = screen
        self.settings = settings
        self.startimage = pygame.image.load('img/star.png')
        self.startimage_w, self.startimage_h = self.startimage.get_size()

        self.image = pygame.transform.smoothscale(self.startimage, (25, 25))
        self.image_w, self.image_h = self.image.get_size()
        
        if starn < 11:
            self.x_position = self.screen.get_width()-30
            self.y_position = self.screen.get_height() - settings.scoreboard_height - 25 * starn
        elif starn>10 and starn< 21:
            self.x_position = self.screen.get_width() - 60
            self.y_position = self.screen.get_height() - settings.scoreboard_height - 25 * (starn-10)
        elif starn > 20 and starn < 31:
            self.x_position = self.screen.get_width() - 90
            self.y_position = self.screen.get_height()-settings.scoreboard_height-25 * (starn-20)
        elif starn > 30 and starn < 41:
            self.x_position = self.screen.get_width() - 120
            self.y_position = self.screen.get_height()-settings.scoreboard_height-25 * (starn-30)

        self.update_rect()

    def blitme(self):
        draw_pos = self.image.get_rect()
        draw_pos = draw_pos.move(self.x_position, self.y_position)
        self.screen.blit(self.image, draw_pos)

    def update_rect(self):
        self.rect = pygame.Rect(self.x_position, self.y_position,
                                self.image_w, self.image_h)

    def check_push(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True
        else: return False