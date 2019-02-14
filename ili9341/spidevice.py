from machine import Pin, SPI

from ili9341.constants import DEFAULT_BAUDRATE, DEFAULT_CS_PIN, DEFAULT_SPI_BUS
from ili9341.constants import BUSPINS, HSPI, VSPI

class SPIDevice:
    """ Python3 style SPI device implementation.
    """
    def __init__(self, busid = DEFAULT_SPI_BUS, cs = DEFAULT_CS_PIN,
                 baudrate = DEFAULT_BAUDRATE, sck = None, mosi = None,
                 miso = None, **kwargs):
        if busid not in [HSPI, VSPI]:
            raise RuntimeError('SPIDevice `busid?` must be `HSPI` or `VSPI`')
        if cs is None:
            raise RuntimeError('`cs` pin number is a mandatory SPIDevice parameter')

        if sck is None:
            sck = Pin(BUSPINS[busid]['sck'])
        if mosi is None:
            mosi = Pin(BUSPINS[busid]['mosi'])
        if miso is None:
            miso = Pin(BUSPINS[busid]['miso'])
        self.spi = SPI(busid, baudrate = baudrate, sck = sck, mosi = mosi, miso = miso, **kwargs)
        self.cs = Pin(cs, Pin.OUT, value = 1)

    def __enter__(self):
        self.cs(0)
        return self.spi

    def __exit__(self, exc_type, exc_value, traceback):
        self.cs(1)
        return exc_type is None
