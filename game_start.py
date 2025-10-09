import pygame

from config_handler import Config
from game import (
    Menu, Game, Settings, SoundManager
)


def main():
    pygame.init()
    config = Config()
    sound = SoundManager(config)
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    pygame.display.set_caption(config.game_caption)

    while True:
        menu = Menu(config, screen)
        action = menu.run()

        if action == "PLAY":
            current_game = Game(config, screen)
            current_game.countdown(2)
            result = current_game.run()

            if result == "MENU":
                continue

            if result == "RETRY":
                continue

        elif action == "SETTINGS":
            settings = Settings(config, sound, screen)
            back = settings.run()

            if back == "BACK":
                config.save()

            screen = pygame.display.set_mode((config.screen_width, config.screen_height))
            pygame.display.set_caption(config.game_caption)


if __name__ == "__main__":
    main()
