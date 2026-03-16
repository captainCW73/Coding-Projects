import pygame
import sys

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("3D-Like Platformer (Fake 3D)")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
ORANGE = (255, 150, 0)
BLACK = (0, 0, 0)

# Player
player = pygame.Rect(100, 500, 40, 60)
velocity_y = 0
gravity = 0.5
jump_power = 10
on_ground = False

# Platforms
platforms = [pygame.Rect(0, 580, 800, 20),
             pygame.Rect(300, 480, 100, 10),
             pygame.Rect(450, 380, 100, 10),
             pygame.Rect(600, 280, 100, 10)]

# Draw cube with fake 3D shading
def draw_block(rect, color):
    pygame.draw.rect(win, color, rect)
    shadow = pygame.Rect(rect.x + 5, rect.y + 5, rect.width, rect.height)
    pygame.draw.rect(win, (color[0]//2, color[1]//2, color[2]//2), shadow)

# Main loop
while True:
    win.fill((40, 40, 60))  # Background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = -jump_power

    # Apply gravity
    velocity_y += gravity
    player.y += velocity_y
    on_ground = False

    # Collision with platforms
    for plat in platforms:
        if player.colliderect(plat) and velocity_y >= 0:
            player.bottom = plat.top
            velocity_y = 0
            on_ground = True

    # Draw platforms
    for plat in platforms:
        draw_block(plat, GREEN)

    # Draw player
    draw_block(player, ORANGE)

    # Refresh
    pygame.display.update()
    clock.tick(60)

