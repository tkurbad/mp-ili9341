## Constants
from micropython import const

# Maximum Number of Pixels per SPI Write
CHUNK = const(1024)

#   Miscelleanous Default Settings
DEFAULT_BAUDRATE = const(50000000)  # Default Baud Rate
DEFAULT_HEIGHT   = const(320)       # Default TFT Height
DEFAULT_WIDTH    = const(240)       # Default TFT Width
DEFAULT_CS_PIN   = const(22)        # Default Pin for TFT SPI Chip Select
DEFAULT_DC_PIN   = const(21)        # Default Pin for TFT D/C
DEFAULT_RST_PIN  = None             # Default Pin for TFT Reset
DEFAULT_MADCTL   = const(0x88)      # Default Memory Access Control
                                    #  This Controls Mirroring / Flipping
                                    #  of the Display

#   IlI9341 registers definitions

# LCD control registers
NOP         = const(0x00)   # No Operation
SWRESET     = const(0x01)   # Software Reset

# LCD Read status registers
RDDID       = const(0x04)   # Read Display Identification (24-Bit)
RDDST       = const(0x09)   # Read Display Status (32-Bit)
RDDPM       = const(0x0A)   # Read Display Power Mode (8-Bit)
RDDMADCTL   = const(0x0B)   # Read Display MADCTL (8-Bit)
RDPIXFMT    = const(0x0C)   # Read Display Pixel Format (8-Bit)
RDDIM       = const(0x0D)   # Read Display Image Format (3-Bit)
RDDSM       = const(0x0E)   # Read Display Signal Mode (8-Bit)
RDDSDR      = const(0x0F)   # Read Display Self-Diagnostic Result (8-Bit)
RDID1       = const(0xDA)   # Read ID1 (8-Bit)
RDID2       = const(0xDB)   # Read ID2 (8-Bit)
RDID3       = const(0xDC)   # Read ID3 (8-Bit)
RDID4       = const(0xD3)   # Read ID4 (8-Bit)

# LCD settings registers
SLPIN       = const(0x10)   # Enter Sleep Mode
SLPOUT      = const(0x11)   # Exit Sleep Mode

PTLON       = const(0x12)   # Partial Mode ON
NORON       = const(0x13)   # Partial Mode OFF, Normal Display mode ON

INVOFF      = const(0x20)   # Display Inversion Off
INVON       = const(0x21)   # Display Inversion On
GAMMASET    = const(0x26)   # Gamma Set
DISPOFF     = const(0x28)   # Display Off
DISPON      = const(0x29)   # Display On

CASET       = const(0x2A)   # Column Address Set
PASET       = const(0x2B)   # Page Address Set
RAMWR       = const(0x2C)   # Memory Write
RGBSET      = const(0x2D)   # Color Set
RAMRD       = const(0x2E)   # Memory Read

PTLAR       = const(0x30)   # Partial Area
VSCRDEF     = const(0x33)   # Vertical Scrolling Definition
MADCTL      = const(0x36)   # Memory Access Control
VSCRSADD    = const(0x37)   # Vertical Scrolling Start Address
IDMOFF      = const(0x38)   # Idle Mode Off
IDMON       = const(0x39)   # Idle Mode On
PIXSET      = const(0x3A)   # Pixel Format Set
RAMWCONT    = const(0x3C)   # Write Memory Continue
RAMRCONT    = const(0x3E)   # Read Memory Continue

WRDISBV     = const(0x51)   # Write Display Brightness
RDDISBV     = const(0x52)   # Read Display Brightness

IFMODE      = const(0xB0)   # RGB Interface Control
FRMCTL1     = const(0xB1)   # Frame Rate Control (In Normal Mode)
FRMCTL2     = const(0xB2)   # Frame Rate Control (In Idle Mode)
FRMCTL3     = const(0xB3)   # Frame Rate Control (In Partial Mode)
INVCTL      = const(0xB4)   # Frame Inversion Control
PRCCTL      = const(0xB5)   # Blanking Porch ControlVFP, VBP, HFP, HBP
DISCTL      = const(0xB6)   # Display Function Control
ETMOD       = const(0xB7)   # Entry mode set

PWCTL1      = const(0xC0)   # Power Control 1
PWCTL2      = const(0xC1)   # Power Control 2
VMCTL1      = const(0xC5)   # VCOM Control 1
VMCTL2      = const(0xC7)   # VCOM Control 2

PWCTLA      = const(0xCB)   # Power Control A
PWCTLB      = const(0xCF)   # Power Control B

PGAMCTL     = const(0xE0)   # Positive Gamma Control
NGAMCTL     = const(0xE1)   # Negative Gamma Control

DTCTLA      = const(0xE8)   # Driver Timing Control A
DTCTLB      = const(0xEA)   # Driver Timing Control B

PWRONCTL    = const(0xED)   # Power on Sequence Control

ENA3G       = const(0xF2)   # Enable Gamma Control
IFCTL       = const(0xF6)   # Interface Control
PRCTL       = const(0xF7)   # Pump Ratio Control
