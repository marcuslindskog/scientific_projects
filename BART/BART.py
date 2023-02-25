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

    # main event loop
    demo_game = Games(screen, settings)
    demo_game.run_demo_game()

    nickname = ""
    display_highscore(screen, nickname)

    screen.fill(settings.bg_black_color)
    pygame.display.flip()

    nickname = ask(screen, "Name")

    screen.fill(settings.bg_color)
    pygame.display.flip()

    run_game(screen, settings, datafile, participant)

    display_highscore(screen, nickname)
    
    pygame.display.quit() 
    pygame.quit()


def run_game(screen, settings, datafile, participant):
    with open('input/BART_Input.csv', 'rU') as f:
        reader = csv.reader(f)
        time_to_blow_all = list(reader)

    settings.nr_balloons = len(time_to_blow_all)
    balloons = [Balloon(screen)]
    boom = Boom(screen)
    scoreboard = Scoreboard(screen, settings)
    playing_game = True
    new_balloon = False
    boom_ballon = False
    stars = []
    new_balloon_button = Button(screen, settings.screen_width/2-settings.button_width/2,
                               settings.screen_height/2+125-settings.button_height/2, settings, "New Balloon")

    end_button = Button(screen, settings.screen_width / 2 - settings.button_width / 2,
                                 settings.screen_height / 2 + 125 - settings.button_height / 2, settings, "Game Finished")

    ballon_number = 0
    time_to_blow = list(map(int, time_to_blow_all[ballon_number]))
    n=0
    while playing_game:
        mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

        # Redraw the empty screen before redrawing any game objects
        screen.fill(settings.bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if balloons[0].rect.collidepoint(mouse_x, mouse_y):
                        n += 1
                        stars.append(Star(screen, settings, n))
                        for balloon in balloons:
                            balloon.update(settings.balloon_scale)
                            if time_to_blow[n] == 1:
                                balloons.remove(balloon)
                                scoreboard.update_nrstars(0)
                                new_balloon = True
                                boom_ballon = True
                    else:
                        for star in stars:
                            if star.rect.collidepoint(mouse_x, mouse_y):
                                balloons.remove(balloon)
                                scoreboard.update_nrstars(n)
                                new_balloon = True

        if new_balloon and scoreboard.nr_balloons > 1:
            # Save data to file
            with open(datafile, 'a') as f:
                if boom_ballon:
                    f.write(participant + settings.delim + str(1+ settings.nr_balloons - scoreboard.nr_balloons) +
                             settings.delim + "1" + settings.delim + str(time_to_blow.index(1)) + settings.delim +
                            str(n) + settings.delim  + str(0) + settings.delim + str(scoreboard.nr_stars)
                            + '\n')
                else:
                    f.write(participant + settings.delim + str(1+ settings.nr_balloons - scoreboard.nr_balloons) +
                             settings.delim + "0" + settings.delim + str(time_to_blow.index(1)) + settings.delim +
                            str(n) + settings.delim  + str(n) + settings.delim + str(scoreboard.nr_stars)
                            + '\n')

            balloons = [Balloon(screen)]
            new_balloon = False
            n = 0
            waiting = True
            if boom_ballon:
                boom.blitme()
                boom_ballon = False
            scoreboard.blitme()
            new_balloon_button.blitme()
            ballon_number += 1
            time_to_blow = list(map(int, time_to_blow_all[ballon_number]))
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
                            scoreboard.update_nrballons()

        elif new_balloon and scoreboard.nr_balloons == 1:
            # Save data to file
            with open(datafile, 'a') as f:
                if boom_ballon:
                    f.write(participant + settings.delim + str(1 + settings.nr_balloons - scoreboard.nr_balloons) +
                            settings.delim + "1" + settings.delim + str(time_to_blow.index(1)) + settings.delim +
                            str(n) + settings.delim + str(0) + settings.delim + str(scoreboard.nr_stars)
                            + '\n')
                else:
                    f.write(participant + settings.delim + str(1 + settings.nr_balloons - scoreboard.nr_balloons) +
                            settings.delim + "0" + settings.delim + str(time_to_blow.index(1)) + settings.delim +
                            str(n) + settings.delim + str(n) + settings.delim + str(scoreboard.nr_stars)
                            + '\n')
            waiting = True
            scoreboard.update_nrballons()
            end_button.blitme()
            scoreboard.blitme()
            pygame.display.flip()
            while waiting:
                mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if end_button.rect.collidepoint(mouse_x, mouse_y):
                            waiting = False
                            return




        #redraw the screen, every pass through the event loop
        screen.fill(settings.bg_color)
        for balloon in balloons:
            balloon.blitme()
        scoreboard.blitme()
        for star in stars:
            star.blitme()
        pygame.display.flip()

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