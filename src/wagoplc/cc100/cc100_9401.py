from wagoplc.cc100.cc100_v1 import CC100_v1

class CC100_9401(CC100_v1):
    DOUT_DATA="/sys/hallo"
    def __init__(self):
        super().__init__()
        print(CC100_9401.DOUT_DATA)


cc2 = CC100_9401()

print(cc2.get_path())