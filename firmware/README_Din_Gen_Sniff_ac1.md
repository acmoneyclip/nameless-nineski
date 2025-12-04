## DIN Generator (Din_Gen_ac1.py)

The DIN Generator runs on the **GEN** Pico and drives a NeoPixel ring from **GP2** (through a 220 Ω resistor).  
It continuously cycles all pixels through four states:

1. Red
2. Green
3. Blue
4. Off

For each state, it keeps sending the corresponding WS2812/NeoPixel data frame for about 1.5 seconds before moving to the next color.  
This creates a repeating test pattern on the DIN line that the sniffer Pico can observe.

---

## DIN Sniffer (Din_Sniff_ac1.py)

The DIN Sniffer runs on the **SNIFF** Pico and taps the same DIN line on **GP27** (through the same 220 Ω resistor node).  
It uses a PIO state machine to sample the WS2812 data stream and reconstruct the first pixel’s **G, R, B** byte values.

- A pushbutton on **GP19** is used to *learn* a color:
  - When you press the button, the sniffer captures a burst of DIN data, decodes the first pixel’s GRB values, and stores them as the **target color**.
- After learning, the sniffer:
  - Continuously captures and decodes new frames.
  - Computes the distance between the current pixel’s GRB values and the stored target.
  - Prints each decoded `(G, R, B)` along with a distance value.
  - Prints `← MATCH` (and blinks the on-board LED) whenever the distance is within a configurable threshold, meaning the incoming color is “close enough” to the learned color.

For best results, press the button **well inside** the time window when a single solid color (red, green, or blue) is active.  
Pressing during a transition between colors can produce noisy or less stable target values, which may lead to weaker or inconsistent matches.
