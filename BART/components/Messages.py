import pygame, pygame.font, pygame.event, pygame.draw, random
from pygame.sprite import Sprite
from pygame.locals import *

class Messages():

    def __init__(self, screen) -> None:
        self.screen = screen

    def ask(self, question):
        pygame.font.init()
        current_string = []
        self.display_box(question + ": " + "".join(current_string))
        while 1:
            inkey = self.get_key()
            if inkey == K_BACKSPACE:
                current_string = current_string[0:-1]
            elif inkey == K_RETURN:
                break
            elif inkey == K_MINUS:
                current_string.append("_")    
            elif inkey <= 127:
                current_string.append(chr(inkey))
                self.display_box(question + ": " + "".join(current_string))
        return "".join(current_string)
    
    def display_box(self, message=""):
        fontobject = pygame.font.Font(None,32)
        pygame.draw.rect(self.screen, (0,0,0),
                        ((self.screen.get_width() / 2) - 100,
                            (self.screen.get_height() / 2) - 10,
                            200,40), 0)
        pygame.draw.rect(self.screen, (0,0,0),
                        ((self.screen.get_width() / 2) - 102,
                            (self.screen.get_height() / 2) - 12,
                            204,44), 1)
        if len(message) != 0:
            self.screen.blit(fontobject.render(message, 1, (255,255,255)),
                        ((self.screen.get_width() / 2) - 100, (self.screen.get_height() / 2) - 10))
        pygame.display.flip()
    
    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass