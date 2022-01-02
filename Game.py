import sys

import pygame
import os  # to define path to the images

from Superspreader import Superspreader
from settings import *
from Runner import Runner  # from filename import className
from Virus import Virus  # from filename import className
from Health import Health1, Health2, Health3

FPS = 60
FramePerSec = pygame.time.Clock()


class Game:
    def __init__(self):  # initialize game window etc
        self.game_over = None
        pygame.init()
        pygame.mixer.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # make new window of defined width & height
        pygame.display.set_caption(TITLE)  # window title
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = True
        self.pause = False
        self.click = False
        # self.jumping = False  # ist jetzt in Klasse Runner
        self.all_sprites = pygame.sprite.Group()  # creates new empty group for all sprites
        self.virus_group = pygame.sprite.Group()

        # create runner and add it to sprites group
        self.runner = Runner()
        self.all_sprites.add(self.runner)

        # all about virus creation
        self.frame_counter = 0  # use for intervals when producing new virus
        self.virus_counter = 0  # TODO: maybe use later to increase virusproduction
        self.virus_frequency = 120
        self.superspreader = Superspreader()

        # count collision -> virus
        self.collision_virus = 0

        # create hearts and add them to sprites group
        self.health1 = None
        self.health2 = None
        self.health3 = None

    def new(self):  # start a new game
        # initialize health
        self.health1 = Health1()
        self.health2 = Health2()
        self.health3 = Health3()
        self.all_sprites.add(self.health1)
        self.all_sprites.add(self.health2)
        self.all_sprites.add(self.health3)

        # set counters to 0 (important when restarting the game)
        self.virus_counter = 0
        self.collision_virus = 0

        self.running = True
        self.playing = True

        # run the game
        self.run()

    def run(self):  # code that handles main game loop in pygame
        while self.playing:  # game loop: open & close the window
            self.clock.tick(FPS)  # controls speed of the while loop
            self.events()
            self.update()
            self.draw()

    def update(self):  # game loop - update
        # virus sprite production depending on number of frames passed
        if self.frame_counter % self.virus_frequency == 0:
            virus = self.superspreader.produce_virus(7)  # produce virus with velocity 7
            self.all_sprites.add(virus)  # add virus to sprites group
            self.virus_group.add(virus)
            self.frame_counter = 0
            self.virus_counter += 1
        self.all_sprites.update()
        pygame.display.update()  # update changes
        self.frame_counter += 1  # necessary for virus sprite production

    def events(self):  # game loop - events
        self.game_over = False
        for event in pygame.event.get():  # loop through list of all different events
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False  # end while loop if user quits game (press x)
                self.running = False
                pygame.quit()   # TODO: quit game properly?
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
            # if self.jumping is False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #    self.jumping = True
        user_input = pygame.key.get_pressed()  # list of currently pressed key(s)
        if self.runner.jumping is False and user_input[pygame.K_SPACE]:
            self.runner.jumping = True
        if self.runner.jumping:
            self.runner.jump()
        # pygame.time.delay(400)  # slows down everything!
        # detect collision
        self.check_collision_with_virus()

    def check_collision_with_virus(self):  # improve health decrease & collision detection
        if pygame.sprite.spritecollide(self.runner, self.virus_group,
                                       True):  # self.runner.rect.colliderect(self.virus):  # detect collisions of two rectangles
            self.collision_virus += 1
            print(self.collision_virus)
            if self.collision_virus == 1:
                pygame.sprite.Sprite.kill(self.health3)
            elif self.collision_virus == 2:
                pygame.sprite.Sprite.kill(self.health2)

            elif self.collision_virus == 3: #display_game_over hier aufrufen
                pygame.sprite.Sprite.kill(self.health1)
                print("you are  dead ")
                #self.playing = False
                s.display_game_over()
                # TODO: end the game when 3 viruses are collected --> Merve
                # bedingung für Aufruf der end seite --> bei 3 collision

    def draw(self):  # game loop - draw
        self.WIN.fill(WHITE)  # RGB color for the window background, defined as constant
        # coordinate system: (0,0) is top left

        # uncommented because included in all_sprites group:
        # self.WIN.blit(self.runner.image,
        #              (self.runner.rect.x, self.runner.rect.y))  # draw surface (pictures, text, ...) on the screen
        # self.WIN.blit(self.virus.image,
        #              (self.virus.rect.x, self.virus.rect.y))
        self.all_sprites.draw(self.WIN)
        mx, my = pygame.mouse.get_pos()
        stop_button = pygame.Rect(WIDTH - 2*MARGIN - SMALL_BUTTON_WIDTH, MARGIN, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT)
        pause_button = pygame.Rect(WIDTH - 2*MARGIN - SMALL_BUTTON_WIDTH, 2*MARGIN + SMALL_BUTTON_HEIGHT, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT)
        pygame.draw.rect(self.WIN, GREY, stop_button)
        pygame.draw.rect(self.WIN, GREY, pause_button)
        Menu.draw_text(self, "stop", pygame.font.Font(None, 50), BLACK, self.WIN, WIDTH - MARGIN - SMALL_BUTTON_WIDTH, 2*MARGIN)
        Menu.draw_text(self, "pause", pygame.font.Font(None, 50), BLACK, self.WIN, WIDTH - MARGIN - SMALL_BUTTON_WIDTH, 3*MARGIN + SMALL_BUTTON_HEIGHT)

        if stop_button.collidepoint(mx, my):
            if self.click:
                self.click = False
                # TODO: jump to start screen, virus should start on the right
                pass
                # s.display_main_menu()   # not correct yet, when pressing start the virus starts where you stopped the game, not at the beginning
        if pause_button.collidepoint(mx, my):
            if self.click:
                self.click = False
                self.pause = True
                # while self.pause:
                    # TODO: implement pause function, maybe with additional screen with continue button
                    # pygame.time.wait(500)   # wait 500 milliseconds

    def show_start_screen(self):  # game splash / start screen
        pass

    def show_go_screen(self):  # game over / continue
        pass


