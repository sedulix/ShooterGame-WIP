import pygame
import sys


pygame.init()
pygame.display.set_caption("slider test")

SCREEN = pygame.display.set_mode((600, 300))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("assets/fonts/BoldPixels.ttf", 36)


# ----------------------- ArrowButton -----------------------


class ArrowButton:
    def __init__(self, x, y, size, direction="left", elevation=3):
        # CORE ATTRIBUTES
        self.x, self.y = x, y
        self.size = size
        self.direction = direction
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.pressed = False

        # BUTTONS ATTRIBUTES
        self.top_rect = pygame.Rect(x, y, size, size)
        self.original_y = y

        # BUTTON COLORS
        self.base_color = (255, 255, 255)
        self.top_rect_color = (255, 255, 255)
        self.press_color = (251, 208, 208)
        self.hover_color = (128, 0, 0)
        self.current_color = self.base_color


    # BUTTONS RENDERING


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


    # ARROWS DIRECTIONS


    def get_points(self, offset = 0):
        cx, cy = self.top_rect.centerx, self.top_rect.centery + offset
        s = self.size // 3 - 3
        if self.direction == "left":
            return [(cx + s, cy - s), (cx + s, cy + s), (cx - s, cy)]
        else:
            return [(cx - s, cy - s), (cx - s, cy + s), (cx + s, cy)]


    # BUTTON STATES + HOVER


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


# STEP_BAR CLASS


class StepBar:
    def __init__(self, x, y, steps = 7, start = 3):
        # CORE ATTRIBUTES
        self.x, self.y = x, y
        self.steps = steps
        self.current = start
        self.cell_size = 40
        self.spacing = 2

        self.width = self.steps * (self.cell_size + self.spacing) - self.spacing
        self.height = self.cell_size

        self.left_btn = ArrowButton(self.x - 45, self.y, 40, "left")
        self.right_btn = ArrowButton(self.x + self.width + 5, self.y, 40, "right")


    # BUTTONS RENDERING


    def draw(self, surface):
        # container_rect = pygame.Rect(self.x - 5, self.y - 5, self.width + 10, self.height + 10)
        # pygame.draw.rect(surface, (0, 0, 0), container_rect, width = 3)

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

        value_text = FONT.render(f"Volume: {self.current + 1}", True, (0, 0, 0))
        surface.blit(value_text, (self.x + self.width // 5.8 - value_text.get_width() // 2, self.y - 30))


# MAIN LOOP
step_bar = StepBar(100, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    SCREEN.fill("#FFFFFF")
    step_bar.draw(SCREEN)

    pygame.display.flip()
    CLOCK.tick(60)

