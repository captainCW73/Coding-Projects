cat > ~/joystick_stepper.py << 'EOF'
import RPi.GPIO as GPIO
import smbus2
import time

ADS7830_ADDR = 0x4b
bus = smbus2.SMBus(1)

IN1, IN2, IN3, IN4 = 17, 18, 27, 22
PINS = [IN1, IN2, IN3, IN4]
SEQUENCE = [
    [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
    [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1],
]

SERVO_PIN = 19
DEADZONE = 40
CENTER = 128
servo_angle = 90

def read_channel(channel):
    cmd = 0x84 | (channel << 4)
    bus.write_byte(ADS7830_ADDR, cmd)
    time.sleep(0.01)
    return bus.read_byte(ADS7830_ADDR)

def step_motor(direction, steps=2, delay=0.002):
    seq = SEQUENCE if direction == 1 else list(reversed(SEQUENCE))
    for _ in range(steps):
        for s in seq:
            for pin, val in zip(PINS, s):
                GPIO.output(pin, val)
            time.sleep(delay)

def set_servo(angle):
    duty = 2.5 + (angle / 180.0) * 10
    servo.ChangeDutyCycle(duty)
    time.sleep(0.02)
    servo.ChangeDutyCycle(0)

def all_off():
    for p in PINS:
        GPIO.output(p, 0)

GPIO.setmode(GPIO.BCM)
for p in PINS:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, 0)

GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)
time.sleep(0.5)
set_servo(90)
all_off()

print("Y axis: stepper | X axis: servo | Ctrl+C to stop")

try:
    while True:
        y = read_channel(0)
        x = read_channel(1)

        y_diff = y - CENTER
        if abs(y_diff) > DEADZONE:
            direction = 1 if y_diff > 0 else -1
            speed = int((abs(y_diff) / 128) * 4) + 1
            step_motor(direction, steps=speed)
        else:
            all_off()

        x_diff = x - CENTER
        if abs(x_diff) > DEADZONE:
            delta = 1 if x_diff > 0 else -1
            new_angle = max(0, min(180, servo_angle + delta * int((abs(x_diff) / 128) * 3 + 1)))
            if new_angle != servo_angle:
                servo_angle = new_angle
                set_servo(servo_angle)

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Stopping")
finally:
    all_off()
    servo.stop()
    GPIO.cleanup()
EOF
#python3 ~/joystick_stepper.py to run the code
