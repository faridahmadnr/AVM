# utils.py

import pygame
import os

def load_image(name, scale=1):
    path = os.path.join('assets', 'images', name)
    image = pygame.image.load(path).convert_alpha()
    if scale != 1:
        size = (int(image.get_width() * scale), int(image.get_height() * scale))
        image = pygame.transform.scale(image, size)
    return image

def load_sound(name):
    path = os.path.join('assets', 'sounds', name)
    return pygame.mixer.Sound(path)
