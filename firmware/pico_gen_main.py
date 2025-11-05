# PICO_GEN1 (left board) - "drop tower" signal generator
# GPIO16 (pin 21) -> Din_Gen -> LED strip + other Pico

from machine import Pin
import time

DIN_PIN = 16  # GPIO16

din = Pin(DIN_PIN, Pin.OUT)
din.value(0)

# Simple pattern: HIGH for 1s every 5s
# You can change these timings or replace with LED-strip code later.
HIGH_TIME = 1.0   # seconds Din is HIGH
LOW_TIME  = 4.0   # seconds Din is LOW between events

while True:
    # Idle period
    din.value(0)
    time.sleep(LOW_TIME)

    # "Drop event" starts: line goes high, LED strip would turn on
    din.value(1)
    time.sleep(HIGH_TIME)

    # End event
    din.value(0)
    # loop repeats
