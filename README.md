# An experimental real-time 3D engine for PewPew

Video: https://twitter.com/isziaui/status/1122519819180548096

## Installation

Copy _maze3d.py_ and _m3dlevel.bmp_ to your PewPew. It should run on all [PewPew](https://pewpew.readthedocs.io/) devices using either CircuitPython or MicroPython. On CircuitPython, firmware version 4.1.0 (in beta at the time of writing) or later is recommended for best performance ([update instructions for the PewPew 10 series](https://pewpew.readthedocs.io/en/latest/pewpew10/hardware.html#updating-the-firmware)). Try different levels by renaming the other BMPs to _m3dlevel.bmp_, or make your own.

## Level format

A level is defined by a 4-bit indexed BMP image with a color palette of exactly 16 colors and a size of exactly 64 × 64 pixels. The image is infinitely tiled (wrapped into a torus), so you can see and walk across the edges. The player starts out in the center of the image, looking north (up). The first color in the palette represents open space, the rest are walls of different textures. A texture is 1 pixel wide and 4 pixels high and is defined by the blue component of the color in the palette. The red and green components are ignored. Of the 8 bits of the blue component, the most significant two specify the bottom pixel, and so on until the least significant two for the top pixel, in the usual PewPew color map of 0=black, 1=green, 2=red, 3=orange (on two-color displays) or 0=black to 3=brightest (on monochrome displays).
