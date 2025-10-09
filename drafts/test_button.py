import pygame, sys
from config_handler import UI_FONT_PATH

# GAME INITIALIZATION
pygame.init()


# DISPLAY CONFIGS
pygame.display.set_caption("button")
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
gui_font = pygame.font.Font(UI_FONT_PATH, 35)


class Button:
    def __init__(self, text, width, height, pos, elevation):
        # CORE ATTRIBUTES
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

        self.text_surf = gui_font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)


    # BUTTON RENDERING


    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=10)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=10)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()


    # BUTTON STATE + HOVER EFFECT


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

        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#000000"


button_1 = Button("Click", 200, 40, (200, 250), 5)

# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("#FFFACD")
    button_1.draw()

    pygame.display.update()
    clock.tick(60)

