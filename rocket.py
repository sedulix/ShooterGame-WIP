from constants import ROCKET_STEP
import pygame.image


class Rocket:
    def __init__(self, ship):
        self.image = pygame.image.load("resources/rocket.png")
        self.width, self.height = 50, 50
        self.x, self.y = 0, 0
        self.step = ROCKET_STEP
        self.was_fired = False
        self.ship = ship

    def fire(self):
        self.was_fired = True
        self.x = self.ship.x + self.ship.width / 2 - self.width / 2
        self.y = self.ship.y - self.height

    def update_position(self):
        if self.was_fired:
            self.y -= self.step

    def is_out_of_screen(self):
        return self.y + self.height < 0

    def reset(self):
        self.was_fired = False

    def is_collision(self, skull):
        return (
            skull.x < self.x < skull.x + skull.width - self.width and
            skull.y < self.y < skull.y + skull.height - self.height
        )
