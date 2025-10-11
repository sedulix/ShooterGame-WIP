import pygame
import sys

from config_handler import Config, UI_FONT_PATH
from game import SoundManager
from .menu import Button


pygame.init()
CLOCK = pygame.time.Clock()
FONT = pygame.font.Font(UI_FONT_PATH, 35)


# ARROW-LOOK BUTTONS 


class ArrowButton:
    def __init__(self, x, y, size, direction="left", elevation=3):
        self.x, self.y = x, y
        self.size = size
        self.direction = direction
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.pressed = False

        self.top_rect = pygame.Rect(x, y, size, size)
        self.original_y = y

        # COLORS
        self.base_color = (255, 255, 255)
        self.top_rect_color = (255, 255, 255)
        self.press_color = (251, 208, 208)
        self.hover_color = (128, 0, 0)
        self.current_color = self.base_color


    def draw(self, surface):
        self.top_rect.y = self.original_y - self.dynamic_elevation

        bg_rect = self.top_rect.copy()
        bg_rect.y = self.original_y
        pygame.draw.rect(surface, "#000000", bg_rect, border_radius=6)

        top_bg = self.top_rect.copy()
        pygame.draw.rect(surface, self.top_rect_color, top_bg, border_radius=6)
        pygame.draw.rect(surface, (0, 0, 0), top_bg, width=2, border_radius=6)

        top_points = self.get_points(offset=0)
        color = self.hover_color if self.top_rect.collidepoint(pygame.mouse.get_pos()) else (0, 0, 0)
        pygame.draw.polygon(surface, color, top_points)

        return self.check_click()


    def get_points(self, offset = 0):
        cx, cy = self.top_rect.centerx, self.top_rect.centery + offset
        s = self.size // 3 - 3
        if self.direction == "left":
            return [(cx + s, cy - s), (cx + s, cy + s), (cx - s, cy)]
        else:
            return [(cx - s, cy - s), (cx - s, cy + s), (cx + s, cy)]


    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
                self.top_rect_color = self.press_color

            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
                    self.top_rect_color = self.base_color
                    return True
                else:
                    self.top_rect_color = self.base_color

        else:
            self.dynamic_elevation = self.elevation
            self.current_color = self.base_color
        return False


# STEP BAR GUI 


class StepBar:
    def __init__(self, x, y, steps = 7, start = 3):
        self.x, self.y = x, y
        self.steps = steps
        self.current = start
        self.cell_size = 40
        self.spacing = 2


        self.width = self.steps * (self.cell_size + self.spacing) - self.spacing
        self.height = self.cell_size

        self.left_btn = ArrowButton(self.x - 45, self.y, 40, "left")
        self.right_btn = ArrowButton(self.x + self.width + 5, self.y, 40, "right")


    def draw(self, surface):
        for i in range(self.steps):
            rect = pygame.Rect(
                self.x + i * (self.cell_size + self.spacing),
                self.y,
                self.cell_size,
                self.cell_size
            )

            color = (0, 0, 0) if i == self.current else (255, 255, 255)
            pygame.draw.rect(surface, color, rect, border_radius = 5)

            border_color = (0, 0, 0)
            pygame.draw.rect(surface, border_color, rect, width = 3, border_radius = 5)

        if self.left_btn.draw(surface):
            self.current = max(0, self.current - 1)
        if self.right_btn.draw(surface):
            self.current = min(self.steps - 1, self.current + 1)

        return self.current


# MAIN LOOP


class Settings:
    def __init__(self, config: Config, sound_manager: SoundManager, screen,):
        self.config = config
        self.screen = screen
        self.sound_manager = sound_manager

        self.title = pygame.font.Font("assets/fonts/ka1.ttf", 45)
        self.ui_font = pygame.font.Font("assets/fonts/BoldPixels.ttf", 35)

        start_volume = round(self.config.default_volume * (8 - 1))
        self.volume_bar = StepBar(200, 200, steps = 8, start = start_volume)

        start_speed = round(self.config.default_ship_step * (8 - 1))
        self.ship_speed_bar = StepBar(200, 300, steps = 8, start = start_speed)

        self.back_button = Button("BACK", 250, 50,
                                  (self.config.screen_width // 2 - 125, self.config.screen_height // 2 + 200),
                                  5, self.ui_font, screen)

        self.last_volume = self.volume_bar.current
        self.last_ship_speed = self.ship_speed_bar.current

        self.apply_volume_live()


    def apply_volume_live(self):
        vol = self.volume_bar.current / (self.volume_bar.steps - 1)
        self.sound_manager.set_volume(vol)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))

            title = self.title.render("SETTINGS", True, (0, 0, 0))
            self.screen.blit(title, ((self.config.screen_width // 2 - title.get_width()) // 2, 80))


            volume_value = self.volume_bar.draw(self.screen)
            if volume_value != self.last_volume:
                self.last_volume = volume_value
                self.apply_volume_live()

            vol_label = self.ui_font.render(
                f"Volume: {self.last_volume / (self.volume_bar.steps - 1): .2f}", True, (0, 0, 0))
            self.screen.blit(vol_label, (self.volume_bar.x, self.volume_bar.y - 35))


            speed_value = self.ship_speed_bar.draw(self.screen)
            if speed_value != self.last_ship_speed:
                self.last_ship_speed = speed_value
                self.config.default_ship_step = speed_value / (self.ship_speed_bar.steps - 1)

            speed_label = self.ui_font.render(
                f"Ship speed: {self.config.default_ship_step: .2f}", True, (0, 0, 0))
            self.screen.blit(speed_label, (self.ship_speed_bar.x, self.ship_speed_bar.y - 35))


            if self.back_button.draw():
                self.config.default_volume = self.last_volume / (self.volume_bar.steps - 1)
                self.config.default_ship_step = self.last_ship_speed / (self.ship_speed_bar.steps - 1)
                self.config.save()
                return "BACK"

            pygame.display.flip()



