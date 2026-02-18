from wagoplc.cc100.cc100_v1 import CC100_v1

class CC100_9301(CC100_v1):
    DOUT_DATA="/sys/hallo"
    def __init__(self):
        super().__init__()
        print(CC100_9301.DOUT_DATA)


cc1 = CC100_9301()

print(cc1.get_path())