class Menu:
    def __init__(self):  # initialize game window etc
        pygame.init()
        pygame.mixer.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # make new window of defined width & height
        pygame.display.set_caption(TITLE_START)  # window title
        self.running = True
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 60)
        self.font_big = pygame.font.Font(None, 100)
        self.click = False

    def run(self):
        self.click = False
        pygame.display.update()
        self.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    def display_main_menu(self):
        while self.running:
            self.WIN.fill(WHITE)
            mx, my = pygame.mouse.get_pos()
            # create buttons
            start_button = pygame.Rect(WIDTH/2 - BUTTON_WIDTH/2, 180, BUTTON_WIDTH, BUTTON_HEIGHT)
            highscore_button = pygame.Rect(WIDTH/2 - BUTTON_WIDTH/2, 180 + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
            quit_button = pygame.Rect(WIDTH/2 - BUTTON_WIDTH/2, 180 + 2*MARGIN + 2*BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
            # display rectangles
            pygame.draw.rect(self.WIN, GREY, start_button)
            pygame.draw.rect(self.WIN, GREY, highscore_button)
            pygame.draw.rect(self.WIN, GREY, quit_button)
            # create circle button
            help_button = pygame.draw.circle(self.WIN, GREY, (WIDTH-2*MARGIN-RADIUS, 2*MARGIN+RADIUS), RADIUS) # surface, color, center, radius
            # display text
            self.draw_text("Corona Game", self.font_big, BLACK, self.WIN, 220, 80)
            self.draw_text("Play", self.font_small, BLACK, self.WIN, WIDTH/2 - BUTTON_WIDTH/2 + 2*MARGIN, 180+MARGIN)
            self.draw_text("High Score", self.font_small, BLACK, self.WIN, WIDTH/2 - BUTTON_WIDTH/2 + 2*MARGIN, 180 + 2*MARGIN + BUTTON_HEIGHT)
            self.draw_text("Quit", self.font_small, BLACK, self.WIN, WIDTH/2 - BUTTON_WIDTH/2 + 2*MARGIN, 180 + 3*MARGIN + 2*BUTTON_HEIGHT)
            self.draw_text("?", self.font_small, BLACK, self.WIN, help_button.x+MARGIN, help_button.y+MARGIN)
            # display pictures
            runner = pygame.transform.scale(pygame.image.load(os.path.join('assets', "runner.png")), (RUNNER_WIDTH*1.5, RUNNER_HEIGHT*1.5))
            small_virus = pygame.transform.scale(pygame.image.load(os.path.join('assets', "virus.png")), (VIRUS_WIDTH, VIRUS_HEIGHT))
            big_virus = pygame.transform.scale(pygame.image.load(os.path.join('assets', "virus.png")), (VIRUS_WIDTH*2, VIRUS_HEIGHT*2))
            self.WIN.blit(runner, (WIDTH-2*MARGIN-RUNNER_WIDTH*1.5, HEIGHT-2*MARGIN-RUNNER_HEIGHT*1.5))  # draw surface (pictures, text, ...) on the screen
            self.WIN.blit(small_virus, (50, 350))
            self.WIN.blit(big_virus, (150, 200))

            if start_button.collidepoint((mx, my)):
                if self.click:
                    self.click = False  # reset to avoid zombie runner (continues running when dead if mouse stays in the same position)
                    while g.running:
                        g.new()
            if quit_button.collidepoint(mx, my):
                if self.click:
                    pygame.quit()
                    sys.exit()
            if highscore_button.collidepoint(mx, my):
                if self.click:
                    # TODO: display highscores
                    pass
            if help_button.collidepoint(mx, my):
                if self.click:
                    # TODO: display help page
                    pass
            self.run()


    def display_game_over(self):
        virus_avoided = g.virus_counter-g.collision_virus
        while self.running:
            # initialize text and buttons
            self.WIN.fill(WHITE)
            mx, my = pygame.mouse.get_pos()
            play_again_button = pygame.Rect(180, 230, 250, 80)
            quit_button = pygame.Rect(470, 230, 130, 80)
            pygame.draw.rect(self.WIN, GREY, play_again_button)
            pygame.draw.rect(self.WIN, GREY, quit_button)
            self.draw_text("Ooops! You are dead :/", self.font_big, BLACK, self.WIN, 100, 100)
            self.draw_text("Play again", self.font_small, BLACK, self.WIN, 200, 250)
            self.draw_text("Quit", self.font_small, BLACK, self.WIN, 490, 250)

            if virus_avoided > 0:
                self.draw_text("The good news: " + str(virus_avoided) + " viruses avoided", self.font_small, BLACK, self.WIN,
                               150, 350)
            else:
                self.draw_text("Viruses avoided: " + str(virus_avoided), self.font_small, BLACK,
                               self.WIN, 230, 350)

            if play_again_button.collidepoint(mx, my):
                if self.click:
                    self.click = False  # reset to avoid zombie runner (continues running when dead if mouse stays in the same position)
                    g.new()  # run a new game

            if quit_button.collidepoint(mx, my):
                if self.click:
                    pygame.quit()
                    sys.exit()

            self.run()


g = Game()
s = Menu()
while s.running:
    s.display_main_menu()