class Settings():

    def __init__(self):
        # screen parameters
        self.screen_width, self.screen_height = 800, 600
        self.bg_color = 255, 255, 255
        self.bg_black_color = 0, 0, 0
        self.scoreboard_height = self.screen_height/10
        
        self.balloon_scale = 1.05
        self.nr_balloons = 6

        self.button_width, self.button_height = 250, 50
        self.button_bg = (0,163,0)
        self.button_text_color = (235,235,235)
        self.button_font, self.button_font_size = 'Arial', 24

        self.delim = ";"