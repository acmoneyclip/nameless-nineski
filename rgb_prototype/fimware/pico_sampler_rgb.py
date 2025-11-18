from machine import Pin, PWM
import time

from drop_samples import drop_samples
from tow_samples import tow_samples
from er_samples import er_samples

# ---------- AUDIO SETUP (GP15) ----------

speaker = PWM(Pin(15))
SAMPLE_RATE = 8000
DT_US = int(1_000_000 / SAMPLE_RATE)

def play_sample(samples):
    speaker.freq(20000)  # 20 kHz carrier
    t = time.ticks_us()
    for s in samples:
        speaker.duty_u16(s * 257)
        t = time.ticks_add(t, DT_US)
        while time.ticks_diff(time.ticks_us(), t) < 0:
            pass
    speaker.duty_u16(0)

def play_drop():
    play_sample(drop_samples)

def play_tow():
    play_sample(tow_samples)

def play_er():
    play_sample(er_samples)

# ---------- INPUT PINS (FROM GEN PICO) ----------

R_in = Pin(10, Pin.IN, Pin.PULL_DOWN)  # red line
G_in = Pin(11, Pin.IN, Pin.PULL_DOWN)  # green line
B_in = Pin(12, Pin.IN, Pin.PULL_DOWN)  # blue line

last_pattern = (-1, -1, -1)
busy = False

print("Sniffer ready on GP10/11/12")

while True:
    pattern = (R_in.value(), G_in.value(), B_in.value())

    if pattern != last_pattern:
        print("New pattern:", pattern)
        last_pattern = pattern

        if not busy:
            if pattern == (1, 0, 0):
                print("RED -> drop")
                busy = True
                play_drop()
                busy = False

            elif pattern == (0, 1, 0):
                print("GREEN -> tow")
                busy = True
                play_tow()
                busy = False

            elif pattern == (0, 0, 1):
                print("BLUE -> er")
                busy = True
                play_er()
                busy = False

            # everything else (off/mixes) ignored

    time.sleep(0.01)
