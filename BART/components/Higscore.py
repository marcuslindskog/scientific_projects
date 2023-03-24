import pygame, pygame.font, pygame.event, pygame.draw, random
from pygame.sprite import Sprite
from pygame.locals import *


class Highscore(Sprite):

    def __init__(self, screen) -> None:
        self.screen = screen
        
    def display_highscore(self, nickname=""):
        pygame.font.init()
        fontobject = pygame.font.Font(None, 32)
        bx = 800 # x-size of box
        by = 600  # y-size of box
        GREEN = (51, 255, 51)
        WHITE = (255, 255,255)
        BLACK = (0,0,0)

        ranks = ['1:st', '2:nd', '3:rd', '4:th', '5:th']
        participants = ['hkh', 'big', 'col', 'aaa', 'mlp']
        if len(nickname) > 1:
            participants[random.randint(0, 4)] = nickname

        # make the presentation box
        box = pygame.surface.Surface((bx, by))
        box.fill(BLACK)
        pygame.draw.rect(box, BLACK, (0, 0, bx, by), 1)
        txt_surf = fontobject.render("High Score", True, GREEN)  # headline
        txt_rect = txt_surf.get_rect(center=(bx // 2, 30))
        box.blit(txt_surf, txt_rect)

        txt_surf = fontobject.render("Press ENTER", True, WHITE)  # bottom line
        txt_rect = txt_surf.get_rect(center=(bx // 2, 360))
        box.blit(txt_surf, txt_rect)

        # write the top-10 data to the box
        i = 0
        for rank, par in zip(ranks, participants):
            if str(par) == nickname:
                color_to_use = GREEN
            else:
                color_to_use = WHITE
            txt_surf = fontobject.render(rank + "      " + str(par), True, color_to_use)
            txt_rect = txt_surf.get_rect(center=(bx // 2, 30 * i + 120))
            box.blit(txt_surf, txt_rect)
            i += 1

        self.screen.blit(box, (0, 0))
        pygame.display.flip()

        while True:  # wait for user to acknowledge and return
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    return
            pygame.time.wait(20)