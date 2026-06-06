# filepath: /3d-platformer-game/3d-platformer-game/src/game.py
import pygame
import sys
from player import Player
from platform import Platform

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("3D-Like Platformer (Fake 3D)")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize player and platforms
        self.player = Player(100, 500)
        self.platforms = [
            Platform(0, 580, 800, 20),
            Platform(300, 480, 100, 10),
            Platform(450, 380, 100, 10),
            Platform(600, 280, 100, 10)
        ]

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.update(self.platforms)

    def render(self):
        self.win.fill((40, 40, 60))  # Background
        for plat in self.platforms:
            plat.draw(self.win)
        self.player.draw(self.win)
        pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
    game.quit()