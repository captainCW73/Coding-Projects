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
pygame.display.set_caption("Yellow Light Intersection Crash Simulation")
clock = pygame.time.Clock()

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
big_font = pygame.font.SysFont("arial", 36, bold=True)


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
        if t < self.cycle["yellow"]:
            self.phase = "yellow"
        elif t < self.cycle["yellow"] + self.cycle["all_red"]:
            self.phase = "red"
        elif t < self.cycle["yellow"] + self.cycle["all_red"] + self.cycle["green"]:
            self.phase = "red"
        else:
            self.timer = 0.0
            self.phase = "yellow"


class Car:
    def __init__(self, color, size, pos, vel, max_speed):
        self.color = color
        self.size = size
        self.pos = list(pos)
        self.vel = list(vel)
        self.max_speed = max_speed
        self.alive = True
        self.crashed = False
        self.stopped = False
        self.accel = 0.0

    def rect(self):
        w, h = self.size
        r = pygame.Rect(0, 0, w, h)
        r.center = (self.pos[0], self.pos[1])
        return r

    def speed(self):
        return math.hypot(self.vel[0], self.vel[1])

    def update(self, dt):
        if not self.alive:
            return
        if self.accel != 0.0:
            if abs(self.vel[0]) > 0:
                v = self.vel[0]
                s = min(self.max_speed, abs(v) + self.accel * dt)
                self.vel[0] = math.copysign(s, v)
            if abs(self.vel[1]) > 0:
                v = self.vel[1]
                s = min(self.max_speed, abs(v) + self.accel * dt)
                self.vel[1] = math.copysign(s, v)
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt


class Piece:
    def __init__(self, pos, size, color, vel, ang, ang_vel, shape="rect", mass=1.0):
        self.pos = list(pos)
        self.size = size
        self.color = color
        self.vel = list(vel)
        self.ang = ang
        self.ang_vel = ang_vel
        self.shape = shape
        self.mass = mass
        self.alive = True

    def update(self, dt):
        if not self.alive:
            return
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.ang += self.ang_vel * dt
        friction = 0.98
        self.vel[0] *= friction
        self.vel[1] *= friction
        self.ang_vel *= 0.98
        if abs(self.vel[0]) + abs(self.vel[1]) < 3 and abs(self.ang_vel) < 0.1:
            self.vel[0] = 0
            self.vel[1] = 0
            self.ang_vel = 0

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
        self.vel[0] *= 0.98
        self.vel[1] *= 0.98

    def draw(self, surf):
        if self.life <= 0:
            return
        a = max(0, min(255, int(255 * (self.life / 2.0))))
        c = (self.color[0], self.color[1], self.color[2], a)
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, c, (int(self.radius), int(self.radius)), int(self.radius))
        surf.blit(s, (self.pos[0] - self.radius, self.pos[1] - self.radius))


cycle = {"yellow": 2.5, "all_red": 0.6, "green": 3.0}
ns_light = TrafficLight(cycle, initial_phase="yellow")

ew_light = TrafficLight(cycle, initial_phase="red")

