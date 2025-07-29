import time
import asyncio
import threading
from typing import Optional, Callable, Dict, Set, NoReturn, List, Any, Union
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
import logging
import sys
import traceback
from contextlib import contextmanager
from functools import wraps
from dataclasses import dataclass
from enum import Enum, auto
import time
from datetime import datetime

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
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class SignalCallback:
    callback: Callable
    sender: Optional[str]
    priority: SignalPriority
    is_async: bool
    filter_condition: Optional[Callable[[Any], bool]]
    stop_propagation: bool = False
    registered_at: datetime = None
    
    def __post_init__(self):
        if self.registered_at is None:
            self.registered_at = datetime.now()

@dataclass
class SignalStats:
    total_signals: int = 0
    total_callbacks: int = 0
    active_callbacks: int = 0
    last_signal_time: Optional[datetime] = None
    signal_counts: Dict[str, int] = None
    callback_counts: Dict[str, int] = None
    error_counts: Dict[str, int] = None
    
    def __post_init__(self):
        if self.signal_counts is None:
            self.signal_counts = {}
        if self.callback_counts is None:
            self.callback_counts = {}
        if self.error_counts is None:
            self.error_counts = {}

# 전역 변수로 시그널 상태 관리
_signal_sender: Optional[str] = None
_signal_received: bool = False
_signal_callbacks: Dict[str, List[SignalCallback]] = {}
_event_loop: Optional[asyncio.AbstractEventLoop] = None
_running_tasks: Set[asyncio.Task] = set()
_executor: Optional[ThreadPoolExecutor] = None
_lock: threading.Lock = threading.Lock()
_signal_queue: Queue = Queue()
_is_initializing: bool = False
_is_shutting_down: bool = False
_initialized: bool = False
_error_count: int = 0
_max_retries: int = 3
_task_lock: threading.Lock = threading.Lock()
_queue_lock: threading.Lock = threading.Lock()
_callback_lock: threading.Lock = threading.Lock()
_loop_lock: threading.Lock = threading.Lock()
_executor_lock: threading.Lock = threading.Lock()
_state_lock: threading.Lock = threading.Lock()
_init_lock: threading.Lock = threading.Lock()
_error_lock: threading.Lock = threading.Lock()
_signal_lock: threading.Lock = threading.Lock()
_stats: SignalStats = SignalStats()

def get_signal_stats() -> SignalStats:
    """
    현재 시그널 시스템의 통계 정보를 반환합니다.
    
    Returns:
        SignalStats: 시그널 시스템 통계 정보
    """
    with _callback_lock:
        _stats.active_callbacks = sum(len(callbacks) for callbacks in _signal_callbacks.values())
    return _stats

def reset_signal_stats() -> None:
    """시그널 시스템의 통계 정보를 초기화합니다."""
    global _stats
    _stats = SignalStats()

@contextmanager
def _error_handler(operation: str):
    """에러 처리를 위한 컨텍스트 매니저"""
    global _error_count
    try:
        yield
        with _error_lock:
            _error_count = 0  # 성공 시 에러 카운트 리셋
    except Exception as e:
        with _error_lock:
            _error_count += 1
            logger.error(f"{operation} 중 오류 발생: {e}\n{traceback.format_exc()}")
            if _error_count >= _max_retries:
                logger.critical(f"최대 재시도 횟수({_max_retries})를 초과했습니다. 시스템을 재초기화합니다.")
                _initialize()
                _error_count = 0
        raise

