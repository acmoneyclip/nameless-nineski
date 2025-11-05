\# LED Sniffer Project Firmware (Revision 2)



This firmware supports the dual-Pico LED Sniffer circuit described in the Revision 2 schematic.



\## PICO\_GEN1 — Signal Generator

\*\*File:\*\* `pico\_gen\_main.py`  

Outputs a periodic digital pulse on GPIO16 (`Din\_Gen`) that simulates the LED data trigger signal.



\- Drives a single-wire digital LED input and the second Pico’s `Din` line.  

\- Default timing: HIGH = 1 s, LOW = 4 s.  

\- Represents a digital LED trigger, not three analog RGB channels.



\## PICO\_MAIN1 — Response Controller

\*\*File:\*\* `pico\_sound\_main.py`  

Listens for the digital trigger on its input pin and drives the speaker through a 2N3904 transistor.



\- Input: `Din`  

\- Output: `SPEAKER\_OUT` (PWM tone)  

\- Push button (`BTN\_IN`) can mute or test the speaker.  



\## Design Note

The LED\_RGB component in the schematic is treated as a \*\*digital single-wire LED\*\*, not a 3-channel analog RGB LED.  

Both programs are written for \*\*Raspberry Pi Pico V1\*\* using \*\*MicroPython\*\*.



