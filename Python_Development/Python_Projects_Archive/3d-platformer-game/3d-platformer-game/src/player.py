class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_power = 10
        self.on_ground = False

    def move(self, dx):
        self.rect.x += dx

    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_power

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    def check_collision(self, platforms):
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat.rect) and self.velocity_y >= 0:
                self.rect.bottom = plat.rect.top
                self.velocity_y = 0
                self.on_ground = True

    def draw(self, win, color):
        pygame.draw.rect(win, color, self.rect)