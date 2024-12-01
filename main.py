import plasma
import machine
import time

# Constants
NUM_LEDS = 66  # Number of LEDs in your strip
DATA_PIN = 22  # Data line connected to GPIO 22 (Pin 29)
DARK_THRESHOLD = 10000  # Light sensor threshold for "darkness"
FADE_IN_STEPS = 50
FADE_OUT_STEPS = 50
FADE_DELAY = 0.01
LED_TIMEOUT = 20  # Timeout in seconds before checking for motion

# Initialize the WS2812 RGB LED strip
led_strip = plasma.WS2812(NUM_LEDS, pio=0, sm=0, dat=DATA_PIN)
led_strip.start()

# Turn off all LEDs at initialization
for i in range(NUM_LEDS):
    led_strip.set_rgb(i, 0, 0, 0)  # Ensure LEDs are off (GRB order)

# Initialize sensors
light_sensor = machine.ADC(27)  # Light sensor on GPIO 27
pir_sensor = machine.Pin(28, machine.Pin.IN)  # PIR sensor on GPIO 28

# Function to fade in the LEDs
def fade_in_leds(target_r, target_g, target_b, start_r=0, start_g=0, start_b=0):
    for step in range(FADE_IN_STEPS + 1):
        factor = step / FADE_IN_STEPS
        r = int(start_r + (target_r - start_r) * factor * 0.4)  # 40% brightness
        g = int(start_g + (target_g - start_g) * factor * 0.4)
        b = int(start_b + (target_b - start_b) * factor * 0.4)
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, b, r, g)
        time.sleep(FADE_DELAY)

# Function to fade out the LEDs
def fade_out_leds(current_r, current_g, current_b):
    for step in range(FADE_OUT_STEPS, -1, -1):
        factor = step / FADE_OUT_STEPS
        r = int(current_r * factor * 0.4)
        g = int(current_g * factor * 0.4)
        b = int(current_b * factor * 0.4)
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, b, r, g)
        time.sleep(FADE_DELAY)

        # Check for motion during fade-out
        if pir_sensor.value() == 1:
            print("Motion Detected During Fade-Out: Fading Back IN")
            fade_in_leds(255, 255, 255, r, g, b)  # Fade back in from stored value
            return False  # Cancel fade-out
    return True  # Fade-out completed

# Main loop to handle light and motion detection with timeout
leds_on = False
timeout_start = 0
while True:
    # Read light sensor
    light_level = light_sensor.read_u16()
    is_dark = light_level < DARK_THRESHOLD

    # Read PIR sensor
    motion_detected = pir_sensor.value() == 1

    if is_dark and motion_detected:
        if not leds_on:
            print("Dark and Motion Detected: Fading LEDs IN")
            fade_in_leds(255, 255, 255)  # White in GRB order
            leds_on = True
            timeout_start = time.time()  # Start timeout countdown
    elif leds_on:
        # Check if the timeout has expired
        if time.time() - timeout_start >= LED_TIMEOUT:
            print("Timeout reached. Checking conditions.")
            motion_detected_after_timeout = pir_sensor.value() == 1
            if motion_detected_after_timeout:
                print("Motion Detected: Resetting timeout.")
                timeout_start = time.time()  # Reset timeout
            elif not is_dark:
                print("Light Detected: Fading LEDs OUT")
                if fade_out_leds(255, 255, 255):  # Fade out from white
                    leds_on = False
            else:
                print("No Motion: Fading LEDs OUT")
                if fade_out_leds(255, 255, 255):  # Fade out from white
                    leds_on = False

    # Debugging output
    print(f"Light Level: {light_level}, Motion Detected: {motion_detected}")
    time.sleep(0.1)

