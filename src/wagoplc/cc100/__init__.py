"""Controller-specific functionality for the CC100.

This package consists of modules for all supported CC100 controllers.

Modules:

- cc100_v1: the older CC100 generation
- cc100_9301: CC100 751-9301
- cc100_9401: CC100 751-9401
- cc100_9403: CC100 751-9403
"""

from wagoplc.cc100.cc100_v1 import CC100_v1 as CC100_v1
from wagoplc.cc100.cc100_9301 import CC100_9301 as CC100_9301
from wagoplc.cc100.cc100_9401 import CC100_9401 as CC100_9401
from wagoplc.cc100.cc100_9403 import CC100_9403 as CC100_9403