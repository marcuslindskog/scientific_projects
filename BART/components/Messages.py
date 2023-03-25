import pygame
from components.Inputs import Inputs

class Messages():

    def __init__(self, screen) -> None:
        self.screen = screen
        self.inputs = Inputs()

    def ask(self, question):
        pygame.font.init()
        current_string = []
        self.display_box(question + ": " + "".join(current_string))
        while 1:
            current_string, time_to_break = self.inputs.get_text(current_string)
            if time_to_break:
                break
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