def _safe_operation(func: Callable) -> Callable:
    """안전한 작업 실행을 위한 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with _error_handler(func.__name__):
            return func(*args, **kwargs)
    return wrapper

def _initialize() -> None:
    """전역 변수들을 초기화합니다."""
    global _signal_sender, _signal_received, _signal_callbacks, _event_loop, _running_tasks, _executor
    global _is_initializing, _is_shutting_down, _initialized, _error_count
    
    with _init_lock:
        if _is_initializing:
            return
        with _state_lock:
            _is_initializing = True
            _is_shutting_down = True
        
        try:
            # 진행 중인 작업이 있다면 완료될 때까지 대기
            with _loop_lock:
                if _event_loop is not None and not _event_loop.is_closed():
                    try:
                        # 이벤트 루프가 실행 중이 아닐 때만 run_until_complete 호출
                        if not _event_loop.is_running():
                            _event_loop.run_until_complete(asyncio.sleep(0.1))
                    except Exception as e:
                        logger.error(f"이벤트 루프 대기 중 오류 발생: {e}\n{traceback.format_exc()}")
            
            # 실행 중인 태스크 취소
            with _task_lock:
                for task in _running_tasks:
                    if not task.done():
                        task.cancel()
                        try:
                            with _loop_lock:
                                if _event_loop is not None and not _event_loop.is_closed():
                                    if not _event_loop.is_running():
                                        _event_loop.run_until_complete(task)
                        except asyncio.CancelledError:
                            pass
                        except Exception as e:
                            logger.error(f"태스크 취소 중 오류 발생: {e}\n{traceback.format_exc()}")
            
            # 이벤트 루프 종료
            with _loop_lock:
                if _event_loop is not None and not _event_loop.is_closed():
                    try:
                        if not _event_loop.is_running():
                            _event_loop.stop()
                        _event_loop.close()
                    except Exception as e:
                        logger.error(f"이벤트 루프 종료 중 오류 발생: {e}\n{traceback.format_exc()}")
            
            # ThreadPoolExecutor 종료
            with _executor_lock:
                if _executor is not None:
                    try:
                        _executor.shutdown(wait=True)
                    except Exception as e:
                        logger.error(f"ThreadPoolExecutor 종료 중 오류 발생: {e}\n{traceback.format_exc()}")
            
            # 상태 초기화
            with _signal_lock:
                _signal_sender = None
                _signal_received = False
            with _callback_lock:
                _signal_callbacks.clear()
            with _loop_lock:
                _event_loop = None
            with _task_lock:
                _running_tasks.clear()
            with _executor_lock:
                _executor = ThreadPoolExecutor(max_workers=1)
            with _error_lock:
                _error_count = 0
            
            # 시그널 큐 초기화
            with _queue_lock:
                while not _signal_queue.empty():
                    try:
                        _signal_queue.get_nowait()
                    except Empty:
                        break
                    except Exception as e:
                        logger.error(f"시그널 큐 초기화 중 오류 발생: {e}\n{traceback.format_exc()}")
                        break
                
        except Exception as e:
            logger.error(f"초기화 중 오류 발생: {e}\n{traceback.format_exc()}")
        finally:
            with _state_lock:
                _is_initializing = False
                _is_shutting_down = False
                _initialized = True

@_safe_operation
def send_signal(
    signal_name: str,
    data: Any = None,
    sender: Optional[str] = None,
    priority: SignalPriority = SignalPriority.NORMAL
) -> None:
    """
    시그널을 발신합니다.
    
    Args:
        signal_name (str): 시그널 이름
        data (Any): 시그널과 함께 전달할 데이터
        sender (Optional[str]): 시그널 발신자
        priority (SignalPriority): 시그널 우선순위
    """
    if not _initialized:
        _initialize()
        
    with _state_lock:
        if _is_shutting_down:
            logger.warning("시스템이 종료 중이어서 시그널을 보낼 수 없습니다.")
            return
        
    global _signal_sender, _signal_received, _stats
    with _lock:
        try:
            with _signal_lock:
                _signal_sender = sender
                _signal_received = True
            with _queue_lock:
                _signal_queue.put((signal_name, data, sender, priority))
                
            # 통계 업데이트
            _stats.total_signals += 1
            _stats.last_signal_time = datetime.now()
            _stats.signal_counts[signal_name] = _stats.signal_counts.get(signal_name, 0) + 1
            
            logger.debug(f"시그널 전송: {signal_name} (발신자: {sender}, 우선순위: {priority.name})")
        except Exception as e:
            logger.error(f"시그널 전송 중 오류 발생: {e}\n{traceback.format_exc()}")
            _stats.error_counts["send_signal"] = _stats.error_counts.get("send_signal", 0) + 1
            raise

async def _execute_callback(callback: SignalCallback, data: Any) -> None:
    """콜백을 실행합니다."""
    start_time = time.time()
    try:
        if callback.is_async:
            await callback.callback(data)
        else:
            with _loop_lock, _executor_lock:
                if _event_loop is not None and not _event_loop.is_closed() and _executor is not None:
                    await _event_loop.run_in_executor(_executor, callback.callback, data)
        
        execution_time = time.time() - start_time
        logger.debug(
            f"콜백 실행 완료: {_get_callback_id(callback.callback)} "
            f"(실행 시간: {execution_time:.3f}초)"
        )
    except Exception as e:
        logger.error(f"콜백 실행 중 오류 발생: {e}\n{traceback.format_exc()}")
        _stats.error_counts["execute_callback"] = _stats.error_counts.get("execute_callback", 0) + 1

async def receive_signal_async(
    signal_name: str,
    callback: Optional[Callable] = None,
    sender: Optional[str] = None,
    filter_condition: Optional[Callable[[Any], bool]] = None
) -> NoReturn:
    """
    시그널을 비동기적으로 수신합니다.
    
    Args:
        signal_name (str): 수신할 시그널 이름
        callback (Optional[Callable]): 시그널 수신 시 실행할 콜백
        sender (Optional[str]): 시그널 발신자
        filter_condition (Optional[Callable]): 추가 필터 조건
    """
    if callback is not None:
        register_callback(signal_name, callback, sender, SignalPriority.NORMAL, filter_condition)
    
    try:
        with _state_lock:
            if _is_shutting_down:
                return
                
        while True:
            with _state_lock:
                if _is_shutting_down:
                    break
                    
            try:
                with _queue_lock:
                    signal_data = _signal_queue.get_nowait()
                    signal_name, data, signal_sender, priority = signal_data
                    
                with _callback_lock:
                    if signal_name in _signal_callbacks:
                        for callback in _signal_callbacks[signal_name]:
                            if (sender is None or callback.sender == sender) and \
                               (callback.filter_condition is None or callback.filter_condition(data)):
                                await _execute_callback(callback, data)
                                if callback.stop_propagation:
                                    break
                                    
            except Empty:
                pass
            except asyncio.CancelledError:
                logger.debug("시그널 수신 태스크가 취소되었습니다.")
                return
            except Exception as e:
                logger.error(f"시그널 수신 중 오류 발생: {e}\n{traceback.format_exc()}")
                
            await asyncio.sleep(0.1)
            
    finally:
        if callback is not None:
            unregister_callback(signal_name, callback)

@_safe_operation
def receive_signal(
    signal_name: str,
    callback: Optional[Callable] = None,
    sender: Optional[str] = None,
    filter_condition: Optional[Callable[[Any], bool]] = None
) -> bool:
    """
    시그널을 수신합니다.
    
    Args:
        signal_name (str): 수신할 시그널 이름
        callback (Optional[Callable]): 시그널 수신 시 실행할 콜백
        sender (Optional[str]): 시그널 발신자
        filter_condition (Optional[Callable]): 추가 필터 조건
        
    Returns:
        bool: 콜백이 없는 경우에만 사용되며, 시그널을 받았으면 True
    """
    if not _initialized:
        _initialize()
        
    global _event_loop, _running_tasks
    
    if callback is not None:
        try:
            # 이벤트 루프가 없거나 종료된 경우 새로 생성
            with _loop_lock:
                if _event_loop is None or _event_loop.is_closed():
                    _event_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(_event_loop)
            
            # 비동기 태스크 시작
            with _loop_lock:
                task = _event_loop.create_task(receive_signal_async(signal_name, callback, sender, filter_condition))
            with _task_lock:
                _running_tasks.add(task)
            return True
            
        except Exception as e:
            logger.error(f"시그널 등록 중 오류 발생: {e}\n{traceback.format_exc()}")
            return False
    
    # 콜백이 없는 경우 기존 동기 처리
    with _lock:
        try:
            with _signal_lock:
                if not _signal_received:
                    return False
                    
                if sender is None or _signal_sender == sender:
                    result = _signal_received
                    _signal_received = False
                    return result
                
                return False
                
        except Exception as e:
            logger.error(f"시그널 확인 중 오류 발생: {e}\n{traceback.format_exc()}")
            return False

@_safe_operation
def wait_for_signals() -> bool:
    """
    모든 시그널 처리가 완료될 때까지 대기합니다.
    
    Returns:
        bool: 모든 시그널이 성공적으로 처리되었으면 True, 아니면 False
    """
    if not _initialized:
        _initialize()
        
    global _event_loop, _running_tasks
    with _loop_lock:
        if _event_loop is not None and _running_tasks:
            try:
                # 모든 시그널이 처리될 때까지 대기
                if not _event_loop.is_running():
                    _event_loop.run_until_complete(asyncio.sleep(0.5))
                
                # 실행 중인 태스크 취소
                with _task_lock:
                    for task in _running_tasks:
                        if not task.done():
                            task.cancel()
                            try:
                                if not _event_loop.is_running():
                                    _event_loop.run_until_complete(task)
                            except asyncio.CancelledError:
                                pass
                            except Exception as e:
                                logger.error(f"태스크 취소 중 오류 발생: {e}\n{traceback.format_exc()}")
                
                # 이벤트 루프 종료
                if not _event_loop.is_closed():
                    try:
                        if not _event_loop.is_running():
                            _event_loop.stop()
                        _event_loop.close()
                    except Exception as e:
                        logger.error(f"이벤트 루프 종료 중 오류 발생: {e}\n{traceback.format_exc()}")
                
                _event_loop = None
                with _task_lock:
                    _running_tasks.clear()
                
                # 상태 초기화
                _initialize()
                return True
            except Exception as e:
                logger.error(f"시그널 대기 중 오류 발생: {e}\n{traceback.format_exc()}")
                # 오류 발생 시에도 리소스 정리
                _initialize()
                return False
    return True

def _get_callback_id(callback: Callable) -> str:
    """콜백 함수의 고유 ID를 생성합니다."""
    return f"{callback.__module__}.{callback.__qualname__}"

@_safe_operation
def register_callback(
    signal_name: str,
    callback: Callable,
    sender: Optional[str] = None,
    priority: SignalPriority = SignalPriority.NORMAL,
    filter_condition: Optional[Callable[[Any], bool]] = None,
    stop_propagation: bool = False
) -> bool:
    """
    시그널에 대한 콜백을 등록합니다.
    
    Args:
        signal_name (str): 시그널 이름
        callback (Callable): 콜백 함수
        sender (Optional[str]): 시그널 발신자
        priority (SignalPriority): 콜백 우선순위
        filter_condition (Optional[Callable]): 추가 필터 조건
        stop_propagation (bool): 시그널 전파 중단 여부
        
    Returns:
        bool: 등록 성공 여부
    """
    if not _initialized:
        _initialize()
        
    try:
        with _callback_lock:
            if signal_name not in _signal_callbacks:
                _signal_callbacks[signal_name] = []
                
            # 중복 등록 방지
            callback_id = _get_callback_id(callback)
            for existing_callback in _signal_callbacks[signal_name]:
                if _get_callback_id(existing_callback.callback) == callback_id:
                    logger.debug(f"콜백이 이미 등록되어 있습니다: {callback_id}")
                    return False
                    
            # 새 콜백 등록
            signal_callback = SignalCallback(
                callback=callback,
                sender=sender,
                priority=priority,
                is_async=asyncio.iscoroutinefunction(callback),
                filter_condition=filter_condition,
                stop_propagation=stop_propagation
            )
            
            _signal_callbacks[signal_name].append(signal_callback)
            # 우선순위에 따라 정렬
            _signal_callbacks[signal_name].sort(key=lambda x: x.priority.value, reverse=True)
            
            logger.debug(f"콜백 등록됨: {callback_id} (시그널: {signal_name}, 우선순위: {priority.name})")
            return True
            
    except Exception as e:
        logger.error(f"콜백 등록 중 오류 발생: {e}\n{traceback.format_exc()}")
        return False

@_safe_operation
def unregister_callback(signal_name: str, callback: Callable) -> bool:
    """
    등록된 콜백을 해제합니다.
    
    Args:
        signal_name (str): 시그널 이름
        callback (Callable): 해제할 콜백 함수
        
    Returns:
        bool: 해제 성공 여부
    """
    if not _initialized:
        _initialize()
        
    try:
        with _callback_lock:
            if signal_name not in _signal_callbacks:
                return False
                
            callback_id = _get_callback_id(callback)
            for i, signal_callback in enumerate(_signal_callbacks[signal_name]):
                if _get_callback_id(signal_callback.callback) == callback_id:
                    _signal_callbacks[signal_name].pop(i)
                    logger.debug(f"콜백 해제됨: {callback_id} (시그널: {signal_name})")
                    return True
                    
            return False
            
    except Exception as e:
        logger.error(f"콜백 해제 중 오류 발생: {e}\n{traceback.format_exc()}")
        return False

@_safe_operation
def unregister_all_callbacks(signal_name: Optional[str] = None) -> bool:
    """
    모든 콜백을 해제합니다.
    
    Args:
        signal_name (Optional[str]): 특정 시그널의 콜백만 해제할 경우 시그널 이름
        
    Returns:
        bool: 해제 성공 여부
    """
    if not _initialized:
        _initialize()
        
    try:
        with _callback_lock:
            if signal_name is not None:
                if signal_name in _signal_callbacks:
                    del _signal_callbacks[signal_name]
                    logger.debug(f"시그널의 모든 콜백 해제됨: {signal_name}")
                    return True
                return False
            else:
                _signal_callbacks.clear()
                logger.debug("모든 시그널의 콜백 해제됨")
                return True
                
    except Exception as e:
        logger.error(f"콜백 일괄 해제 중 오류 발생: {e}\n{traceback.format_exc()}")
        return False

# 초기화
_initialize()