car1 = Car(CAR1, (52, 92), (W // 2, H + 200), (0, -260), 260)
car2 = Car(CAR2, (92, 52), (-120, H // 2 - 10), (0, 0), 160)

crash = {"active": False, "timer": 0.0, "pause": 0.0}
frame = 0
sound_played = False
car2_started = False
pieces = []
particles = []
shake = 0.0
collision_printed = False

green_delay = 1.5


stop_line_ns = center[1] + road_h // 2 + 70
stop_line_ew = center[0] - road_w // 2 - 70


def draw_background():
    sky = pygame.Surface((W, H))
    for i in range(H):
        c = 232 + int(16 * (i / H))
        sky.fill((180, 210, c), rect=pygame.Rect(0, i, W, 1))
    screen.blit(sky, (0, 0))
    pygame.draw.rect(screen, BG, (0, H * 0.5, W, H * 0.5))
    for x in range(80, W, 180):
        pygame.draw.circle(screen, GREENERY, (x, 120), 36)
        pygame.draw.circle(screen, (80, 170, 90), (x + 18, 100), 24)
        pygame.draw.rect(screen, TREE_TRUNK, (x - 6, 140, 12, 30))
    for x in range(40, W, 200):
        pygame.draw.circle(screen, GREENERY, (x, H - 120), 34)
        pygame.draw.circle(screen, (80, 170, 90), (x - 16, H - 140), 22)
        pygame.draw.rect(screen, TREE_TRUNK, (x - 6, H - 90, 12, 28))


def draw_roads():
    pygame.draw.rect(screen, (210, 210, 210), (0, 0, W, center[1] - road_h // 2 - 40))
    pygame.draw.rect(screen, (210, 210, 210), (0, center[1] + road_h // 2 + 40, W, H))
    pygame.draw.rect(screen, (210, 210, 210), (0, 0, center[0] - road_w // 2 - 40, H))
    pygame.draw.rect(screen, (210, 210, 210), (center[0] + road_w // 2 + 40, 0, W, H))
    pygame.draw.rect(screen, ROAD, (center[0] - road_w // 2, 0, road_w, H))
    pygame.draw.rect(screen, ROAD, (0, center[1] - road_h // 2, W, road_h))
    wear = pygame.Surface((road_w, road_h), pygame.SRCALPHA)
    wear.fill((0, 0, 0, 35))
    screen.blit(wear, (center[0] - road_w // 2, center[1] - road_h // 2))
    for y in range(0, H, 40):
        pygame.draw.rect(screen, LANE, (center[0] - 4, y + 10, 8, 20))
    for x in range(0, W, 40):
        pygame.draw.rect(screen, LANE, (x + 10, center[1] - 4, 20, 8))
    pygame.draw.line(screen, LANE, (center[0] - road_w // 2, center[1] - road_h // 2 - 60), (center[0] - road_w // 2, center[1] + road_h // 2 + 60), 5)
    pygame.draw.line(screen, LANE, (center[0] + road_w // 2, center[1] - road_h // 2 - 60), (center[0] + road_w // 2, center[1] + road_h // 2 + 60), 5)
    pygame.draw.line(screen, LANE, (center[0] - road_w // 2 - 60, center[1] - road_h // 2), (center[0] + road_w // 2 + 60, center[1] - road_h // 2), 5)
    pygame.draw.line(screen, LANE, (center[0] - road_w // 2 - 60, center[1] + road_h // 2), (center[0] + road_w // 2 + 60, center[1] + road_h // 2), 5)
    pygame.draw.line(screen, YELLOW, (center[0] - 12, 0), (center[0] - 12, H), 4)
    pygame.draw.line(screen, YELLOW, (center[0] + 12, 0), (center[0] + 12, H), 4)
    pygame.draw.line(screen, YELLOW, (0, center[1] - 12), (W, center[1] - 12), 4)
    pygame.draw.line(screen, YELLOW, (0, center[1] + 12), (W, center[1] + 12), 4)
    for i in range(10):
        pygame.draw.line(screen, LANE, (center[0] - road_w // 2 + 40 + i * 20, center[1] - road_h // 2 - 20), (center[0] - road_w // 2 + 40 + i * 20, center[1] - road_h // 2 + 20), 4)
        pygame.draw.line(screen, LANE, (center[0] - road_w // 2 + 40 + i * 20, center[1] + road_h // 2 - 20), (center[0] - road_w // 2 + 40 + i * 20, center[1] + road_h // 2 + 20), 4)
        pygame.draw.line(screen, LANE, (center[0] - road_w // 2 - 20, center[1] - road_h // 2 + 40 + i * 20), (center[0] - road_w // 2 + 20, center[1] - road_h // 2 + 40 + i * 20), 4)
        pygame.draw.line(screen, LANE, (center[0] + road_w // 2 - 20, center[1] - road_h // 2 + 40 + i * 20), (center[0] + road_w // 2 + 20, center[1] - road_h // 2 + 40 + i * 20), 4)
    pygame.draw.line(screen, LANE, (center[0] - road_w // 2, center[1] - road_h // 2 - 70), (center[0] + road_w // 2, center[1] - road_h // 2 - 70), 10)
    pygame.draw.line(screen, LANE, (center[0] - road_w // 2, center[1] + road_h // 2 + 70), (center[0] + road_w // 2, center[1] + road_h // 2 + 70), 10)
    pygame.draw.line(screen, LANE, (center[0] - road_w // 2 - 70, center[1] - road_h // 2), (center[0] - road_w // 2 - 70, center[1] + road_h // 2), 10)
    pygame.draw.line(screen, LANE, (center[0] + road_w // 2 + 70, center[1] - road_h // 2), (center[0] + road_w // 2 + 70, center[1] + road_h // 2), 10)
    arrow = [(center[0] - 60, center[1] - road_h // 2 - 120), (center[0] - 20, center[1] - road_h // 2 - 160), (center[0] + 20, center[1] - road_h // 2 - 120)]
    pygame.draw.polygon(screen, (220, 220, 220), arrow)
    arrow2 = [(center[0] + road_w // 2 + 120, center[1] - 60), (center[0] + road_w // 2 + 160, center[1] - 20), (center[0] + road_w // 2 + 120, center[1] + 20)]
    pygame.draw.polygon(screen, (220, 220, 220), arrow2)


def draw_signal(px, py, phase):
    pygame.draw.rect(screen, (45, 45, 45), (px, py, 26, 86), 0, 6)
    pygame.draw.rect(screen, (80, 80, 80), (px + 8, py + 86, 10, 28), 0, 4)
    red = (255, 0, 0) if phase == "red" else (80, 20, 20)
    yel = (255, 255, 0) if phase == "yellow" else (80, 80, 20)
    grn = (0, 255, 0) if phase == "green" else (20, 80, 20)
    pygame.draw.circle(screen, red, (px + 13, py + 18), 8)
    pygame.draw.circle(screen, yel, (px + 13, py + 43), 8)
    pygame.draw.circle(screen, grn, (px + 13, py + 68), 8)
    if phase == "red":
        gfx.filled_circle(screen, px + 13, py + 18, 16, (255, 0, 0, 60))
    if phase == "yellow":
        gfx.filled_circle(screen, px + 13, py + 43, 16, (255, 255, 0, 60))
    if phase == "green":
        gfx.filled_circle(screen, px + 13, py + 68, 16, (0, 255, 0, 60))


def draw_lights():
    x, y = center
    ns_positions = [
        (x - road_w // 2 - 36, y - road_h // 2 - 80),
        (x + road_w // 2 + 10, y + road_h // 2 + 10),
    ]
    ew_positions = [
        (x + road_w // 2 + 10, y - road_h // 2 - 80),
        (x - road_w // 2 - 36, y + road_h // 2 + 10),
    ]
    for px, py in ns_positions:
        draw_signal(px, py, ns_light.phase)
    for px, py in ew_positions:
        draw_signal(px, py, ew_light.phase)


def draw_car(car, label, brake=False):
    rect = car.rect()
    shadow = pygame.Surface((rect.width + 12, rect.height + 12), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, SHADOW, (0, 0, rect.width + 12, rect.height + 12))
    screen.blit(shadow, (rect.x - 6, rect.y + 8))
    pygame.draw.rect(screen, car.color, rect, 0, 12)
    win = pygame.Rect(rect.x + 8, rect.y + 14, rect.width - 16, rect.height - 28)
    pygame.draw.rect(screen, (180, 200, 210), win, 0, 8)
    roof = [(rect.centerx - 16, rect.y + 8), (rect.centerx + 16, rect.y + 8), (rect.centerx + 10, rect.y + 26), (rect.centerx - 10, rect.y + 26)]
    pygame.draw.polygon(screen, (160, 180, 190), roof)
    pygame.draw.circle(screen, (30, 30, 30), (rect.left + 8, rect.bottom - 10), 8)
    pygame.draw.circle(screen, (90, 90, 90), (rect.left + 8, rect.bottom - 10), 4)
    pygame.draw.circle(screen, (30, 30, 30), (rect.right - 8, rect.bottom - 10), 8)
    pygame.draw.circle(screen, (90, 90, 90), (rect.right - 8, rect.bottom - 10), 4)
    pygame.draw.circle(screen, (255, 240, 220), (rect.centerx - 12, rect.top + 8), 3)
    tail = (255, 60, 60) if brake else (150, 40, 40)
    pygame.draw.circle(screen, tail, (rect.centerx + 12, rect.bottom - 8), 3)
    tag = font.render(label, True, WHITE)
    screen.blit(tag, (rect.centerx - tag.get_width() // 2, rect.top - 22))


def draw_motion(car):
    if car.speed() < 20:
        return
    if abs(car.vel[0]) > abs(car.vel[1]):
        start = (car.pos[0] - 40, car.pos[1])
        end = (car.pos[0] - 10, car.pos[1])
    else:
        start = (car.pos[0], car.pos[1] + 40)
        end = (car.pos[0], car.pos[1] + 10)
    pygame.draw.line(screen, (200, 200, 200), start, end, 3)


def draw_bystanders():
    cars = [
        (center[0] - road_w // 2 + 70, center[1] - road_h // 2 - 140, (40, 80), (60, 60, 60)),
        (center[0] + road_w // 2 - 70, center[1] + road_h // 2 + 140, (40, 80), (230, 230, 230)),
        (center[0] + road_w // 2 + 140, center[1] - road_h // 2 + 80, (80, 40), (40, 40, 40)),
        (center[0] - road_w // 2 - 140, center[1] + road_h // 2 - 80, (80, 40), (210, 210, 210)),
    ]
    for x, y, size, color in cars:
        rect = pygame.Rect(0, 0, size[0], size[1])
        rect.center = (x, y)
        shadow = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, SHADOW, (0, 0, rect.width + 10, rect.height + 10))
        screen.blit(shadow, (rect.x - 5, rect.y + 6))
        pygame.draw.rect(screen, color, rect, 0, 10)
        win = pygame.Rect(rect.x + 6, rect.y + 10, rect.width - 12, rect.height - 20)
        pygame.draw.rect(screen, (180, 200, 210), win, 0, 6)
        pygame.draw.circle(screen, (30, 30, 30), (rect.left + 8, rect.bottom - 8), 7)
        pygame.draw.circle(screen, (30, 30, 30), (rect.right - 8, rect.bottom - 8), 7)


def collision(a, b):
    return a.rect().colliderect(b.rect())


def spawn_crash(pos, impact_dir):
    pieces.clear()
    particles.clear()
    px, py = pos
    vx, vy = impact_dir
    base = 200
    for i in range(4):
        ang = random.uniform(0, math.tau)
        vel = [vx * 0.5 + math.cos(ang) * base, vy * 0.5 + math.sin(ang) * base]
        pieces.append(Piece((px, py), (52, 92), CAR1, vel, ang, random.uniform(-6, 6), "rect", 4.0))
        break
    for i in range(4):
        ang = random.uniform(0, math.tau)
        vel = [vx * 0.3 + math.cos(ang) * base, vy * 0.3 + math.sin(ang) * base]
        pieces.append(Piece((px, py), (92, 52), CAR2, vel, ang, random.uniform(-6, 6), "rect", 4.5))
        break
    parts = [
        ((36, 20), (200, 200, 200), 1.2),
        ((30, 16), (150, 150, 150), 1.0),
        ((18, 10), (120, 120, 120), 0.8),
    ]
    for size, color, mass in parts:
        for _ in range(3):
            ang = random.uniform(0, math.tau)
            vel = [vx + math.cos(ang) * (base + random.uniform(40, 160)), vy + math.sin(ang) * (base + random.uniform(40, 160))]
            pieces.append(Piece((px, py), size, color, vel, ang, random.uniform(-8, 8), "rect", mass))
    for _ in range(4):
        ang = random.uniform(0, math.tau)
        vel = [vx + math.cos(ang) * 260, vy + math.sin(ang) * 260]
        pieces.append(Piece((px, py), 8, (20, 20, 20), vel, 0, random.uniform(-10, 10), "circle", 0.6))
    for _ in range(30):
        ang = random.uniform(0, math.tau)
        vel = [math.cos(ang) * random.uniform(80, 260), math.sin(ang) * random.uniform(80, 260)]
        particles.append(Particle((px, py), vel, random.uniform(2, 4), (200, 230, 255), 1.8))
    for _ in range(18):
        ang = random.uniform(0, math.tau)
        vel = [math.cos(ang) * random.uniform(120, 320), math.sin(ang) * random.uniform(120, 320)]
        particles.append(Particle((px, py), vel, random.uniform(2, 3), (255, 200, 80), 1.0))
    for _ in range(20):
        ang = random.uniform(0, math.tau)
        vel = [math.cos(ang) * random.uniform(60, 180), math.sin(ang) * random.uniform(60, 180)]
        particles.append(Particle((px, py), vel, random.uniform(2, 3), (60, 60, 60), 2.0))
    for _ in range(8):
        vel = [random.uniform(-20, 20), random.uniform(-50, -10)]
        particles.append(Particle((px, py), vel, random.uniform(8, 14), (120, 120, 120), 3.0, grow=6.0))


def reset():
    ns_light.timer = 0.0
    ns_light.phase = "yellow"
    ew_light.timer = 0.0
    ew_light.phase = "red"
    car1.vel = [0, -300]
    t_start = cycle["yellow"] + cycle["all_red"] + green_delay + 0.8
    car1.pos = [W // 2, center[1] + abs(car1.vel[1]) * t_start]
    car1.alive = True
    car1.crashed = False
    car2.vel = [150, 0]
    car2.pos = [stop_line_ew - car2.size[0] // 2, H // 2 - 10]
    car2.alive = True
    car2.crashed = False
    car2.stopped = True
    car2.accel = 0.0
    global crash, sound_played, car2_started, pieces, particles, shake, collision_printed
    crash = {"active": False, "timer": 0.0, "pause": 0.0}
    sound_played = False
    car2_started = False
    pieces = []
    particles = []
    shake = 0.0
    collision_printed = False


reset()
running = True

while running:
    dt = clock.tick(60) / 1000.0
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset()

    ns_light.update(dt)
    t = ns_light.timer
    if t < cycle["yellow"]:
        ns_light.phase = "yellow"
        ew_light.phase = "red"
        time_to_change = cycle["yellow"] - t
    elif t < cycle["yellow"] + cycle["all_red"]:
        ns_light.phase = "red"
        ew_light.phase = "red"
        time_to_change = cycle["yellow"] + cycle["all_red"] - t
    elif t < cycle["yellow"] + cycle["all_red"] + cycle["green"]:
        ns_light.phase = "red"
        ew_light.phase = "green"
        time_to_change = cycle["yellow"] + cycle["all_red"] + cycle["green"] - t
    else:
        ns_light.timer = 0.0
        ns_light.phase = "yellow"
        ew_light.phase = "red"
        time_to_change = cycle["yellow"]

    if crash["pause"] > 0:
        crash["pause"] -= dt
    else:
        if not crash["active"]:
            car1.update(dt)
            if ew_light.phase == "green":
                if not car2_started:
                    car2_started = True
                    car2.accel = 90.0
                if car2_started and ns_light.timer >= cycle["yellow"] + cycle["all_red"] + green_delay:
                    car2.stopped = False
                    dist_to_center = max(1.0, center[0] - car2.pos[0])
                    t_remain = max(0.2, abs(car1.pos[1] - center[1]) / max(1.0, abs(car1.vel[1])))
                    target_speed = min(car2.max_speed, dist_to_center / t_remain)
                    car2.max_speed = target_speed
                    if car2.vel[0] == 0:
                        car2.vel[0] = 10.0
            if car2.stopped:
                car2.vel[0] = 0
                car2.pos[0] = stop_line_ew - car2.size[0] // 2
            else:
                car2.update(dt)
        else:
            for p in pieces:
                p.update(dt)
            for prt in particles:
                prt.update(dt)
            particles = [p for p in particles if p.life > 0]

    dx = car2.pos[0] - car1.pos[0]
    dy = car2.pos[1] - car1.pos[1]
    dist = math.hypot(dx, dy)
    size_sum = (car1.size[0] + car1.size[1] + car2.size[0] + car2.size[1]) / 4
    dist_check = dist < (size_sum / 2)
    if (collision(car1, car2) or dist_check) and not crash["active"]:
        crash["active"] = True
        crash["timer"] = 2.0
        crash["pause"] = 0.2
        car1.crashed = True
        car2.crashed = True
        car1.alive = False
        car2.alive = False
        impact = (car1.vel[0] + car2.vel[0], car1.vel[1] + car2.vel[1])
        spawn_crash(center, impact)
        shake = 12.0
        if not sound_played:
            crash_sound.play()
            sound_played = True
        if not collision_printed:
            print("COLLISION DETECTED!")
            collision_printed = True

    draw_background()

    offset = (0, 0)
    if shake > 0:
        offset = (random.randint(-6, 6), random.randint(-6, 6))
        shake = max(0, shake - 30 * dt)
    temp = pygame.Surface((W, H), pygame.SRCALPHA)

    draw_roads()
    draw_lights()
    draw_bystanders()

    if not crash["active"]:
        draw_motion(car1)
        draw_motion(car2)
        draw_car(car1, "Speeding Vehicle", False)
        draw_car(car2, "Law-Abiding Driver", car2.stopped or ew_light.phase != "green")
    else:
        for p in pieces:
            p.draw(screen)
        for prt in particles:
            prt.draw(screen)
        flash = pygame.Surface((W, H), pygame.SRCALPHA)
        if crash["timer"] > 1.5:
            flash.fill((255, 255, 255, 120))
            screen.blit(flash, (0, 0))

    pygame.draw.line(screen, (220, 40, 40), (center[0] - 10, center[1] - 10), (center[0] + 10, center[1] + 10), 3)
    pygame.draw.line(screen, (220, 40, 40), (center[0] - 10, center[1] + 10), (center[0] + 10, center[1] - 10), 3)
    pygame.draw.rect(screen, (0, 200, 255), car1.rect(), 2)
    pygame.draw.rect(screen, (255, 200, 0), car2.rect(), 2)

    dx = car2.pos[0] - car1.pos[0]
    dy = car2.pos[1] - car1.pos[1]
    dist = math.hypot(dx, dy)
    t_car1 = abs(car1.pos[1] - center[1]) / max(1.0, abs(car1.vel[1]))
    if car2.stopped:
        t_car2 = max(0.0, (cycle["yellow"] + cycle["all_red"] + green_delay) - ns_light.timer)
        t_car2 += abs(car2.pos[0] - center[0]) / max(1.0, car2.max_speed)
    else:
        t_car2 = abs(car2.pos[0] - center[0]) / max(1.0, abs(car2.vel[0]))
    ttc = min(t_car1, t_car2)

    panel = pygame.Surface((280, 160), pygame.SRCALPHA)
    panel.fill((20, 20, 20, 170))
    screen.blit(panel, (20, 20))
    hud = [
        f"Frame: {frame}",
        f"NS Light: {ns_light.phase.upper()}",
        f"EW Light: {ew_light.phase.upper()}",
        f"Light Change In: {time_to_change:.1f}s",
        f"Speeding Vehicle: {int(car1.speed())} px/s",
        f"Law-Abiding Driver: {int(car2.speed())} px/s",
        f"Distance: {int(dist)} px",
        f"Time To Collision: {ttc:.1f}s",
            "R to reset",
    ]
    for i, line in enumerate(hud):
        t = font.render(line, True, WHITE)
        screen.blit(t, (30, 28 + i * 20))

    pygame.display.flip()

pygame.quit()
