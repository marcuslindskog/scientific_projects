import pygame, random
from components.Inputs import Inputs


class Highscore():

    def __init__(self, screen) -> None:
        self.screen = screen
        self.input = Inputs()
        
    def display_highscore(self, nickname=""):
        pygame.font.init()
        fontobject = pygame.font.Font(None, 32)

        bx, by = 800, 600
        GREEN, WHITE, BLACK = (51, 255, 51), (255, 255,255), (0,0,0)

        ranks = ['1:st', '2:nd', '3:rd', '4:th', '5:th']
        participants = ['hkh', 'big', 'col', 'aaa', 'mlp']
        if len(nickname) > 0:
            participants[random.randint(0, 4)] = nickname

        box = pygame.surface.Surface((bx, by))
        box.fill(BLACK)
        pygame.draw.rect(box, BLACK, (0, 0, bx, by), 1)
        txt_surf = fontobject.render("High Score", True, GREEN)
        txt_rect = txt_surf.get_rect(center=(bx // 2, 30))
        box.blit(txt_surf, txt_rect)

        txt_surf = fontobject.render("Press ENTER", True, WHITE)
        txt_rect = txt_surf.get_rect(center=(bx // 2, 360))
        box.blit(txt_surf, txt_rect)

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
        self.input.wait_for_enter()