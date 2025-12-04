import machine, time, array
from rp2 import PIO, StateMachine, asm_pio

# --------- PINS ---------
DIN_PIN = 27               # data line from GEN (through 220R)
BUTTON_PIN = 19            # learn button
LED = machine.Pin("LED", machine.Pin.OUT)

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

# --------- PIO sampler: 1-bit samples -> 32-bit words ---------
NUM_WORDS = 256           # 256 * 32 = 8192 raw samples

@asm_pio(autopush=True, push_thresh=32)
def logic_sampler():
    wrap_target()
    in_(pins, 1)          # sample DIN_PIN
    wrap()

sm = StateMachine(
    0,
    logic_sampler,
    freq=5_000_000,       # 5 MHz sampling
    in_base=machine.Pin(DIN_PIN)   # GP27
)

def capture_words():
    buf = array.array("I", [0] * NUM_WORDS)
    sm.active(1)
    for i in range(NUM_WORDS):
        buf[i] = sm.get()
    sm.active(0)
    return buf

# ---- convert raw samples -> cleaned bitstream ----

def words_to_bits(words):
    bits = []
    for w in words:
        for i in range(32):               # MSB first
            bits.append((w >> (31 - i)) & 1)
    return bits

def measure_high_pulses(bits):
    pulses = []
    cur = 0
    for b in bits:
        if b:
            cur += 1
        elif cur:
            pulses.append(cur)
            cur = 0
    if cur:
        pulses.append(cur)
    return pulses

def pulses_to_bits(pulses):
    """
    Turn high pulse lengths into logical 0/1 bits.

    From your histogram:
      1 sample  -> noise -> ignore
      2 samples -> short -> 0
      >=3       -> long  -> 1
    """
    out = []
    for n in pulses:
        if n == 1:
            continue
        elif n == 2:
            out.append(0)
        else:
            out.append(1)
    return out

# --------- decode first pixel's GRB bytes ---------

def bits_to_byte(bits8):
    v = 0
    for b in bits8:
        v = (v << 1) | (b & 1)
    return v

def capture_pixel_once(debug=False):
    """Capture once and try to extract first pixel's GRB."""
    words = capture_words()
    raw_bits = words_to_bits(words)
    pulses = measure_high_pulses(raw_bits)
    clean_bits = pulses_to_bits(pulses)

    if debug:
        print("  DEBUG: pulses =", len(pulses),
              "bits_raw =", len(raw_bits),
              "bits_clean =", len(clean_bits))

    if len(clean_bits) < 24:
        return None  # not enough bits for even one pixel

    # We don't know bit alignment; try all 24 phase offsets
    best_pixel = None
    best_score = -1

    max_offset = min(24, len(clean_bits) - 24)
    for offset in range(max_offset):
        g_bits = clean_bits[offset       : offset + 8]
        r_bits = clean_bits[offset +  8  : offset + 16]
        b_bits = clean_bits[offset + 16  : offset + 24]

        G = bits_to_byte(g_bits)
        R = bits_to_byte(r_bits)
        B = bits_to_byte(b_bits)

        score = G + R + B  # brightness heuristic
        if score > best_score:
            best_score = score
            best_pixel = (G, R, B, offset)

    if best_pixel is None:
        return None

    return best_pixel  # (G,R,B,offset)

def capture_pixel_reliable(debug=False):
    """
    Try up to N times to get a non-None pixel decode.
    This avoids the 'too few bits' corner case.
    """
    for _ in range(8):
        px = capture_pixel_once(debug=debug)
        if px is not None:
            return px
    return None

# --------- matching logic ---------

def manhattan_dist(p1, p2):
    G1, R1, B1 = p1
    G2, R2, B2 = p2
    return abs(G1 - G2) + abs(R1 - R2) + abs(B1 - B2)

DIST_THRESH = 100   # tweak: 80–120 seems good from your logs
CHECK_PERIOD_MS = 250

target_pixel = None
last_button = 0
last_match = False

print("Sniffer ready (byte mode, NO AUDIO).")
print(" - Press button on GP19 while your desired color is ON.")
print(" - Sniffer will remember first pixel's GRB bytes.")
print(" - It will print current bytes and distance every check.\n")

# --------- main loop ---------

while True:
    # --- learn on button rising edge ---
    btn = button.value()
    if btn and not last_button:
        print("=== LEARNING PIXEL ===")
        px = capture_pixel_reliable(debug=True)
        if px is None:
            print("Could not decode pixel – too few bits.")
        else:
            G, R, B, off = px
            target_pixel = (G, R, B)
            print("Learned target pixel: G=%3d R=%3d B=%3d (offset=%d)" %
                  (G, R, B, off))
            LED.value(1)
            time.sleep_ms(120)
            LED.value(0)
    last_button = btn

    # --- monitor current pixel and compare ---
    px = capture_pixel_reliable(debug=False)
    if px is not None and target_pixel is not None:
        G, R, B, off = px
        cur = (G, R, B)
        d = manhattan_dist(cur, target_pixel)

        msg = "MON: G=%3d R=%3d B=%3d d=%3d" % (G, R, B, d)
        if d <= DIST_THRESH:
            msg += "  <- MATCH"
            if not last_match:
                # blink LED 3x on *new* match
                for _ in range(3):
                    LED.value(1)
                    time.sleep_ms(70)
                    LED.value(0)
                    time.sleep_ms(70)
                last_match = True
        else:
            last_match = False

        print(msg)

    time.sleep_ms(CHECK_PERIOD_MS)
