# bullet.py

import pygame
from config import *
from utils import load_image

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, angle):
        super().__init__()
        self.image = load_image('bullets.png', 0.2)
        self.rect = self.image.get_rect(center=position)
        self.velocity = pygame.math.Vector2(BULLET_SPEED, 0).rotate(-angle)

    def update(self):
        self.rect.move_ip(self.velocity)
        # Remove bullet if it goes off-screen
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).collidepoint(self.rect.center):
            self.kill()
