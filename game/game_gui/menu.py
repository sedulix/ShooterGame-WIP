import sys
import pygame

from config_handler import Config


# ------> BUTTONS ANIMATION <------


class Button:
    def __init__(self, content, width, height, pos, elevation, gui_font, screen, is_image = False):
        # CORE ATTRIBUTES
        self.screen = screen
        self.clicked = False
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # TOP RECT
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = "#000000"

        # BOTTOM RECT
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = "#4b251c"

        if is_image:
            self.content_surf = content
        else:
            self.content_surf = gui_font.render(content, True, "#FFFFFF")

        self.content_rect = self.content_surf.get_rect(center = self.top_rect.center)


    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.content_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=10)
        self.screen.blit(self.content_surf, self.content_rect)

        return self.check_click()


    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "#800000"

            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True

            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
                    self.clicked = True

        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#000000"

        return self.clicked


# MENU THING


class Menu:
    def __init__(self, config: Config, screen):
        self.config = config
        self.screen = screen
        self.title_font = pygame.font.Font("assets/fonts/ka1.ttf", 55)
        self.ui_font = pygame.font.Font("assets/fonts/BoldPixels.ttf", 48)

        self.play_button = Button("PLAY", 250, 50,
                                  (self.config.screen_width // 2 - 125, self.config.screen_height // 2 - 65),
                                  5, self.ui_font, screen
        )
        self.settings_button = Button("SETTINGS", 250, 50,
                                      (self.config.screen_width // 2.068 - 100, self.config.screen_height // 2),
                                      5, self.ui_font, screen
        )
        self.quit_button = Button("QUIT", 250, 50,
                                  (self.config.screen_width // 2.068 - 100, self.config.screen_height // 2 + 65),
                                  5, self.ui_font, screen
        )


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            self.screen.fill((255, 255, 255))

            title = self.title_font.render("ENEMY SHOTER", True, (0, 0, 0))
            self.screen.blit(title, (self.config.screen_width // 2 - title.get_width() // 2,
                                     self.config.screen_height // 4))

            if self.play_button.draw():
                return "PLAY"

            if self.settings_button.draw():
                return "SETTINGS"

            if self.quit_button.draw():
                pygame.quit()
                sys.exit()

            pygame.display.flip()


