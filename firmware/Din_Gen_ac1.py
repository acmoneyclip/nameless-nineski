import machine, neopixel, time

PIN_NUM = 2          # GP2 -> 220R -> DIN
NUM_PIXELS = 8

pin = machine.Pin(PIN_NUM, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, NUM_PIXELS)

def set_color(r, g, b):
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)

def show_color_for_ms(name, r, g, b, duration_ms):
    print("GEN color:", name)
    set_color(r, g, b)
    end = time.ticks_add(time.ticks_ms(), duration_ms)
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        np.write()          # continuously send frames
        time.sleep_ms(1)

colors = [
    ("RED",   255,   0,   0),
    ("GREEN",   0, 255,   0),
    ("BLUE",    0,   0, 255),
    ("OFF",     0,   0,   0),
]

print("GEN: cycling colors on GP2")
while True:
    for name, r, g, b in colors:
        show_color_for_ms(name, r, g, b, 1500)   # 1.5 s per color
