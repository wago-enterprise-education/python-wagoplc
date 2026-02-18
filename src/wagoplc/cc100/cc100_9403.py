from wagoplc.cc100.cc100_v1 import CC100_v1

class CC100_9403(CC100_v1):
    DIN="/sys/devices/platform/soc/44009000.spi/spi_master/spi1/spi1.0/din"
    def __init__(self):
        super().__init__()
        print(CC100_9403.DIN)


cc3 = CC100_9403()

#print(cc3.get_path())