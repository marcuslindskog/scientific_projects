import pygame, sys, random, pygame.font, pygame.event, pygame.draw, string, datetime, csv
from pygame.locals import *

from settings.Settings import Settings

from components.Balloon import Balloon
from components.Scoreboard import Scoreboard
from components.Button import Button
from components.Boom import Boom
from components.Star import Star

from components.Games import Games

def Bart_Run():
    settings = Settings()
    # initialize game
    pygame.init()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Balloon Hunt")

    participant = ask(screen, "Participant ID")
    datafile = 'data/BART_' + participant + '_' + datetime.datetime.now().strftime("%Y%m%d") + ".txt"
    with open(datafile, 'a') as f:
        f.write('ID; Balloon; Boom; Boom_limit; Presses; Stars; Tot_Stars' + '\n')


    screen.fill(settings.bg_color)
    pygame.display.flip()

    demo_button = Button(screen, settings.screen_width / 2 - settings.button_width / 2,
                        settings.screen_height / 2 + 125 - settings.button_height / 2, settings, "Start Demo")

    demo_button.blitme()

    pygame.display.flip()
    waiting = True
    while waiting:
        mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if demo_button.rect.collidepoint(mouse_x, mouse_y):
                    waiting = False

    with open('input/demo_input.csv', 'r') as f:
        reader = csv.reader(f)
        times_to_blow = list(reader) 

    settings.nr_balloons = 4

    demo_game = Games(screen, settings, is_demo=True, times_to_blow=times_to_blow)
    demo_game.run_game()

    nickname = ""
    display_highscore(screen, nickname)

    screen.fill(settings.bg_black_color)
    pygame.display.flip()

    nickname = ask(screen, "Name")

    screen.fill(settings.bg_color)
    pygame.display.flip()

    with open('input/main_game_input.csv', 'r') as f:
        reader = csv.reader(f)
        times_to_blow = list(reader) 

    settings.nr_balloons = len(times_to_blow)
    main_game = Games(screen, settings, is_demo=False, times_to_blow=times_to_blow, datafile=datafile, participant=participant)
    main_game.run_game()

    display_highscore(screen, nickname)
    
    pygame.display.quit() 
    pygame.quit()

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  fontobject = pygame.font.Font(None,32)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,40), 0)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,44), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + "".join(current_string))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")    
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + "".join(current_string))
  return "".join(current_string)


def display_highscore(screen, nickname):
    pygame.font.init()
    fontobject = pygame.font.Font(None, 32)
    bx = 800 # x-size of box
    by = 600  # y-size of box
    GREEN = (51, 255, 51)
    WHITE = (255, 255,255)
    BLACK = (0,0,0)

    participants = ['hkh', 'big', 'col', 'aaa', 'mlp']
    if len(nickname) > 0:
        pos = random.randint(0, 4)
        print (pos)
        participants.insert(pos, nickname)

    ranks = ['1:st', '2:nd', '3:rd', '4:th', '5:th']

    all_score=[]
    for line in range(0,5):
        name = participants[line]
        rank = ranks[line]
        all_score.append((rank, name))

    best = all_score[:5]

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
    for i, entry in enumerate(best):
        if str(entry[1]) == nickname:
            color_to_use = GREEN
        else:
            color_to_use = WHITE

        txt_surf = fontobject.render(entry[0] + "      " + str(entry[1]), True, color_to_use)
        txt_rect = txt_surf.get_rect(center=(bx // 2, 30 * i + 120))
        box.blit(txt_surf, txt_rect)

    screen.blit(box, (0, 0))
    pygame.display.flip()

    while True:  # wait for user to acknowledge and return
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                return
        pygame.time.wait(20)


Bart_Run()