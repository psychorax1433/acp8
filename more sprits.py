"""
Player‑vs‑Enemies collision demo
--------------------------------
• Arrow keys or W A S D  →  move the blue player rectangle
• 7 red enemy rectangles start at random positions
• Each collision adds 1 to the score and respawns that enemy
"""

import pygame
import sys
import random

# ── basic setup ────────────────────────────────────────────────────────────────
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Score Game")
clock        = pygame.time.Clock()
FPS          = 60
WHITE        = (255, 255, 255)
PLAYER_COLOR = ( 30, 144, 255)   # DodgerBlue
ENEMY_COLOR  = (220,  20,  60)   # Crimson
FONT         = pygame.font.SysFont(None, 36)

# ── sprite classes ─────────────────────────────────────────────────────────────
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size=(50, 50), speed=5):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(PLAYER_COLOR)
        self.rect  = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self, keys):
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]:
            self.rect.y += self.speed

        # keep inside window
        self.rect.clamp_ip(screen.get_rect())

class Enemy(pygame.sprite.Sprite):
    def __init__(self, size=(40, 40)):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(ENEMY_COLOR)
        self.rect  = self.image.get_rect()
        self.random_reposition()

    def random_reposition(self):
        self.rect.x = random.randint(0, WIDTH  - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

# ── create sprites ─────────────────────────────────────────────────────────────
player = Player((WIDTH//2, HEIGHT//2))
enemies = pygame.sprite.Group([Enemy() for _ in range(7)])
all_sprites = pygame.sprite.Group(enemies, player)

# ── game variables ─────────────────────────────────────────────────────────────
score = 0

# ── main loop ──────────────────────────────────────────────────────────────────
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    player.update(keys)

    # collision detection
    collided_enemies = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in collided_enemies:
        score += 1
        enemy.random_reposition()

    # draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    score_surface = FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
# ── end of file ────────────────────────────────────────────────────────────────