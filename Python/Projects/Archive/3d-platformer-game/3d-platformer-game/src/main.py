import pygame
import sys
from player import Player
from platform import Platform
from game import Game

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D-Like Platformer (Fake 3D)")
clock = pygame.time.Clock()

# Create game instance
game = Game()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.update()
    game.draw(win)

    pygame.display.update()
    clock.tick(60)