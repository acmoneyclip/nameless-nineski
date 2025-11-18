from machine import Pin, PWM
import time
from drop_samples import drop_samples

speaker = PWM(Pin(15))
SAMPLE_RATE = 8000
DT_US = int(1_000_000 / SAMPLE_RATE)

def play_sample(samples):
    speaker.freq(20000)
    t = time.ticks_us()
    for s in samples:
        speaker.duty_u16(s * 257)
        t = time.ticks_add(t, DT_US)
        while time.ticks_diff(time.ticks_us(), t) < 0:
            pass
    speaker.duty_u16(0)

print("PLAY TEST")
play_sample(drop_samples)
print("DONE")
