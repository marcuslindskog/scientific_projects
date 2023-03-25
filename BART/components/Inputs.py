import pygame
from pygame.locals import *

class Inputs():
    
    def __init__(self) -> None:
        pass

    def wait_for_enter(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    return
            pygame.time.wait(20)

    def get_text(self, string):
        current_string = string
        time_to_break = False
        inkey = self.get_key()
        if inkey == pygame.K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == pygame.K_RETURN:
             time_to_break = True
        elif inkey == pygame.K_MINUS:
            current_string.append("_")    
        elif inkey <= 127:
            current_string.append(chr(inkey))
        return current_string, time_to_break

    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                return event.key
            else:
                pass