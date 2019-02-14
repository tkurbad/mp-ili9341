# test of printing multiple fonts to the ILI9341 on an M5Stack using H/W SP
# MIT License; Copyright (c) 2017 Jeffrey N. Magee

from ili9341 import ILI9341, color565
from ili9341.fonts import tt14
from ili9341.fonts import glcdfont
from ili9341.fonts import tt14
from ili9341.fonts import tt24
from ili9341.fonts import tt32

fonts = [glcdfont, tt14, tt24, tt32]

text = 'Now is the time for all good men to come to the aid of the party.'

display = ILI9341(busid = 2, cs = 22, dc = 21, baudrate = 60000000)

display.erase()
display.set_pos(0, 0)
for ff in fonts:
    display.set_font(ff)
    display.print(text)
