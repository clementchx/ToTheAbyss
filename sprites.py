import pygame as pg
vec = pg.math.Vector2
import random

from setting import *

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(PLAYER_SIZE)
        self.image.fill(DARKBLUE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = PLAYER_START
        self.pos = vec(self.rect.midbottom)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, GRAVITY)

        #processing input
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x += -ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acc.x += ACCELERATION
        #apply friction
        self.acc.x += self.vel.x * FRICTION
        #equations of movement
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #boundaries
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT

        #apply new position
        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, THICKNESS))
        self.image.fill(DARKBROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, boost):
        #make platforms going up
        self.rect.y -= SPEED + boost

    def divide(self):
        #take one platform and create two children platform with a random division point
        hole_left = random.randint(20, WIDTH - 20 - HOLE_SIZE)
        hole_right = hole_left + HOLE_SIZE
        left = Platform(0, self.rect.y, hole_left)
        right = Platform(hole_right, self.rect.y, WIDTH - hole_right)
        return left, right
