import pygame
from game.player import Player
from game.enemies import Enemy
from game.level import Level

def main():
    pygame.init()
    
    # Set up the game window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("3D Platformer Game")
    
    # Initialize game objects
    player = Player()
    enemy = Enemy()
    level = Level()
    
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update game state
        player.move()
        enemy.patrol()
        level.update()
        
        # Render the game
        screen.fill((0, 0, 0))  # Clear the screen with black
        # Here you would draw your player, enemies, and level
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()