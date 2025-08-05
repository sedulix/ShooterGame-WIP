import pygame

from sounds_config import SOUND_FILES, DEFAULT_VOLUME


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.volume = DEFAULT_VOLUME
        self.load_sound()


    def load_sound(self):
        for name, path in SOUND_FILES.items():
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.volume)
            self.sounds[name] = sound


    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()


    def set_volume(self, volume):
        self.volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)


    def stop_sound(self):
        for sound in self.sounds.values():
            sound.stop()


