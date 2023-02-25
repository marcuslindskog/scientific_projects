import pygame, pygame.font
from pygame.sprite import Sprite


class Scoreboard(Sprite):

    def __init__(self, screen, settings):

        Sprite.__init__(self)
        self.screen = screen
        self.settings = settings

        self.initialize_stats(settings)
        
        # Set dimensions and properties of scoreboard
        self.sb_height, self.sb_width = settings.scoreboard_height, self.screen.get_width()
        self.rect = pygame.Rect(0, self.screen.get_height()-self.sb_height, self.sb_width, self.sb_height)
        self.bg_color=(100,100,100)
        self.text_color = (225,225,225)
        self.font = pygame.font.SysFont('Arial', 32)

        # Set positions of individual scoring elements on the scoreboard
        self.x_balloons_position, self.y_balloons_position = settings.screen_width/2-150, settings.screen_height-settings.scoreboard_height+15
        self.x_stars_position, self.y_stars_position  =  settings.screen_width/2+150, settings.screen_height-settings.scoreboard_height + 15

        self.starimage = pygame.image.load('img/star.png')
        self.starimage_w, self.starimage_h = self.starimage.get_size()

        self.ballonimage = pygame.image.load('img/balloon_new.png')
        self.ballonimage_w, self.ballonimage_h = self.ballonimage.get_size()

        self.image = pygame.transform.smoothscale(self.starimage, (50, 50))
        self.image_w, self.image_h = self.image.get_size()
        self.star_x_position = self.screen.get_width()/2+100
        self.star_y_position = self.screen.get_height() - settings.scoreboard_height + 5

        self.image_balloon = pygame.transform.smoothscale(self.ballonimage, (50, 50))
        self.image_balloon_w, self.image_balloon_h = self.image_balloon.get_size()
        self.balloon_x_position = self.screen.get_width() / 2 - 200
        self.balloon_y_position = self.screen.get_height() - settings.scoreboard_height + 10

    def initialize_stats(self, settings):
        # Game attributes to track for scoring
        self.nr_balloons = settings.nr_balloons
        self.nr_stars = 0


    def prep_scores(self):
        self.nr_ballons_string = ": " + format(self.nr_balloons, ',d')
        self.nr_balloons_image = self.font.render(self.nr_ballons_string, True, self.text_color)


        self.nr_stars_string = ": " + format(self.nr_stars, ',d')
        self.nr_stars_image = self.font.render(self.nr_stars_string, True, self.text_color)

    def update_nrstars(self, n):
        self.nr_stars += n

    def update_nrballons(self):
        self.nr_balloons -=1

    def blitme(self):
        # Turn individual scoring elements into images that can be drawn
        self.prep_scores()
        # Draw blank scoreboard
        self.screen.fill(self.bg_color, self.rect)
        # Draw individual scoring elements
        draw_pos = self.image.get_rect()
        draw_pos = draw_pos.move(self.star_x_position, self.star_y_position)
        self.screen.blit(self.image, draw_pos)
        self.screen.blit(self.nr_stars_image , (self.x_stars_position, self.y_stars_position))

        draw_pos_balloon = self.image_balloon.get_rect()
        draw_pos_balloon = draw_pos_balloon.move(self.balloon_x_position, self.balloon_y_position)
        self.screen.blit(self.image_balloon, draw_pos_balloon)
        self.screen.blit(self.nr_balloons_image, (self.x_balloons_position, self.y_balloons_position))

