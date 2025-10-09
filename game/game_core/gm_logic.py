import pygame
import time
import sys

from config_handler import Config, UI_FONT_PATH
from game import Rocket
from game import Enemy
from game import Ship
from game import SoundManager, PauseMenu, Settings, Retry


class Game:
    def __init__(self, config: Config, screen):
        # CORE ATTRIBUTES
        self.config = config
        self.screen_width, self.screen_height = self.config.screen_width, self.config.screen_height
        self.screen_fill_color = self.config.screen_color
        self.screen = screen
        self.game_font = pygame.font.Font(UI_FONT_PATH, 40)

        # GAME SCORE
        self.game_score = 0

        # SHIP AND ENEMY OBJECTS
        self.ship = Ship(config)
        self.enemy = Enemy(config)

        # ROCKET OBJECT
        self.rockets = []
        self.last_rocket_time = 0
        self.rocket_cooldown = 250

        # SOUNDS OBJECT
        self.sound_manager = SoundManager(config)

        # GAME STATE
        self.game_is_running = True
        self.paused = False


    # START THE GAME


    def run(self):
        pause_menu = None

        while self.game_is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # CATCHING EVENTS
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    if self.paused:
                        pause_menu = PauseMenu(self.config, self.screen)

                if not self.paused:
                    self.handle_key_events(event)

            # PAUSE MENU LOGIC
            if self.paused:
                action = pause_menu.draw()
                if action == "RESUME":
                    self.paused = False

                elif action == "SETTINGS":
                    settings = Settings(self.config, self.sound_manager, self.screen)
                    back = settings.run()

                    if back == "BACK":
                        self.config.save()
                        self.screen.fill((0, 0, 0))
                        pause_menu = PauseMenu(self.config, self.screen)
                        continue

                elif action == "MENU":
                    return "MENU"

            else:
                self.update_game_state()
                self.draw_screen()

        self.show_game_over()
        retry_screen = Retry(self.config, self.screen)

        # GAME RESTARTING LOGIC
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            action = retry_screen.draw()
            if action == "RETRY":
                self.__init__(self.config, self.screen)
                self.countdown(2)
                return self.run()

            elif action == "MENU":
                return "MENU"


    # STARTING GAME COUNTDOWN


    def countdown(self, seconds=2):
        for i in range(seconds, 0, -1):
            self.screen.fill((255, 255, 255))
            text = self.game_font.render(str(i), True, (0, 0, 0))
            self.screen.blit(text, (self.config.screen_width // 2 - text.get_width() // 2,
                                    self.config.screen_height // 2 - text.get_height() // 2)
            )
            pygame.display.flip()
            time.sleep(1)

        self.screen.fill((255, 255, 255))
        text = self.game_font.render("GO!", True, (0, 0, 0))
        self.screen.blit(text, (self.config.screen_width // 2 - text.get_width() // 2,
                                self.config.screen_height // 2 - text.get_height() // 2)
        )
        pygame.display.flip()
        time.sleep(1)


    # PLAYER CONTROLLER + ATTACK (DEFAULT ROCKET ATTACK)


    def handle_key_events(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.ship.move_left()

            if event.key == pygame.K_RIGHT:
                self.ship.move_right()

            if event.key == pygame.K_UP:
                self.ship.move_up()

            if event.key == pygame.K_DOWN:
                self.ship.move_down()

            if event.key == pygame.K_SPACE:
                current_time = pygame.time.get_ticks()

                if current_time - self.last_rocket_time >= self.rocket_cooldown:
                    new_rocket = Rocket(self.config, self.ship.x, self.ship.y, self.ship.width)
                    self.rockets.append(new_rocket)
                    self.last_rocket_time = current_time
                    self.sound_manager.play("fire")

        if event.type == pygame.KEYUP:
            self.ship.stop_moving(event.key)


    # UPDATING GAME STATES + (FOR FIRST ENEMY)


    def update_game_state(self):
        self.ship.update_position()
        self.enemy.update_position()

        for rocket in self.rockets[:]:
            rocket.update_position()

            if rocket.is_out_of_screen():
                self.rockets.remove(rocket)
                continue

            if rocket.is_collision(self.enemy):
                self.rockets.remove(rocket)
                self.enemy.reset()
                self.sound_manager.play("explosion")
                self.game_score += 5000

        if self.enemy.is_reached_ship(self.ship):
            self.game_is_running = False


    # GAME SCREEN RENDERING


    def draw_screen(self):
        self.screen.fill(self.config.screen_color)
        self.screen.blit(self.ship.image, (self.ship.x, self.ship.y))
        self.screen.blit(self.enemy.image, (self.enemy.x, self.enemy.y))

        for rocket in self.rockets:
            self.screen.blit(rocket.image, (rocket.x, rocket.y))

        self.show_game_score()
        pygame.display.update()


    # GAME SCORE


    def show_game_score(self):
        dev_score_text = self.game_font.render(f"Dev's highest score is: 190000", True, (0, 0, 0))
        game_score_text = self.game_font.render(f"Your score is: {self.game_score}", True, (0, 0, 0))
        self.screen.blit(dev_score_text, (20, 20))
        self.screen.blit(game_score_text, (20, 60))


    # GAME OVER EVENT


    def show_game_over(self):
        game_over_text = self.game_font.render("GAME OVER", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (self.config.screen_width / 2, self.config.screen_height / 2)
        self.screen.blit(game_over_text, game_over_rect)
        self.sound_manager.play("game_over")
        
        pygame.display.update()
        pygame.time.wait(2500)

