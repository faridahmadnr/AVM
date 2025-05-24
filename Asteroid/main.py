import pygame
import sys
from config import *
from player import Player
from bullet import Bullet
from asteroid import Asteroid
from explosion import Explosion
from utils import load_sound

def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    # Load sounds
    shoot_sound = load_sound('0523.mp3')
    explosion_sound = load_sound('explosion.mp3')
    hit_sound = load_sound('spwan.mp3')
    game_over_sound = load_sound('game_over.mp3')  # Ganti dengan file sound game over Anda
    pygame.mixer.music.load('assets/sounds/background.mp3')
    pygame.mixer.music.play(-1)

    def reset_game():
        """Reset semua game state untuk restart"""
        nonlocal score, player, all_sprites, bullets, asteroids, explosions
        
        # Reset sprite groups
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        
        # Buat player baru
        player = Player()
        all_sprites.add(player)
        
        # Reset score
        score = 0
        
        # Spawn asteroid awal
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)
        
        return player

    # Game state awal
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)
    score = 0
    font = pygame.font.SysFont(None, 36)
    max_asteroids = 5
    spawn_delay = 2000
    last_spawn_time = pygame.time.get_ticks()
    game_active = True

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bullet = Bullet(player.rect.center, player.angle)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()
                if event.key == pygame.K_r and not game_active:
                    # Restart game
                    player = reset_game()
                    game_active = True
                    pygame.mixer.music.play(-1)  # Restart background music

        if game_active:
            # Game logic saat bermain
            keys_pressed = pygame.key.get_pressed()
            
            # Spawn asteroid
            if len(asteroids) < max_asteroids and current_time - last_spawn_time > spawn_delay:
                new_asteroid = Asteroid()
                all_sprites.add(new_asteroid)
                asteroids.add(new_asteroid)
                last_spawn_time = current_time

            # Update sprites
            player.update(keys_pressed, current_time)
            bullets.update()
            asteroids.update()
            explosions.update()

            # Collision detection
            hits = pygame.sprite.groupcollide(asteroids, bullets, True, True, collided=pygame.sprite.collide_circle)
            for hit in hits:
                explosion = Explosion(hit.rect.center)
                all_sprites.add(explosion)
                explosions.add(explosion)
                explosion_sound.play()
                score += 10

            # Player collision
            if not player.invulnerable:
                if pygame.sprite.spritecollideany(player, asteroids, collided=pygame.sprite.collide_circle):
                    hit_sound.play()
                    player.lives -= 1
                    player.invulnerable = True
                    player.invulnerable_time = current_time
                    
                    if player.lives <= 0:
                        game_over_sound.play()  # Play game over sound
                        explosion = Explosion(player.rect.center)
                        all_sprites.add(explosion)
                        explosions.add(explosion)
                        game_active = False
                        pygame.mixer.music.stop()  # Stop background music

        # Drawing
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        explosions.draw(screen)

        # Draw UI
        if game_active:
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))

            if player.invulnerable:
                invul_time = (player.invulnerable_duration - (current_time - player.invulnerable_time)) // 1000
                invul_text = font.render(f"Immune: {invul_time}s", True, (255, 0, 0))
                screen.blit(invul_text, (10, 90))
        else:
            # Game over screen
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50, (255, 0, 0))
            draw_text(screen, f"Final Score: {score}", 48, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)
            draw_text(screen, "Press R to Restart", 36, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80)
            draw_text(screen, "Press ESC to Quit", 36, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 120)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
