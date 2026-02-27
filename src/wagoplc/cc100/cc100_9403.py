from dataclasses import dataclass

from wagoplc.cc100.cc100_v1 import CC100_v1


DIN = "/sys/devices/platform/soc/44009000.spi/spi_master/spi1/spi1.0/din"

class CC100_9403(CC100_v1):

    def __init__(self):
        super().__init__()
