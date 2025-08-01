from constants import SCREEN_WIDTH, SKULL_STEP
from random import randint
import pygame.image


class Skull:
    def __init__(self):
        self.image = pygame.image.load("enemies/enemy.png")
        self.width, self.height = 80, 80
        self.x, self.y = randint(0, SCREEN_WIDTH - self.width), 0
        self.step = SKULL_STEP
        self.speed = self.step


    def update_position(self):
        self.y += self.speed


    def increase_speed(self):
        self.speed += self.step / 6


    def reset(self):
        self.increase_speed()
        self.x, self.y = randint(0, SCREEN_WIDTH - self.width), 0


    def is_reached_ship(self, ship):
        return self.y + self.height > ship.y


