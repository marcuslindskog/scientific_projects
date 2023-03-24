import pygame, sys, csv
from pygame.sprite import Sprite
from components.Balloon import Balloon
from components.Scoreboard import Scoreboard
from components.Button import Button
from components.Boom import Boom
from components.Star import Star

class Games():
    
    def __init__(self, screen, settings, is_demo, datafile='data/demo.txt', participant='demo'):
        self.screen = screen
        self.settings = settings
        self.boom = Boom(self.screen)
        self.scoreboard = Scoreboard(self.screen, self.settings)
        self.new_balloon_button = Button(self.screen, self.settings.screen_width / 2 - self.settings.button_width / 2,
                                    self.settings.screen_height / 2 + 125 - self.settings.button_height / 2, self.settings, "New Balloon")
        if is_demo:
            self.end_button = Button(self.screen, self.settings.screen_width / 2 - self.settings.button_width / 2,
                                self.settings.screen_height / 2 + 125 - self.settings.button_height / 2, self.settings, "Start Game")
            
            with open('input/demo_input.csv', 'r') as f:
                reader = csv.reader(f)
                self.times_to_blow = list(reader) 
        else:    
            self.end_button = Button(screen, settings.screen_width / 2 - settings.button_width / 2,
                                    settings.screen_height / 2 + 125 - settings.button_height / 2, settings, "Game Finished")
            with open('input/main_game_input.csv', 'r') as f:
                reader = csv.reader(f)
                self.times_to_blow = list(reader)

        self.demo_button = Button(self.screen, self.settings.screen_width / 2 - self.settings.button_width / 2,
                        self.settings.screen_height / 2 + 125 - self.settings.button_height / 2, settings, "Start Demo")
        self.is_demo = is_demo
        self.datafile = datafile
        self.participant = participant
    
    def run_game(self):
        if self.is_demo:
            self.demo_button.blitme()
            pygame.display.flip()
            waiting = True
            while waiting:
                mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.demo_button.rect.collidepoint(mouse_x, mouse_y):
                            waiting = False

        balloons = [Balloon(self.screen)]
        playing_game = True
        new_balloon = False
        boom_ballon = False
        stars = []
        ballon_number = 0
        time_to_blow = list(map(int, self.times_to_blow[ballon_number]))
        n=0
        while playing_game:
            mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            # Redraw the empty screen before redrawing any game objects
            self.screen.fill(self.settings.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if balloons[0].rect.collidepoint(mouse_x, mouse_y):
                            n += 1
                            stars.append(Star(self.screen, self.settings, n))
                            for balloon in balloons:
                                balloon.update(self.settings.balloon_scale)
                                if time_to_blow[n] == 1:
                                    balloons.remove(balloon)
                                    self.scoreboard.update_nrstars(0)
                                    new_balloon = True
                                    boom_ballon = True
                        else:
                            for star in stars:
                                if star.rect.collidepoint(mouse_x, mouse_y):
                                    balloons.remove(balloon)
                                    self.scoreboard.update_nrstars(n)
                                    new_balloon = True

            if new_balloon and self.scoreboard.nr_balloons > 1:
                # Save data to file
                with open(self.datafile, 'a') as f:
                    if boom_ballon:
                        f.write(self.participant + self.settings.delim + str(1+ self.settings.nr_balloons - self.scoreboard.nr_balloons) +
                                self.settings.delim + "1" + self.settings.delim + str(time_to_blow.index(1)) + self.settings.delim +
                                str(n) + self.settings.delim  + str(0) + self.settings.delim + str(self.scoreboard.nr_stars)
                                + '\n')
                    else:
                        f.write(self.participant + self.settings.delim + str(1+ self.settings.nr_balloons - self.scoreboard.nr_balloons) +
                                self.settings.delim + "0" + self.settings.delim + str(time_to_blow.index(1)) + self.settings.delim +
                                str(n) + self.settings.delim  + str(n) + self.settings.delim + str(self.scoreboard.nr_stars)
                                + '\n')

                balloons = [Balloon(self.screen)]
                new_balloon = False
                n = 0
                waiting = True
                if boom_ballon:
                    self.boom.blitme()
                    boom_ballon = False
                self.scoreboard.blitme()
                self.new_balloon_button.blitme()
                ballon_number += 1
                time_to_blow = list(map(int, self.times_to_blow[ballon_number]))
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
                            if self.new_balloon_button.rect.collidepoint(mouse_x, mouse_y):
                                waiting = False
                                self.scoreboard.update_nrballons()

            elif new_balloon and self.scoreboard.nr_balloons == 1:
                # Save data to file
                with open(self.datafile, 'a') as f:
                    if boom_ballon:
                        f.write(self.participant + self.settings.delim + str(1 + self.settings.nr_balloons - self.scoreboard.nr_balloons) +
                                self.settings.delim + "1" + self.settings.delim + str(time_to_blow.index(1)) + self.settings.delim +
                                str(n) + self.settings.delim + str(0) + self.settings.delim + str(self.scoreboard.nr_stars)
                                + '\n')
                    else:
                        f.write(self.participant + self.settings.delim + str(1 + self.settings.nr_balloons - self.scoreboard.nr_balloons) +
                                self.settings.delim + "0" + self.settings.delim + str(time_to_blow.index(1)) + self.settings.delim +
                                str(n) + self.settings.delim + str(n) + self.settings.delim + str(self.scoreboard.nr_stars)
                                + '\n')
                waiting = True
                self.scoreboard.update_nrballons()
                self.end_button.blitme()
                self.scoreboard.blitme()
                pygame.display.flip()
                while waiting:
                    mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.end_button.rect.collidepoint(mouse_x, mouse_y):
                                waiting = False
                                return

            #redraw the screen, every pass through the event loop
            self.screen.fill(self.settings.bg_color)
            for balloon in balloons:
                balloon.blitme()
            self.scoreboard.blitme()
            for star in stars:
                star.blitme()
            pygame.display.flip()