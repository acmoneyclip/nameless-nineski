import wave

with wave.open("drop.wav", "rb") as w:
    print("channels:", w.getnchannels())
    print("width:", w.getsampwidth())
    print("rate:", w.getframerate())
    assert w.getnchannels() == 1
    assert w.getsampwidth() == 1
    assert w.getframerate() == 8000

    n = w.getnframes()
    frames = w.readframes(n)

samples = list(frames)

print("drop_samples = [")
for i, s in enumerate(samples):
    if i % 16 == 0:
        print("    ", end="")
    print(s, end=", ")
    if i % 16 == 15:
        print()
print("]")
