"""
fnsignal - A powerful function signal system for Python
"""

__version__ = "2.3.0"

from .fnsignal import (
    signal_manager,
    SignalPriority,
    SignalCallback,
    SignalStats
)

__all__ = [
    "signal_manager",
    "SignalPriority",
    "SignalCallback",
    "SignalStats"
]

# 패키지 레벨에서 함수들을 직접 사용할 수 있게 함
__all__ = [
    "signal_manager",
    "SignalPriority",
    "SignalCallback",
    "SignalStats"
]

# 패키지 레벨에 함수들을 직접 할당
globals().update({
    "signal_manager": signal_manager,
    "SignalPriority": SignalPriority,
    "SignalCallback": SignalCallback,
    "SignalStats": SignalStats
}) 