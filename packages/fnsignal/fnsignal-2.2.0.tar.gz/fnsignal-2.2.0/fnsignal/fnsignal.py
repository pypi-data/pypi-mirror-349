import time
import asyncio
import threading
import os
import logging
import sys
import traceback
import queue
import concurrent.futures
from typing import Optional, Callable, Dict, Set, List, Any, Union
from contextlib import contextmanager
from functools import wraps
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
from collections import defaultdict

# 로깅 설정
def setup_logging(
    level: int = logging.INFO,
    log_file: str = 'fnsignal.log',
    enable_console: bool = True,
    enable_file: bool = True,
    format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> None:
    """
    로깅 설정을 구성합니다.
    
    Args:
        level (int): 로깅 레벨
        log_file (str): 로그 파일 경로
        enable_console (bool): 콘솔 출력 활성화 여부
        enable_file (bool): 파일 출력 활성화 여부
        format_str (str): 로그 포맷 문자열
    """
    handlers = []
    
    if enable_console:
        handlers.append(logging.StreamHandler(sys.stdout))
    if enable_file:
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
        
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=handlers
    )

# 기본 로깅 설정
setup_logging()
logger = logging.getLogger(__name__)

class SignalPriority(Enum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()

@dataclass
class SignalCallback:
    callback: Callable
    sender: Optional[str]
    priority: SignalPriority
    is_async: bool
    filter_condition: Optional[Callable[[Any], bool]]
    stop_propagation: bool = False
    registered_at: datetime = field(default_factory=datetime.now)
    execution_count: int = 0
    total_execution_time: float = 0.0
    max_execution_time: float = 0.0
    error_count: int = 0
    
    def update_stats(self, execution_time: float, error: bool = False) -> None:
        self.execution_count += 1
        self.total_execution_time += execution_time
        self.max_execution_time = max(self.max_execution_time, execution_time)
        if error:
            self.error_count += 1
    
    @property
    def average_execution_time(self) -> float:
        return self.total_execution_time / self.execution_count if self.execution_count > 0 else 0.0
    
    @property
    def error_rate(self) -> float:
        return self.error_count / self.execution_count if self.execution_count > 0 else 0.0

@dataclass
class SignalStats:
    total_signals: int = 0
    active_callbacks: int = 0
    last_signal_time: Optional[datetime] = None
    signal_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    error_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    execution_times: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))
    total_execution_time: float = 0.0
    max_execution_time: float = 0.0
    
    def update_execution_time(self, execution_time: float) -> None:
        self.total_execution_time += execution_time
        self.max_execution_time = max(self.max_execution_time, execution_time)
    
    @property
    def average_execution_time(self) -> float:
        return self.total_execution_time / self.total_signals if self.total_signals > 0 else 0.0

class SignalManager:
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._callbacks: Dict[str, List[SignalCallback]] = defaultdict(list)
                    self._stats = SignalStats()
                    self._signal_queue = queue.PriorityQueue()
                    self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
                    self._running = True
                    self._event_loop = None
                    self._processing_thread = threading.Thread(target=self._process_signals, daemon=True)
                    self._processing_thread.start()
                    self._initialized = True

    def _ensure_event_loop(self):
        if self._event_loop is None or self._event_loop.is_closed():
            self._event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._event_loop)
        return self._event_loop

    def _process_signals(self):
        while self._running:
            try:
                priority, (signal_name, data, sender) = self._signal_queue.get(timeout=0.1)
                self._execute_callbacks(signal_name, data, sender)
                self._signal_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Signal processing error: {e}")

    def _execute_callbacks(self, signal_name: str, data: Any, sender: Any):
        callbacks = self._callbacks.get(signal_name, [])
        for callback in callbacks:
            try:
                if callback.filter_condition and not callback.filter_condition(data):
                    continue

                start_time = time.time()
                if callback.is_async:
                    loop = self._ensure_event_loop()
                    future = asyncio.run_coroutine_threadsafe(
                        callback.callback(signal_name, data, sender),
                        loop
                    )
                    try:
                        future.result(timeout=30)  # 30초 타임아웃
                    except concurrent.futures.TimeoutError:
                        logger.error(f"Async callback timeout: {signal_name}")
                        callback.update_stats(time.time() - start_time, error=True)
                        continue
                else:
                    self._executor.submit(callback.callback, signal_name, data, sender)

                execution_time = time.time() - start_time
                callback.update_stats(execution_time)
                self._stats.execution_times[signal_name].append(execution_time)
                self._stats.total_signals += 1
                self._stats.signal_counts[signal_name] += 1
                self._stats.last_signal_time = datetime.now()

                if callback.stop_propagation:
                    break

            except Exception as e:
                logger.error(f"Callback execution error: {e}")
                callback.update_stats(time.time() - start_time, error=True)
                self._stats.error_counts[signal_name] += 1

    def register_callback(
        self,
        signal_name: str,
        callback: Callable,
        sender: Any = None,
        priority: SignalPriority = SignalPriority.NORMAL,
        filter_condition: Optional[Callable] = None,
        stop_propagation: bool = False
    ):
        with self._lock:
            callback_obj = SignalCallback(
                callback=callback,
                sender=sender,
                priority=priority,
                is_async=asyncio.iscoroutinefunction(callback),
                filter_condition=filter_condition,
                stop_propagation=stop_propagation
            )
            self._callbacks[signal_name].append(callback_obj)
            self._callbacks[signal_name].sort(key=lambda x: x.priority.value, reverse=True)
            self._stats.active_callbacks += 1

    def unregister_callback(self, signal_name: str, callback: Callable):
        with self._lock:
            if signal_name in self._callbacks:
                self._callbacks[signal_name] = [
                    cb for cb in self._callbacks[signal_name]
                    if cb.callback != callback
                ]
                self._stats.active_callbacks -= 1

    def send_signal(
        self,
        signal_name: str,
        data: Any = None,
        sender: Any = None,
        priority: SignalPriority = SignalPriority.NORMAL
    ):
        priority_value = {
            SignalPriority.LOW: 3,
            SignalPriority.NORMAL: 2,
            SignalPriority.HIGH: 1,
            SignalPriority.CRITICAL: 0
        }[priority]
        self._signal_queue.put((priority_value, (signal_name, data, sender)))

    def get_signal_stats(self) -> SignalStats:
        return self._stats

    def reset_signal_stats(self):
        with self._lock:
            self._stats = SignalStats()

    def shutdown(self):
        self._running = False
        self._processing_thread.join()
        self._executor.shutdown(wait=True)
        if self._event_loop and not self._event_loop.is_closed():
            self._event_loop.close()

# 싱글톤 인스턴스 생성
signal_manager = SignalManager()