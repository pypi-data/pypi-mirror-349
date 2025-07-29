from .fnsignal import (
    send_signal,
    receive_signal,
    receive_signal_async,
    wait_for_signals,
    register_callback,
    unregister_callback,
    unregister_all_callbacks,
    setup_logging,
    get_signal_stats,
    reset_signal_stats,
    SignalPriority
)

__version__ = "2.0.0"

# 패키지 레벨에서 함수들을 직접 사용할 수 있게 함
__all__ = [
    "send_signal",
    "receive_signal",
    "receive_signal_async",
    "wait_for_signals",
    "register_callback",
    "unregister_callback",
    "unregister_all_callbacks",
    "setup_logging",
    "get_signal_stats",
    "reset_signal_stats",
    "SignalPriority"
]

# 패키지 레벨에 함수들을 직접 할당
globals().update({
    "send_signal": send_signal,
    "receive_signal": receive_signal,
    "receive_signal_async": receive_signal_async,
    "wait_for_signals": wait_for_signals,
    "register_callback": register_callback,
    "unregister_callback": unregister_callback,
    "unregister_all_callbacks": unregister_all_callbacks,
    "setup_logging": setup_logging,
    "get_signal_stats": get_signal_stats,
    "reset_signal_stats": reset_signal_stats,
    "SignalPriority": SignalPriority
}) 