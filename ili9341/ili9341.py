# This is an adapted version of the ILI934X driver as below.
# It works with multiple fonts and also works with the esp32 H/W SPI implementation
# Also includes a word wrap print function
# Proportional fonts are generated by Peter Hinch's Font-to-py 
# MIT License; Copyright (c) 2017 Jeffrey N. Magee

# This file is part of MicroPython ILI934X driver
# Copyright (c) 2016 - 2017 Radomir Dopieralski, Mika Tuupola
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#
# Project home:
#   https://github.com/tuupola/micropython-ili934x

from time import sleep_ms
from ustruct import pack
from ili9341.fonts import glcdfont
from framebuf import FrameBuffer, MONO_VLSB

from machine import Pin

from ili9341.constants import *
from hwspi.hwspi import HWSPI


class ILI9341:

    def __init__(self, busid, cs, dc, rst = None, baudrate = DEFAULT_BAUDRATE,
        height = DEFAULT_HEIGHT, width = DEFAULT_WIDTH,
        madctl = DEFAULT_MADCTL, **kwargs):
        """ Setup and Initialize Display. """
        self.spi = HWSPI(busid = busid, cs = cs, baudrate = baudrate, **kwargs)

        if dc is None:
            raise RuntimeError('ILI9341 must be initialized with a dc pin number')
        self.dc = Pin(dc, Pin.OUT, value=0)

        self.rst = None
        if rst is not None:
            self.rst = Pin(rst, Pin.OUT, value=0)

        self.height = height
        self.width = width
        self.madctl = pack('>B', madctl)

        self.reset()
        self.init()

        self._scroll = 0
        self._buf = bytearray(CHUNK * 2)
        self._colormap = bytearray(b'\x00\x00\xFF\xFF') #default white foregraound, black background
        self._x = 0
        self._y = 0
        self._font = glcdfont
        self.scrolling = False
    
    def set_color(self, fg, bg):
        self._colormap[0] = bg>>8
        self._colormap[1] = bg & 255
        self._colormap[2] = fg>>8
        self._colormap[3] = fg & 255
    
    def set_pos(self,x,y):
        self._x = x
        self._y = y
    
    def reset_scroll(self):
        self.scrolling = False
        self._scroll = 0
        self.scroll(0)
    
    def set_font(self, font):
        self._font = font
    
    def init(self):
        for command, data in (
            (RDDSDR, b"\x03\x80\x02"),
            (PWCTLB, b"\x00\xc1\x30"),
            (PWRONCTL, b"\x64\x03\x12\x81"),
            (DTCTLA, b"\x85\x00\x78"),
            (PWCTLA, b"\x39\x2c\x00\x34\x02"),
            (PRCTL, b"\x20"),
            (DTCTLB, b"\x00\x00"),
            (PWCTL1, b"\x23"),
            (PWCTL1, b"\x10"),
            (VMCTL1, b"\x3e\x28"),
            (VMCTL2, b"\x86"),
            (PIXSET, b"\x55"),
            (FRMCTL1, b"\x00\x18"),
            (DISCTL, b"\x08\x82\x27"),
            (ENA3G, b"\x00"),
            (GAMMASET, b"\x01"),
            (PGAMCTL, b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"),
            (NGAMCTL, b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f"),
            (MADCTL, self.madctl)):
            self._write(command, data)
        self._write(SLPOUT)
        sleep_ms(120)
        self._write(DISPON)
        sleep_ms(50)

    def reset(self):
        if self.rst is None:
            self._write(SWRESET)
            sleep_ms(50)
            return

        self.rst(0)
        sleep_ms(50)
        self.rst(1)
        sleep_ms(50)

    def _write(self, command, data = None):
        with self.spi as spi:
            self.dc(0)
            spi.write(bytearray([command]))
        if data is not None:
            self._data(data)

    def _data(self, data):
        with self.spi as spi:
            self.dc(1)
            spi.write(data)

    def _writeblock(self, x0, y0, x1, y1, data=None):
        self._write(CASET, pack(">HH", x0, x1))
        self._write(PASET, pack(">HH", y0, y1))
        self._write(RAMWR, data)

    def _readblock(self, x0, y0, x1, y1):
        self._write(CASET, pack(">HH", x0, x1))
        self._write(PASET, pack(">HH", y0, y1))
        if data is None:
            return self._read(RAMRD, (x1 - x0 + 1) * (y1 - y0 + 1) * 3)

    def _read(self, command, count):
        with self.spi as spi:
            self.dc(0)
            spi.write(bytearray([command]))
            data = spi.read(count)
        return data

    def pixel(self, x, y, color=None):
        if color is None:
            r, b, g = self._readblock(x, y, x, y)
            return color565(r, g, b)
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return
        self._writeblock(x, y, x, y, pack(">H", color))

    def fill_rectangle(self, x, y, w, h, color = None):
        x = min(self.width - 1, max(0, x))
        y = min(self.height - 1, max(0, y))
        w = min(self.width - x, max(1, w))
        h = min(self.height - y, max(1, h))
        if color:
            color = pack(">H", color)
        else:
            color = self._colormap[0:2] #background
        for i in range(CHUNK):
            self._buf[2*i]=color[0]; self._buf[2*i+1]=color[1]
        chunks, rest = divmod(w * h, CHUNK)
        self._writeblock(x, y, x + w - 1, y + h - 1, None)
        if chunks:
            for count in range(chunks):
                self._data(self._buf)
        if rest != 0:
            mv = memoryview(self._buf)
            self._data(mv[:rest*2])

    def erase(self):
        self.fill_rectangle(0, 0, self.width, self.height)
        
    def blit(self, bitbuff, x, y, w, h):
        x = min(self.width - 1, max(0, x))
        y = min(self.height - 1, max(0, y))
        w = min(self.width - x, max(1, w))
        h = min(self.height - y, max(1, h))
        chunks, rest = divmod(w * h, CHUNK)
        self._writeblock(x, y, x + w - 1, y + h - 1, None)
        written = 0
        for iy in range(h):
            for ix in range(w):
                index = ix+iy*w - written
                if index >= CHUNK:
                    self._data(self._buf)
                    written += CHUNK
                    index   -= CHUNK
                c = bitbuff.pixel(ix,iy)
                self._buf[index*2] = self._colormap[c*2]
                self._buf[index*2+1] = self._colormap[c*2+1]
        rest = w*h - written
        if rest != 0:
            mv = memoryview(self._buf)
            self._data(mv[:rest*2])
    
    def chars(self, str, x, y):
        str_w  = self._font.get_width(str)
        div, rem = divmod(self._font.height(),8)
        nbytes = div+1 if rem else div
        buf = bytearray(str_w * nbytes)
        pos = 0
        for ch in str:
            glyph, char_w = self._font.get_ch(ch)
            for row in range(nbytes):
                index = row*str_w + pos
                for i in range(char_w):
                    buf[index+i] = glyph[nbytes*i+row]
            pos += char_w
        fb = FrameBuffer(buf, str_w, self._font.height(), MONO_VLSB)
        self.blit(fb, x, y, str_w, self._font.height())
        return x + str_w

    def scroll(self, dy):
        self._scroll = (self._scroll + dy) % self.height
        self._write(VSCRSADD, pack(">H", self._scroll))

    def next_line(self, cury, char_h):
        global scrolling
        if not self.scrolling:
            res = cury + char_h
            self.scrolling = (res >= self.height)
        if self.scrolling:
            self.scroll(char_h)
            res = (self.height - char_h + self._scroll)%self.height
            self.fill_rectangle(0, res, self.width, self._font.height())
        return res

    def write(self, text): #does character wrap, compatible with stream output
        curx = self._x; cury = self._y
        char_h = self._font.height()
        width = 0
        written = 0
        for pos, ch in enumerate(text):
            if ch == '\n':
                if pos>0:
                    self.chars(text[written:pos],curx,cury)
                curx = 0; written = pos+1; width = 0
                cury = self.next_line(cury,char_h)
            else:
                char_w = self._font.get_width(ch)
                if curx + width + char_w >= self.width:
                    self.chars(text[written:pos], curx,cury)
                    curx = 0 ; written = pos; width = char_h
                    cury = self.next_line(cury,char_h)
                else:
                    width += char_w
        if written<len(text):
            curx = self.chars(text[written:], curx,cury)
        self._x = curx; self._y = cury


    def print(self, text): #does word wrap, leaves self._x unchanged
        cury = self._y; curx = self._x
        char_h = self._font.height()
        char_w = self._font.max_width()
        lines = text.split('\n')
        for line in lines:
            words = line.split(' ')
            for word in words:
                if curx + self._font.get_width(word) >= self.width:
                    curx = self._x; cury = self.next_line(cury,char_h)
                    while self._font.get_width(word) > self.width:
                        self.chars(word[:self.width//char_w],curx,cury)
                        word = word[self.width//char_w:]
                        cury = self.next_line(cury,char_h)
                if len(word)>0:
                    curx = self.chars(word+' ', curx,cury)
            curx = self._x; cury = self.next_line(cury,char_h)
        self._y = cury
