#Game "To The Abyss" developped by Clément Chaix in December 2019

import pygame as pg

from setting import *
import sprites
from os import path

class Game(object):
    def __init__(self):
        #Initialize Pygame
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()

    def load_data(self):
        #load window icon
        icon = pg.image.load(ICON)
        pg.display.set_icon(icon)
        #load highscore
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), "w") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #load sounds
        self.collision_sound = pg.mixer.Sound(DROP)
        self.collision_sound.set_volume(0.3)
        self.game_over_sound = pg.mixer.Sound(CRASH)
        self.game_over_sound.set_volume(0.1)
        #load theme music
        pg.mixer.music.load(THEME)

    def new(self):
        #Create a new game
        self.score = 0
        self.boost = 0
        self.ground_tempo = 0
        self.ground_count = 0
        self.collide = False

            #Creation of player
        self.characters = pg.sprite.Group()
        self.man = sprites.Player()
        self.characters.add(self.man)
            #Creation of ceil
        self.platforms = pg.sprite.Group()
        ceil = sprites.Platform(0, SPREAD, WIDTH)
        self.platforms.add(ceil)
            #Customize creation of first floor (to avoid hole below player at the beginning)
        p1left = sprites.Platform(0, self.platforms.sprites()[-1].rect.y + SPREAD, WIDTH / 2)
        p1right = sprites.Platform(WIDTH / 2 + HOLE_SIZE, self.platforms.sprites()[-1].rect.y + SPREAD, WIDTH / 2 - HOLE_SIZE)
        self.platforms.add(p1left, p1right)
            #Creation of 5 next floors
        for i in range(1, 6):
            self.create_floor()

        self.render()

    def run(self):
        #Game loop - Main
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.2)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.render()
        pg.mixer.music.fadeout(200)

    def events(self):
        #Game loop - 1/Events

        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

        #delete platforms above the window
        for platform in self.platforms:
            if platform.rect.bottom < 0:
                platform.kill()
                self.ground_tempo += 1
                self.ground_count += 1

        #create platforms below the screen accordingly
        if self.ground_tempo == 1:
            self.create_floor()
            self.ground_tempo = -1
            self.score += 1
            #increasing boost with time
            for i in range(1, 9):
                if self.ground_count < 6 * i + 10:
                    self.boost += (2 / i) * BOOSTER
                    break

        #game over
        if self.man.rect.top < 0:
            self.playing = False
            self.game_over_sound.play()

    def update(self):
        #Game loop - 2/Update
        self.characters.update()
        self.platforms.update(self.boost)
        #Collision check
        hits = pg.sprite.spritecollide(self.man, self.platforms, False)
        if hits:
            if not self.man.rect.top > hits[0].rect.top:
                self.man.pos.y = hits[0].rect.top
                self.man.vel.y = 0
                if not self.collide:
                    self.collide = True
                    self.collision_sound.play()
        else:
            self.collide = False

    def render(self):
        #Game loop - 3/Render
        self.screen.fill(GREY)
        self.platforms.draw(self.screen)
        self.characters.draw(self.screen)
        self.draw_text(str(self.score), 30, DARKBLUE, WIDTH - 60, 30)
        pg.display.update()

    def show_start_screen(self):
        #Start screen
        self.draw_text("To The Abyss", 30, LIGHTBLUE, WIDTH / 2, 30)
        self.draw_text("You lose when you hit the top of the screen", 30, LIGHTBLUE, WIDTH / 2, 60)
        self.draw_text("Press right to start", 30, LIGHTBLUE, WIDTH / 2, 90)
        pg.display.update()

        waiting = True
        while waiting:
            for event in pg.event.get():
                #check for closing window
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False

            k = pg.key.get_pressed()

            if k[pg.K_RIGHT]:
                waiting = False

    def show_end_screen(self):
        #Game over/continue
        if not self.running:
            return
        self.screen.fill(GREY)
        self.draw_text("You lose", 70, DARKBROWN, WIDTH / 2, HEIGHT / 2 - 120)
        self.draw_text("Press space to replay", 30, DARKBROWN, WIDTH / 2, HEIGHT / 2 - 50)
        self.draw_text("Your score is : " + str(self.score), 40, DARKBROWN, WIDTH / 2, HEIGHT / 2 + 40)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("New highscore!", 40, LIGHTBLUE, WIDTH / 2, HEIGHT / 2 + 90)
            with open(path.join(self.dir, HS_FILE), "w") as f:
                f.write(str(self.score))
        else:
            self.draw_text("Highscore : " + str(self.highscore), 40, DARKBROWN, WIDTH / 2, HEIGHT / 2 + 90)
        self.draw_text("Created by Clement Chaix", 20, LIGHTBROWN, WIDTH / 2, HEIGHT - 30)
        pg.display.update()

        waiting = True
        while waiting:
            for event in pg.event.get():
                #check  for closing window
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False

            k = pg.key.get_pressed()

            if k[pg.K_SPACE]:
                waiting = False
                g.new()
                g.show_start_screen()

    def create_floor(self):
        p = sprites.Platform(0, self.platforms.sprites()[-1].rect.y + SPREAD, WIDTH)
        pleft, pright = p.divide()
        p.kill()
        self.platforms.add(pleft, pright)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(FONT, size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.new()
g.show_start_screen()
while g.running:
    g.run()
    g.show_end_screen()

pg.quit()
