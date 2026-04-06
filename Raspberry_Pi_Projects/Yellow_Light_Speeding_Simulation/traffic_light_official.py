import RPi.GPIO as GPIO
import time
from gpiozero import PWMLED

GPIO.setmode(GPIO.BCM)
led_yellow = PWMLED(26)

# green led
GPIO.setup(20, GPIO.OUT)
# yellow led (note: this conflicts with gpiozero LED on pin 26)
# GPIO.setup(26, GPIO.OUT)  # Comment this out since we're using gpiozero for pin 26
# red led
GPIO.setup(21, GPIO.OUT)
# buzzer
buzzer_pin = 17  # Change to your buzzer pin if different
GPIO.setup(buzzer_pin, GPIO.OUT)

# Initialize all LEDs and buzzer to OFF
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
led_yellow.off()
GPIO.output(buzzer_pin, GPIO.LOW)

try:
    while True:
        # Red light
        GPIO.output(21, GPIO.HIGH)
        print("Red")
        time.sleep(4)
        GPIO.output(21, GPIO.LOW)
        
        # Yellow fading with buzzer
        led_yellow.on()
        time.sleep(3)
        for _ in range(5):
            GPIO.output(buzzer_pin, GPIO.HIGH)  # CHANGED: Buzzer ON at start
            
            # Fade in
            for brightness in range(0, 101, 10):
                led_yellow.value = brightness / 100
                time.sleep(0.025)
            
            # Fade out
            for brightness in range(100, -1, -10):
                led_yellow.value = brightness / 100
                time.sleep(0.025)
            
            GPIO.output(buzzer_pin, GPIO.LOW)   # CHANGED: Buzzer OFF at end
            time.sleep(0.05)  # ADDED: Small pause between pulses
            
        print("Yellow")
        
        # Green light
        GPIO.output(20, GPIO.HIGH)
        print("Green")
        time.sleep(4)
        print("------------")
        GPIO.output(20, GPIO.LOW)
        
finally:
    GPIO.cleanup()

