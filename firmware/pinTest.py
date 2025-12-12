import machine, time

pin = machine.Pin(27, machine.Pin.IN)

print("Sampling GP27 (Ctrl+C to stop)...")
while True:
    # 80 fast samples
    s = ''.join('1' if pin.value() else '0' for _ in range(80))
    print(s)
    time.sleep(0.1)
