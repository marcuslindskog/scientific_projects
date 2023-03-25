import pygame

from settings.Settings import Settings
from components.Higscore import Highscore
from components.Messages import Messages
from components.Participant import Participant
from components.Games import Games

def Bart_Run():
    settings = Settings()  

    pygame.init()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Balloon Hunt")
    
    messages = Messages(screen=screen)
    highscore = Highscore(screen)

    participant = Participant()
    participant.id = messages.ask("Participant ID")
    participant.create_datafile()
  
    screen.fill(settings.bg_color)
    pygame.display.flip()

    settings.nr_balloons = 4
    demo_game = Games(screen, settings, is_demo=True)
    demo_game.run_game()

    highscore.display_highscore(nickname=participant.nickname)

    screen.fill(settings.bg_black_color)
    pygame.display.flip()

    participant.nickname = messages.ask("Name")

    screen.fill(settings.bg_color)
    pygame.display.flip()
   
    settings.nr_balloons = 30
    main_game = Games(screen, settings, is_demo=False, datafile=participant.datafile, participant=participant.id)
    main_game.run_game()

    highscore.display_highscore(nickname = participant.nickname)
    
    pygame.display.quit() 
    pygame.quit()

Bart_Run()
