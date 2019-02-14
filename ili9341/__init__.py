from ili9341.ili9341 import ILI9341

def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3
