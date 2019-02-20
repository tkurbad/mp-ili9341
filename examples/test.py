# test of printing multiple fonts to the ILI9341 on an M5Stack using H/W SP
# MIT License; Copyright (c) 2017 Jeffrey N. Magee

from hwspi.hwspi import VSPI

from ili9341 import ILI9341, color565
from ili9341.fonts import tt14
from ili9341.fonts import glcdfont
from ili9341.fonts import tt14
from ili9341.fonts import tt24
from ili9341.fonts import tt32

fonts = [glcdfont, tt14, tt24, tt32]

text = 'Now is the time for all good men to come to the aid of the party.'

display = ILI9341(busid = VSPI, cs = 22, dc = 21, baudrate = 60000000)

display.erase()
#display.set_pos(0, 0)
#for ff in fonts:
#    display.set_font(ff)
#    display.print(text)

display.fill_rectangle(0, 300, 240, 320, color = color565(200, 200, 200))
display.set_color(color565(0, 0, 0), color565(200, 200, 200))
display.set_font(tt14)
x_extra = display._font.get_width(' ')
x_tc1 = display.chars('TC1', 10, 302) + x_extra
x_tc2 = display.chars('TC2', 90, 302) + x_extra
x_tc3 = display.chars('TC3', 170, 302) + x_extra
