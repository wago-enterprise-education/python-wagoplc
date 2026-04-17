"""
The CC100 751-9301 is the base version of the CC100 series. 
"""
from wagoplc.cc100.cc100_v1 import CC100_v1

class CC100_9301(CC100_v1):

    def __init__(self):
        super().__init__()