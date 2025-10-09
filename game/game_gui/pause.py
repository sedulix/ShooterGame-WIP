import pygame

from config_handler import (
    UI_FONT_PATH, PAUSE_ICO_PATH, SETTINGS_ICO_PATH, MENU_ICO_PATH,
    Config,
)
from game.game_gui import Button


class PauseMenu:
    def __init__(self, config: Config, screen):
        # CORE ATTRIBUTES
        self.config = config
        self.screen = screen
        self.gui_font = pygame.font.Font(UI_FONT_PATH, 40)
        self.overlay = pygame.Surface((self.config.screen_width, self.config.screen_height), pygame.SRCALPHA)

        # ICONS PATHS
        settings_img = pygame.image.load(SETTINGS_ICO_PATH).convert_alpha()
        resume_img = pygame.image.load(PAUSE_ICO_PATH).convert_alpha()
        menu_img = pygame.image.load(MENU_ICO_PATH).convert_alpha()

        # PAUSE MENU BUTTONS
        gap = 50
        total_width = 120 * 3 + gap * 2
        start_x = self.config.screen_width // 2 - total_width // 2

        self.setting_button = Button(settings_img, 120, 120,
                                     (start_x, self.config.screen_height // 2.40), 5, None,
                                     self.screen, is_image = True
        )
        self.resume_button = Button(resume_img, 180, 180,(start_x + 90 + gap,
                                    self.config.screen_height // 2.67), 5,None, self.screen,
                                    is_image = True
        )
        self.menu_button = Button(menu_img, 120, 120,
                                  (start_x + (120 + gap) * 2, self.config.screen_height // 2.40), 5,
                                  None, self.screen, is_image = True
        )


    # PAUSE MENU RENDERING


    def draw(self):
        self.overlay.fill((150, 150, 150, 5))
        self.screen.blit(self.overlay, (0, 0))

        pygame.draw.rect(self.screen, (220, 220, 220), (
            self.config.screen_width // 2 - 810 // 2,
            self.config.screen_height // 2 - 410 // 2, 810, 410), border_radius=50
        )
        pygame.draw.rect(self.screen, (10, 10, 10), (
            self.config.screen_width // 2 - 800 // 2,
            self.config.screen_height // 2 - 400 // 2 + 10, 800, 400), border_radius = 50
        )
        pygame.draw.rect(self.screen, (135, 135, 135), (
            self.config.screen_width // 2 - 800 // 2,
            self.config.screen_height // 2 - 400 // 2, 800, 400), border_radius = 50
        )

        pygame.draw.rect(self.screen, (255, 255, 255), (
            self.config.screen_width // 2 - 460 // 2,
            self.config.screen_height // 2 - 400 // 1.75, 460, 60), border_radius = 25
        )
        pause_rect = pygame.Rect(
            self.config.screen_width // 2 - 450 // 2,
            self.config.screen_height // 2 - 400 // 1.80, 450, 50
        )
        pygame.draw.rect(self.screen, (30, 30, 30), pause_rect, border_radius = 20)

        text = self.gui_font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center = pause_rect.center)
        self.screen.blit(text, text_rect)

        if self.resume_button.draw():
            return "RESUME"
        if self.setting_button.draw():
            return "SETTINGS"
        if self.menu_button.draw():
            return "MENU"

        pygame.display.flip()
        return None
