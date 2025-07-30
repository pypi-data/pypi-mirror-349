"""
辅助测试的一些常用功能
"""

import warnings

warnings.simplefilter("default", DeprecationWarning)
from ._date import DateLib, Timer
from ._datetime_utils import DateTimeUtils, Timer
from ._fake_data_utils import FakeDataUtils
from ._net import NetLib
from ._network_utils import NetworkUtils
from ._path import DirLib, PathLib
from ._path_utils import PathUtils
from ._person import Person
from ._rand import Random
from ._random_utils import RandomUtils

__all__: list[str] = [
    "DateLib",
    "PathLib",
    "DirLib",
    "Random",
    "NetLib",
    "Person",
    "Timer",
    "DateTimeUtils",
    "RandomUtils",
    "NetworkUtils",
    "PathUtils",
    "FakeDataUtils",
]
