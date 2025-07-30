"""
辅助测试的一些常用功能
"""

import warnings

from ._datetime_utils import DateTimeUtils, Timer
from ._fake_data_utils import FakeDataUtils
from ._network_utils import NetworkUtils
from ._path_utils import PathUtils
from ._random_utils import RandomUtils

__all__: list[str] = [
    "Timer",
    "DateTimeUtils",
    "RandomUtils",
    "NetworkUtils",
    "PathUtils",
    "FakeDataUtils",
]


def __getattr__(name):
    match name:
        case "Random":
            warnings.warn(
                "Random 已弃用，请改用 RandomUtils",
                DeprecationWarning,
                stacklevel=2,
            )
            from ._rand import Random

            return Random
        case "DateLib":
            warnings.warn(
                "DateLib 已弃用，请改用 DateTimeUtils",
                DeprecationWarning,
                stacklevel=2,
            )
            from ._date import DateLib

            return DateLib

        case "NetLib":
            warnings.warn(
                "NetLib 已弃用，请改用 NetworkUtils",
                DeprecationWarning,
                stacklevel=2,
            )
            from ._net import NetLib

            return NetLib
        case "DirLib":
            warnings.warn(
                "DirLib 已弃用，请改用 PathUtils",
                DeprecationWarning,
                stacklevel=2,
            )
            from ._path import DirLib

            return DirLib
        case "PathLib":
            warnings.warn(
                "PathLib 已弃用，请改用 PathUtils",
                DeprecationWarning,
                stacklevel=2,
            )
            from ._path import PathLib

            return PathLib

        case "Person":
            warnings.warn(
                "Person 已弃用，请改用 FakeDataUtils",
                DeprecationWarning,
                stacklevel=2,
            )
            from ._person import Person

            return Person

    raise AttributeError(f"module {__name__} has no attribute {name}")
