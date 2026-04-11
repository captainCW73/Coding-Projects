import sys
import math
import random
import array

try:
    import pygame
    import pygame.gfxdraw as gfx
except Exception:
    print("This simulation needs pygame. Install with: python -m pip install pygame")
    sys.exit(1)

pygame.init()
pygame.mixer.init()

W, H = 900, 900
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("The T-Bone Incident")
clock = pygame.time.Clock()

# --- COLORS & STYLES ---
ROAD = (64, 64, 64)
LANE = (255, 255, 255)
YELLOW = (255, 255, 0)
BG = (232, 232, 232)
CAR1 = (220, 40, 40)
CAR2 = (200, 200, 200)
WHITE = (245, 245, 245)
SHADOW = (0, 0, 0, 90)
GREENERY = (60, 140, 70)
TREE_TRUNK = (90, 60, 30)

center = (W // 2, H // 2)
road_w = 340
road_h = 340
font = pygame.font.SysFont("arial", 18)

def make_crash_sound():
    freq = 44100
    duration = 0.35
    volume = 0.6
    samples = int(freq * duration)
    buf = array.array("h")
    for i in range(samples):
        t = i / freq
        wave = 1.0 if (int(t * 220 * 2) % 2 == 0) else -1.0
        env = max(0.0, 1.0 - t / duration)
        val = int(32767 * volume * wave * env)
        buf.append(val)
    return pygame.mixer.Sound(buffer=buf.tobytes())

crash_sound = make_crash_sound()

class TrafficLight:
    def __init__(self, cycle, initial_phase="yellow"):
        self.cycle = cycle
        self.timer = 0.0
        self.phase = initial_phase

    def update(self, dt):
        self.timer += dt
        t = self.timer
        if t < self.cycle["yellow"]: self.phase = "yellow"
        elif t < self.cycle["yellow"] + self.cycle["all_red"]: self.phase = "red"
        elif t < self.cycle["yellow"] + self.cycle["all_red"] + self.cycle["green"]: self.phase = "red"
        else:
            self.timer = 0.0
            self.phase = "yellow"

class Car:
    def __init__(self, color, size, pos, vel):
        self.color = color
        self.size = size
        self.pos = list(pos)
        self.vel = list(vel)
        self.alive = True

    def rect(self):
        w, h = self.size
        r = pygame.Rect(0, 0, w, h)
        r.center = (self.pos[0], self.pos[1])
        return r

    def speed(self):
        return math.hypot(self.vel[0], self.vel[1])

    def update(self, dt):
        if not self.alive: return
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt

class Piece:
    def __init__(self, pos, size, color, vel, ang, ang_vel, shape="rect"):
        self.pos = list(pos)
        self.size = size
        self.color = color
        self.vel = list(vel)
        self.ang = ang
        self.ang_vel = ang_vel
        self.shape = shape
        self.alive = True

    def update(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.ang += self.ang_vel * dt
        self.vel[0] *= 0.98
        self.vel[1] *= 0.98
        self.ang_vel *= 0.98

    def draw(self, surf):
        if self.shape == "circle":
            pygame.draw.circle(surf, self.color, (int(self.pos[0]), int(self.pos[1])), self.size)
            return
        w, h = self.size
        rect = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(rect, self.color, (0, 0, w, h), 0, 4)
        rot = pygame.transform.rotate(rect, math.degrees(self.ang))
        r = rot.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        surf.blit(rot, r.topleft)

class Particle:
    def __init__(self, pos, vel, radius, color, life, grow=0.0):
        self.pos = list(pos)
        self.vel = list(vel)
        self.radius = radius
        self.color = color
        self.life = life
        self.grow = grow

    def update(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.radius = max(0, self.radius + self.grow * dt)
        self.life -= dt

    def draw(self, surf):
        if self.life <= 0: return
        a = max(0, min(255, int(255 * (self.life / 2.0))))
        c = (self.color[0], self.color[1], self.color[2], a)
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, c, (int(self.radius), int(self.radius)), int(self.radius))
        surf.blit(s, (self.pos[0] - self.radius, self.pos[1] - self.radius))

# --- ENVIRONMENT DRAWING ---
def draw_background():
    sky = pygame.Surface((W, H))
    for i in range(H):
        c = 232 + int(16 * (i / H))
        sky.fill((180, 210, c), rect=pygame.Rect(0, i, W, 1))
    screen.blit(sky, (0, 0))
    pygame.draw.rect(screen, BG, (0, H * 0.5, W, H * 0.5))
    for x in range(80, W, 180):
        pygame.draw.circle(screen, GREENERY, (x, 120), 36)
        pygame.draw.rect(screen, TREE_TRUNK, (x - 6, 140, 12, 30))

def draw_roads():
    pygame.draw.rect(screen, ROAD, (center[0] - road_w // 2, 0, road_w, H))
    pygame.draw.rect(screen, ROAD, (0, center[1] - road_h // 2, W, road_h))
    for y in range(0, H, 40): pygame.draw.rect(screen, LANE, (center[0] - 4, y + 10, 8, 20))
    for x in range(0, W, 40): pygame.draw.rect(screen, LANE, (x + 10, center[1] - 4, 20, 8))
    pygame.draw.line(screen, YELLOW, (center[0] - 12, 0), (center[0] - 12, H), 4)
    pygame.draw.line(screen, YELLOW, (0, center[1] - 12), (W, center[1] - 12), 4)

def draw_signal(px, py, phase):
    pygame.draw.rect(screen, (45, 45, 45), (px, py, 26, 86), 0, 6)
    red = (255, 0, 0) if phase == "red" else (40, 0, 0)
    yel = (255, 255, 0) if phase == "yellow" else (40, 40, 0)
    grn = (0, 255, 0) if phase == "green" else (0, 40, 0)
    pygame.draw.circle(screen, red, (px + 13, py + 18), 8)
    pygame.draw.circle(screen, yel, (px + 13, py + 43), 8)
    pygame.draw.circle(screen, grn, (px + 13, py + 68), 8)

def draw_car_fancy(car, label):
    rect = car.rect()
    shadow = pygame.Surface((rect.width + 12, rect.height + 12), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, SHADOW, (0, 0, rect.width + 12, rect.height + 12))
    screen.blit(shadow, (rect.x - 6, rect.y + 8))
    pygame.draw.rect(screen, car.color, rect, 0, 12)
    tag = font.render(label, True, WHITE)
    screen.blit(tag, (rect.centerx - tag.get_width() // 2, rect.top - 22))

def spawn_crash(pos, impact_dir):
    px, py = pos
    vx, vy = impact_dir
    new_p = []
    new_prt = []
    for _ in range(15):
        ang = random.uniform(0, math.tau)
        vel = [vx * 0.4 + math.cos(ang) * 400, vy * 0.4 + math.sin(ang) * 400]
        new_p.append(Piece((px, py), (20, 20), (120, 120, 120), vel, ang, random.uniform(-10, 10)))
    for _ in range(40):
        vel = [random.uniform(-300, 300), random.uniform(-300, 300)]
        new_prt.append(Particle((px, py), vel, random.uniform(2, 6), (255, 180, 50), 2.0))
    return new_p, new_prt

# --- MAIN LOOP ---
cycle = {"yellow": 2.5, "all_red": 0.6, "green": 3.0}
ns_light = TrafficLight(cycle, initial_phase="yellow")
ew_light = TrafficLight(cycle, initial_phase="red")

car1 = Car(CAR1, (52, 92), (W // 2, center[1] + 120), (0, -110))
car2 = Car(CAR2, (92, 52), (-500, H // 2 - 10), (800, 0))

pieces = []
particles = []
crash_active = False
shake = 0.0

def reset():
    global car1, car2, pieces, particles, crash_active, shake
    car1 = Car(CAR1, (52, 92), (W // 2, center[1] + 120), (0, -110))
    car2 = Car(CAR2, (92, 52), (-500, H // 2 - 10), (800, 0))
    pieces, particles = [], []
    crash_active = False
    shake = 0.0

running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r: reset()

    ns_light.update(dt)
    ew_light.update(dt)

    if not crash_active:
        car1.update(dt)
        car2.update(dt)
        if car1.rect().colliderect(car2.rect()):
            crash_active = True
            impact = (car1.vel[0] + car2.vel[0], car1.vel[1] + car2.vel[1])
            pieces, particles = spawn_crash(car1.pos, impact)
            crash_sound.play()
            shake = 15.0
    else:
        for p in pieces: p.update(dt)
        for prt in particles: prt.update(dt)
        particles = [p for p in particles if p.life > 0]
        shake = max(0, shake - 40 * dt)

    # Rendering
    draw_background()
    draw_roads()
    draw_signal(center[0] - 200, center[1] - 250, ns_light.phase)
    draw_signal(center[0] + 180, center[1] - 250, ew_light.phase)

    if not crash_active:
        draw_car_fancy(car1, "Target")
        draw_car_fancy(car2, "Aggressor")
    else:
        for p in pieces: p.draw(screen)
        for prt in particles: prt.draw(screen)

    msg = font.render("R to Reset", True, (0, 0, 0))
    screen.blit(msg, (20, 20))
    pygame.display.flip()

pygame.quit()
