import pygame, sys

class Button():
    
    def __init__(self, screen,settings, x_pos, y_pos, message):     
        self.screen = screen
        self.settings = settings

        self.width, self.height = settings.button_width, settings.button_height
        self.x_position, self.y_position = x_pos, y_pos
        self.rect = pygame.Rect(x_pos, y_pos, self.width, self.height)
        self.font = pygame.font.SysFont(settings.button_font, settings.button_font_size)
        self.message = message        

        self.prep_messasge()

    def prep_messasge(self):
        self.msg_image = self.font.render(self.message, True, self.settings.button_text_color)
        self.msg_x = self.x_position + (self.width - self.msg_image.get_width()) / 2
        self.msg_y = self.y_position + (self.height - self.msg_image.get_height()) / 2

    def blitme(self):
        self.screen.fill(self.settings.button_bg, self.rect)
        self.screen.blit(self.msg_image, (self.msg_x, self.msg_y))
    
    def check_push(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                 if self.rect.collidepoint(mouse_x, mouse_y):
                    return True
        return False