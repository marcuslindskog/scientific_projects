import pygame, sys, csv
from components.Balloon import Balloon
from components.Scoreboard import Scoreboard
from components.Button import Button
from components.Boom import Boom
from components.Star import Star

class Games():
    
    def __init__(self, screen, settings, is_demo, datafile='data/demo.txt', participant='demo'):
        self.screen = screen
        self.settings = settings
        self.is_demo = is_demo
        self.datafile = datafile
        self.participant = participant

        self.boom = Boom(self.screen)
        self.scoreboard = Scoreboard(self.screen, self.settings)

        buttons_xpos = self.settings.screen_width / 2 - self.settings.button_width / 2
        buttons_ypos = self.settings.screen_height / 2 + 125 - self.settings.button_height / 2

        self.new_balloon_button = Button(self.screen, self.settings, buttons_xpos, buttons_ypos, "New Balloon")
        self.demo_button = Button(self.screen, self.settings, buttons_xpos, buttons_ypos, "Start Demo")
        
        if self.is_demo:
            self.end_button = Button(self.screen, self.settings, buttons_xpos, buttons_ypos, "Start Game")
            input_file = 'input/demo_input.csv'
        else:    
            self.end_button = Button(self.screen, self.settings,buttons_xpos, buttons_ypos, "Game Finished")
            input_file = 'input/main_game_input.csv'

        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            self.times_to_blow = list(reader) 
        
    def run_game(self):
        playing_game = True
        new_balloon = False
        boom_ballon = False

        balloon = Balloon(self.screen)      
        ballon_number = 0
        number_of_pumps = 0
        time_to_blow = list(map(int, self.times_to_blow[ballon_number]))

        stars = []

        if self.is_demo:
            self.demo_button.blitme()
            pygame.display.flip()
            waiting = True
            while waiting:
                if self.demo_button.check_push():
                    waiting = False

       
        while playing_game:
            self.screen.fill(self.settings.bg_color)

            mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            mouse_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = True
                    
            if mouse_pressed and balloon.check_push(mouse_x, mouse_y):
                number_of_pumps += 1
                stars.append(Star(self.screen, self.settings, number_of_pumps))
                balloon.update(self.settings.balloon_scale)
                if time_to_blow[number_of_pumps] == 1:
                    self.scoreboard.update_nrstars(0)
                    new_balloon = True
                    boom_ballon = True
            
            for star in stars:
                if mouse_pressed and star.check_push(mouse_x, mouse_y):
                    self.scoreboard.update_nrstars(number_of_pumps)
                    new_balloon = True

            if new_balloon:
                value_list = [self.participant,
                              str(ballon_number + 1),
                              "1" if boom_ballon else "0",
                              str(time_to_blow.index(1)),
                              str(number_of_pumps),
                              "0" if boom_ballon else str(number_of_pumps),
                              str(self.scoreboard.nr_stars)
                              ]
                output_string = self.settings.delim.join(value_list)
                with open(self.datafile, 'a') as f:
                    f.write(output_string + '\n')

            if new_balloon and self.scoreboard.nr_balloons > 1:
                ballon_number += 1
                self.scoreboard.update_nrballons()

                balloon = Balloon(self.screen)
                new_balloon = False
                number_of_pumps = 0
                time_to_blow = list(map(int, self.times_to_blow[ballon_number]))
         
                if boom_ballon:
                    self.boom.blitme()
                    boom_ballon = False
                self.scoreboard.blitme()
                self.new_balloon_button.blitme()
                
                
                for star in stars:
                    star.blitme()
                pygame.display.flip()
                
                stars = []

                waiting = True
                while waiting:
                    if self.new_balloon_button.check_push():
                        waiting = False

            elif new_balloon and self.scoreboard.nr_balloons == 1:                
                self.scoreboard.update_nrballons()
                self.end_button.blitme()
                self.scoreboard.blitme()
                pygame.display.flip()

                waiting = True
                while waiting:
                    if self.end_button.check_push():
                        waiting = False
                        playing_game = False

            self.screen.fill(self.settings.bg_color)
            balloon.blitme()
            self.scoreboard.blitme()
            for star in stars:
                star.blitme()
            pygame.display.flip()