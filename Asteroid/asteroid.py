import pygame
import random
import math
from config import *
from utils import load_image

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, player_pos=None, min_distance=200):
        super().__init__()
        self.image = load_image('asteroid.png', 0.5)
        self.rect = self.image.get_rect()
        
        # Vector properties
        self.pos = pygame.math.Vector2(
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT)
        )
        self.velocity = pygame.math.Vector2(
            random.uniform(-1, 1) * ASTEROID_SPEED,
            random.uniform(-1, 1) * ASTEROID_SPEED
        ).normalize() * ASTEROID_SPEED
        
        self.radius = self.rect.width * 0.3

        # Ensure safe spawn distance from player
        if player_pos:
            player_vec = pygame.math.Vector2(player_pos)
            while self.pos.distance_to(player_vec) < min_distance:
                self.pos = pygame.math.Vector2(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT)
                )
        
        # Set initial rect position
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def update(self):
        # Update position with vector math
        self.pos += self.velocity
        
        # Screen wrapping with vector logic
        if self.pos.x > SCREEN_WIDTH + self.rect.width/2:
            self.pos.x = -self.rect.width/2
        elif self.pos.x < -self.rect.width/2:
            self.pos.x = SCREEN_WIDTH + self.rect.width/2
            
        if self.pos.y > SCREEN_HEIGHT + self.rect.height/2:
            self.pos.y = -self.rect.height/2
        elif self.pos.y < -self.rect.height/2:
            self.pos.y = SCREEN_HEIGHT + self.rect.height/2
        
        # Update rect position
        self.rect.center = (int(self.pos.x), int(self.pos.y))