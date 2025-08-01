from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SHIP_STEP
import pygame.image


class Ship:
    def __init__(self):
        self.image = pygame.image.load("space_ships/space_ship.png")
        self.width, self.height = self.image.get_size()
        self.x, self.y = SCREEN_WIDTH / 2 - self.width / 2, SCREEN_HEIGHT - self.height
        self.max_up_y = SCREEN_HEIGHT - self.height - 100
        self.is_moving_right, self.is_moving_left, self.is_moving_up, self.is_moving_down = False, False, False, False
        self.step = SHIP_STEP
        self.speed = self.step


    def move_left(self):
        self.is_moving_left = True


    def move_right(self):
        self.is_moving_right = True


    def move_up(self):
        self.is_moving_up = True


    def move_down(self):
        self.is_moving_down = True


    def stop_moving(self, key):
        if key == pygame.K_UP:
            self.is_moving_up = False
        elif key == pygame.K_DOWN:
            self.is_moving_down = False
        elif key == pygame.K_LEFT:
            self.is_moving_left = False
        elif key == pygame.K_RIGHT:
            self.is_moving_right = False


    def update_position(self):
        if self.is_moving_left and self.x >= self.step:
            self.x -= self.step

        if self.is_moving_right and self.x <= SCREEN_WIDTH - self.width - self.step:
            self.x += self.step

        if self.is_moving_up and self.y > self.max_up_y:
            self.y -= self.step

        if self.is_moving_down and self.y < SCREEN_HEIGHT - self.height - self.step:
            self.y += self.step

