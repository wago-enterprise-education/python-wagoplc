from wagoplc.cc100.cc100_v1 import CC100_v1
from wagoplc.controller import AI
from wagoplc.exceptions import NonExistingIOError

class CC100_9403(CC100_v1):
    DIN = "/sys/devices/platform/soc/44009000.spi/spi_master/spi1/spi1.0/din"

    def __init__(self):
        super().__init__()
        # The 751-9403 doesn't have analog inputs
        self.file_map.pop(AI)
        self.specs.pop(AI)

    def get_read_paths(self) -> tuple[str]:
        return (
            self.DIN,
            self.IN_VOLTAGE13_RAW,
            self.IN_VOLTAGE1_RAW,
        )

    def analogRead(self, input: int, module: str) -> None:
        raise NonExistingIOError("The 751-9403 has no analog inputs.")
