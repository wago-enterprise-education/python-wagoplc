from wagoplc.cc100.cc100_v1 import CC100_v1
from wagoplc.plc import NonExistingIOError
class CC100_9403(CC100_v1):
    DIN = "/sys/devices/platform/soc/44009000.spi/spi_master/spi1/spi1.0/din"

    def __init__(self):
        super().__init__()

    def analogRead(self, input: int)-> int|bool:
        raise NonExistingIOError("The 751-9403 has no analog inputs.")