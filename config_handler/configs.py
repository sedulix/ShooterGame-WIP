import json
import os


# PATHS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# FONTS
UI_FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "BoldPixels.ttf")
BIG_FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "ka1.ttf")

# GUI IMAGES
PAUSE_ICO_PATH = os.path.join(BASE_DIR, "assets", "gui_stuff", "pause_ico.png")
SETTINGS_ICO_PATH = os.path.join(BASE_DIR, "assets", "gui_stuff", "settings_ico.png")
MENU_ICO_PATH = os.path.join(BASE_DIR, "assets", "gui_stuff", "menu_ico.png")
RETRY_ICO_PATH = os.path.join(BASE_DIR, "assets", "gui_stuff", "retry_ico.png")
LEAVE_ICO_PATH = os.path.join(BASE_DIR, "assets", "gui_stuff", "leave_ico.png")


# DEFAULT CONFIGS VALUES --------------------------------------------------------------------------------------------<<<
CONFIG_FILE = "config_handler/config_handler.json"

DEFAULT_CONFIGS = {
    "SCREEN_WIDTH": 1500,
    "SCREEN_HEIGHT": 700,
    "SHIP_STEP": 0.6,
    "DEFAULT_VOLUME": 0.5,

    "SCREEN_COLOR": [255, 255, 255],
    "GAME_CAPTION": "SHOOTER GAME",
    "ROCKET_STEP": 0.4,
    "ENEMY_STEP": 0.1
}


class Config:
    def __init__(self, filepath=CONFIG_FILE):
        self.filepath = filepath
        self._configs = self.load()


    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as t:
                return json.load(t)
        return DEFAULT_CONFIGS.copy()


    def save(self):
        with open(self.filepath, "w") as t:
            json.dump(self._configs, t, indent=4)


    def get(self, key, default = None):
        return self._configs.get(key, default)


    def set(self, key, value):
        self._configs[key] = value


    # PROPERTIES TO CHANGE


    @property
    def game_caption(self):
        return self._configs["GAME_CAPTION"]


    @property
    def screen_color(self):
        return self._configs["SCREEN_COLOR"]


    @property
    def screen_width(self):
        return self._configs["SCREEN_WIDTH"]


    @property
    def screen_height(self):
        return self._configs["SCREEN_HEIGHT"]


    @property
    def default_volume(self):
        return self._configs["DEFAULT_VOLUME"]


    @property
    def default_ship_step(self):
        return self._configs["SHIP_STEP"]


    @property
    def rocket_step(self):
        return self._configs["ROCKET_STEP"]


    @property
    def enemy_step(self):
        return self._configs["ENEMY_STEP"]


    # FOR CHANGE VALUES


    @default_volume.setter
    def default_volume(self, value):
        self._configs["DEFAULT_VOLUME"] = value


    @default_ship_step.setter
    def default_ship_step(self, value):
        self._configs["SHIP_STEP"] = value

