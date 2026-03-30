class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect)