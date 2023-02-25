import pygame, sys
from pygame.sprite import Sprite
from components.Balloon import Balloon
from components.Scoreboard import Scoreboard
from components.Button import Button
from components.Boom import Boom
from components.Star import Star

class Games():
    
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
    
    def run_demo_game(self):
        self.settings.nr_balloons = 4
        # Create a list to hold our balloons, and include our first balloon in the list
        balloons_demo = [Balloon(self.screen)]
        boom = Boom(self.screen)
        scoreboard_demo = Scoreboard(self.screen, self.settings)
        playing_game = True
        new_balloon = False
        boom_ballon = False
        stars = []
        new_balloon_button = Button(self.screen, self.settings.screen_width / 2 - self.settings.button_width / 2,
                                    self.settings.screen_height / 2 + 125 - self.settings.button_height / 2, self.settings, "New Balloon")

        end_button = Button(self.screen, self.settings.screen_width / 2 - self.settings.button_width / 2,
                            self.settings.screen_height / 2 + 125 - self.settings.button_height / 2, self.settings, "Start Game")

        time_to_blow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        n = 0
        while playing_game:
            mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

            # Redraw the empty screen before redrawing any game objects
            self.screen.fill(self.settings.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if balloons_demo[0].rect.collidepoint(mouse_x, mouse_y):
                        n += 1
                        stars.append(Star(self.screen, self.settings, n))
                        for balloon in balloons_demo:
                            balloon.update(self.settings.balloon_scale)
                            if time_to_blow[n] == 1:
                                balloons_demo.remove(balloon)
                                scoreboard_demo.update_nrstars(0)
                                new_balloon = True
                                boom_ballon = True
                    else:
                        for star in stars:
                            if star.rect.collidepoint(mouse_x, mouse_y):
                                balloons_demo.remove(balloon)
                                scoreboard_demo.update_nrstars(n)
                                new_balloon = True

            if new_balloon and scoreboard_demo.nr_balloons > 1:
                balloons_demo = [Balloon(self.screen)]
                new_balloon = False
                n = 0
                waiting = True
                if boom_ballon:
                    boom.blitme()
                    boom_ballon = False
                scoreboard_demo.blitme()
                new_balloon_button.blitme()
                if scoreboard_demo.nr_balloons == 3:
                    time_to_blow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                elif scoreboard_demo.nr_balloons == 4:
                    time_to_blow = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                elif scoreboard_demo.nr_balloons == 2:
                    time_to_blow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for star in stars:
                    star.blitme()
                pygame.display.flip()
                stars = []
                while waiting:
                    mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if new_balloon_button.rect.collidepoint(mouse_x, mouse_y):
                                waiting = False
                                scoreboard_demo.update_nrballons()

            elif new_balloon and scoreboard_demo.nr_balloons == 1:
                waiting = True
                scoreboard_demo.update_nrballons()
                end_button.blitme()
                if boom_ballon:
                    boom.blitme()
                scoreboard_demo.blitme()
                for star in stars:
                    star.blitme()
                pygame.display.flip()
                while waiting:
                    mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if end_button.rect.collidepoint(mouse_x, mouse_y):
                                return

            # redraw the screen, every pass through the event loop
            self.screen.fill(self.settings.bg_color)
            for balloon in balloons_demo:
                balloon.blitme()
            scoreboard_demo.blitme()
            for star in stars:
                star.blitme()
            pygame.display.flip()