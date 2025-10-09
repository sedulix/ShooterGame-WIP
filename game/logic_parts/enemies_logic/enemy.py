from config_handler import Config
from random import randint
import pygame.image


class Enemy:
    def __init__(self, config: Config):
        self.config = config
        self.image = pygame.image.load("assets/enemies/enemy.png")
        self.width, self.height = 80, 80
        self.x, self.y = randint(0, self.config.screen_width - self.width), 0
        self.step = self.config.enemy_step
        self.speed = self.step


    def update_position(self):
        self.y += self.speed


    def increase_speed(self):
        self.speed += self.step / 6


    def reset(self):
        self.increase_speed()
        self.x, self.y = randint(0, self.config.screen_width - self.width), 0


    def is_reached_ship(self, ship):
        return self.y + self.height > ship.y

