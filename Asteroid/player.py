import pygame
from config import *
from utils import load_image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = load_image('ship.png', 0.5)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.speed = PLAYER_SPEED
        self.rotation_speed = 5
        self.angle = 0
        self.lives = 3  # 3 nyawa
        self.radius = self.rect.width * 0.3
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 2000  # 2 detik tidak bisa kena
        self.blink_interval = 100  # efek blink setiap 100ms

    def update(self, keys_pressed, current_time):
        # Handle efek invulnerable
        if self.invulnerable:
            if current_time - self.invulnerable_time > self.invulnerable_duration:
                self.invulnerable = False
                self.image.set_alpha(255)  # Kembali normal
            else:
                # Efek blink
                if (current_time // self.blink_interval) % 2 == 0:
                    self.image.set_alpha(100)  # transparan
                else:
                    self.image.set_alpha(255)  # normal

        # Kontrol rotasi
        if keys_pressed[pygame.K_LEFT]:
            self.angle += self.rotation_speed
        if keys_pressed[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed

        # Gerakan
        move = pygame.math.Vector2(0, 0)
        if keys_pressed[pygame.K_UP]:
            move.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:
            move.y += self.speed

        # Terapkan gerakan
        rotated_move = move.rotate(-self.angle)
        self.rect.x += rotated_move.x
        self.rect.y += rotated_move.y

        # Update visual
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Batas layar
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))