# PICO_MAIN1 (right board) - listens to Din and drives the speaker
#
# GPIO1   (pin 2)  -> Din1      (input from other Pico)
# GPIO16  (pin 21) -> SPEAKER_OUT (PWM to transistor + speaker)
# GPIO22  (pin 29) -> BTN_IN    (pushbutton to GND, active LOW)

from machine import Pin, PWM
import time

# Pin numbers
DIN_PIN      = 1   # from PICO_GEN1
SPEAKER_PIN  = 16  # to base resistor / transistor / speaker
BUTTON_PIN   = 22  # push button to GND

# Setup input pins
din = Pin(DIN_PIN, Pin.IN, Pin.PULL_DOWN)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)  # active LOW

# Setup speaker PWM
speaker_pwm = PWM(Pin(SPEAKER_PIN))
speaker_pwm.freq(1000)   # 1 kHz tone
speaker_pwm.duty_u16(0)  # start silent

def beep(duration_ms=1000):
    """Play a simple tone for duration_ms milliseconds."""
    # If button is held, mute (safety / test mute)
    if button.value() == 0:  # button pressed (LOW)
        return

    speaker_pwm.duty_u16(32768)  # ~50% duty (16-bit)
    time.sleep_ms(duration_ms)
    speaker_pwm.duty_u16(0)

print("PICO_MAIN1 running: waiting for Din rising edges...")

last_din = din.value()

while True:
    current = din.value()

    # Detect rising edge: 0 -> 1
    if last_din == 0 and current == 1:
        # Got a "drop event" from the other Pico
        beep(1000)  # 1-second beep

    last_din = current

    # Poll quickly but not insanely fast
    time.sleep_ms(5)
