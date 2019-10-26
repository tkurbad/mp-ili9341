AMPY=ampy -p /dev/ttyUSB0
MPY_CROSS=../micropython/mpy-cross/mpy-cross -march=xtensa -X heapsize=111168 -O3


all:
	$(MPY_CROSS) ili9341/constants.py
	$(MPY_CROSS) ili9341/ili9341.py
	$(MPY_CROSS) ili9341/fonts/glcdfont.py
	$(MPY_CROSS) ili9341/fonts/tt14.py
	$(MPY_CROSS) ili9341/fonts/tt24.py
	$(MPY_CROSS) ili9341/fonts/tt32.py
	$(MPY_CROSS) ili9341/fonts/verdana16.py
	$(MPY_CROSS) ili9341/fonts/verdanab16.py

push:
	$(AMPY) put ili9341/__init__.py ili9341/__init__.py
	$(AMPY) put ili9341/constants.mpy ili9341/constants.mpy
	$(AMPY) put ili9341/ili9341.mpy ili9341/ili9341.mpy
	$(AMPY) put ili9341/fonts/__init__.py ili9341/fonts/__init__.py
	$(AMPY) put ili9341/fonts/glcdfont.mpy ili9341/fonts/glcdfont.mpy
	$(AMPY) put ili9341/fonts/tt14.mpy ili9341/fonts/tt14.mpy
	$(AMPY) put ili9341/fonts/tt24.mpy ili9341/fonts/tt24.mpy
	$(AMPY) put ili9341/fonts/tt32.mpy ili9341/fonts/tt32.mpy
	$(AMPY) put ili9341/fonts/verdana16.mpy ili9341/fonts/verdana16.mpy
	$(AMPY) put ili9341/fonts/verdanab16.mpy ili9341/fonts/verdanab16.mpy

clean:
	rm -rf *.mpy
