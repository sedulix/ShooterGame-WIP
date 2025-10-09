from config_handler import Config
import pygame.image


class Rocket:
    def __init__(self, config: Config, ship_x, ship_y, ship_width):
        self.config = config
        self.image = pygame.image.load("assets/rockets/rocket.png")
        self.width, self.height = 50, 50
        self.x = ship_x + ship_width / 2 - self.width / 2
        self.y = ship_y - self.height
        self.step = self.config.rocket_step


    def update_position(self):
        self.y -= self.step


    def is_out_of_screen(self):
        return self.y + self.height < 0


    def is_collision(self, skull):
        return (
            skull.x < self.x < skull.x + skull.width - self.width and
            skull.y < self.y < skull.y + skull.height - self.height
        )
