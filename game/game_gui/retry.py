import pygame

from config_handler import Config, RETRY_ICO_PATH, LEAVE_ICO_PATH, UI_FONT_PATH
from game.game_gui import Button


pygame.init()


class Retry:
    def __init__(self, config: Config, screen, ):
        # CORE ATTRIBUTES
        self.config = config
        self.screen = screen

        # FONT
        self.ui_font = pygame.font.Font(UI_FONT_PATH, 40)

        # BUTTONS
        retry_img = pygame.image.load(RETRY_ICO_PATH).convert_alpha()
        leave_img = pygame.image.load(LEAVE_ICO_PATH).convert_alpha()

        self.retry_button = Button(retry_img, 40, 40,
                                   (self.config.screen_width // 2.04 - 40, self.config.screen_height // 1.85),
                                   5,None, self.screen, is_image = True
        )
        self.leave_button = Button(leave_img, 40, 40,
                                   (self.config.screen_width // 2.07 + 29, self.config.screen_height // 1.85),
                                   5,None, self.screen, is_image = True
        )


    # RETRY BUTTONS RENDERING


    def draw(self):
        self.screen.fill((255, 255, 255))

        retry_text = self.ui_font.render("RETRY?", True, (0, 0, 0))
        retry_text_rect = retry_text.get_rect()
        retry_text_rect.center = (self.config.screen_width / 2, self.config.screen_height / 2)
        self.screen.blit(retry_text, retry_text_rect)

        if self.retry_button.draw():
            pygame.display.flip()
            pygame.time.wait(150)
            return "RETRY"

        elif self.leave_button.draw():
            pygame.display.flip()
            pygame.time.wait(150)
            return "MENU"

        pygame.display.flip()
        return None

