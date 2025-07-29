import time
import sys
import functools
from threading import Thread, Event, Lock
from typing import Callable, Any, Optional, Union, Type




# ================================================== 线程控制器 ==================================================
class ThreadController:
    # 循环定时器控制器(用于停止定时任务)
    def __init__(self):
        self._stopEvent = Event()  # 停止事件标志
        self._thread: Union[Thread, None] = None  # 工作线程引用
        self._value: Any = None  # 存储结果

    # 停止定时循环
    def stop(self):
        self._stopEvent.set()  # 设置停止标志
        if self._thread and self._thread.is_alive(): self._thread.join()  # 等待线程结束

    # 检查定时器是否在运行
    def isRunning(self) -> bool: return not self._stopEvent.is_set()

    # 存储结果
    def result(self) -> Any: return self._value  # 存储结果




# ================================================== 单次定时器 ==================================================
def setTimeout(sleep: float) -> Callable:
    """
    单次定时器装饰器工厂
    :param sleep: 延迟时间(秒)
    :returns: 返回ThreadController对象
    """

    # 校验参数
    if sleep < 0: raise ValueError("延迟时间不能为负数")

    # 定义装饰器
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Union[ThreadController, Any]:
            # 创建控制器对象
            controller = ThreadController()

            # 定义任务函数
            def task():
                try:
                    time.sleep(sleep)
                    if controller.isRunning() is False: return  # 停止事件
                    controller._value = func(*args, **kwargs) # 存储结果
                except Exception as e: print(f"定时任务执行失败: {str(e)}")

            # 启动任务线程
            controller._thread = Thread(target=task)
            controller._thread.start()
            
            # 异步模式返回任务线程对象
            return controller 
        return wrapper
    return decorator




# ================================================== 循环定时器 ==================================================
def setInterval(interval: float, end: float = 0) -> Callable:
    """
    循环定时器装饰器工厂
    :param interval: 执行间隔(秒)
    :param end: 最大持续时间(秒)，0表示无限
    :returns: 返回ThreadController对象
    """

    # 校验参数
    if interval < 0 or end < 0: raise ValueError("时间参数不能为负数")

    # 定义装饰器
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> ThreadController:
            # 创建控制器对象
            controller = ThreadController()
            endstamp = time.time() + end if end > interval else float('inf')  # 计算结束时间戳
            controller._value = []  # 存储结果
            
            # 定义任务函数
            def task():
                while not controller._stopEvent.is_set():
                    controller._stopEvent.wait(max(0, interval))  # 带停止检测的等待
                    if time.time() >= endstamp: break

                    # 执行目标函数
                    try: controller._value.append(func(*args, **kwargs))
                    except Exception as e: print(f"函数：{func.__name__} 定时任务执行失败: {str(e)}")

            # 启动任务线程
            controller._thread = Thread(target=task)
            controller._thread.start()

            # 返回控制器对象
            return controller
        return wrapper
    return decorator




# ================================================== 创建多线程 ==================================================
def createThread(inherit: bool = False) -> Callable:
    """
    创建线程装饰器工厂
    :param inherit: 是否要随着主线程结束而结束
    :returns: 返回ThreadController对象
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> ThreadController:
            # 创建控制器对象
            controller = ThreadController()

            # 创建线程对象
            controller._thread = Thread(target=func, args=args, kwargs=kwargs)
            controller._thread.setDaemon(inherit)  # 设置守护线程
            controller._thread.start()  # 启动线程

            # 返回线程对象
            return controller
        return wrapper
    return decorator




# ================================================== 耗时计算 ==================================================
def timeIt(number: int = 1, show: bool = True) -> Callable:
    """
    耗时统计装饰器工厂
    :param number: 执行次数
    :param show: 是否直接打印耗时信息
    :return: 返回原始结果或(结果, 耗时信息)元组
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> tuple[Callable | None, dict]:
            result = None  # 存储结果
            tempElapsed = []  # 存储耗时

            # 循环执行目标函数
            for _ in range(number):
                start = time.perf_counter()  # 高精度计时开始
                result = func(*args, **kwargs)
                tempElapsed.append(time.perf_counter() - start)   # 计算耗时

            # 计算统计信息
            elapsed = {"avg": sum(tempElapsed) / number}  # 计算平均耗时
            elapsed["min"] = min(tempElapsed)  # 计算最小耗时
            elapsed["max"] = max(tempElapsed)  # 计算最大耗时
            elapsed["sum"] = sum(tempElapsed)  # 计算总耗时
            if number > 1: elapsed["median"] = sorted(tempElapsed)[len(tempElapsed) // 2]  # 计算中位数耗时
            elapsed = {k: f"{v:.5f}" for k, v in elapsed.items()}  # 格式化耗时信息

            # 判断是否显示耗时信息
            if show:
                print(f"函数：{func.__name__} 耗时统计信息:")
                for k, v in elapsed.items(): print(f"{k}: {v}s")

            # 返回结果和耗时
            return result, elapsed
        return wrapper
    return decorator




# ================================================== 异常处理 ==================================================
def catch(
    exceptionToHandle: Union[Type[Exception], Type[Exception]] = Exception,
    defaultValue: Any = None,
    reRaise: bool = False,
    showError: bool = True
) -> Callable:
    """
    异常捕获装饰器工厂
    :param exceptionToHandle: 要捕获的异常类型
    :param defaultValue: 异常发生时返回的默认值
    :param reRaise: 是否重新抛出异常
    :param showError: 是否显示错误信息
    :return: 装饰器函数和默认值
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> tuple[Any, Exception]:
            # 捕获异常并返回默认值
            try: return func(*args, **kwargs)  # 正常执行
            except exceptionToHandle as e:
                if showError: print(f"[异常捕获 {func.__name__}], 错误信息: [{str(e)}]")
                if reRaise: raise # 重新抛出异常开关
                return (defaultValue, e)  # 返回元组

        # 包装后的函数
        return wrapper
    return decorator




# ================================================== 全局异常捕获 ==================================================
def _catchAllErrors(func: Callable, showError: bool = True, defaultValue: Any = None) -> Callable:
    """
    内部实现的全局异常捕获装饰器
    :param func: 需要装饰的目标函数
    :param showError: 是否显示错误信息
    :param defaultValue: 异常发生时返回的默认值
    :return: 装饰器函数和默认值
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try: return func(*args, **kwargs)
        except Exception as e:
            if showError: print(f"[异常捕获 {func.__name__}], 错误信息: [{str(e)}]")
            return (defaultValue, e)
    return wrapper


def catchAll(name: str, error: bool = True, value: Any = None) -> Optional[Exception]:
    """
    模块级全局异常捕获
    :param name: 需要处理的模块名称
    :param error: 是否显示错误信息
    :param value: 异常发生时返回的默认值
    :return: 装饰器函数和默认值
    """
    # 获取模块对象
    targetModule = sys.modules.get(name)
    if not targetModule: raise ValueError(f"找不到模块: {name}")

    # 遍历模块所有成员
    for attrName in dir(targetModule):
        # 获取成员对象
        attr = getattr(targetModule, attrName)

        # 仅处理用户定义的函数
        if callable(attr) and not isinstance(attr, type):
            try:
                # 添加异常捕获装饰器
                wrappedFunc = _catchAllErrors(attr, error, value)
                setattr(targetModule, attrName, wrappedFunc)
            except Exception as e: 
                if error: print(f"处理函数 {attrName} 时发生错误: {str(e)}")
                return e




# ================================================== 调用限制 ==================================================
def callLimit(maxCalls: int = 1, defaultValue: Any = None) -> Callable:
    """
    调用次数限制装饰器工厂(线程安全版)
    :param maxCalls: 最大允许调用次数
    :param defaultValue: 超限后返回值
    """
    def decorator(func: Callable) -> Callable:
        lock = Lock()  # 线程锁
        callCount = 0  # 调用计数器

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            # 保证原子操作
            nonlocal callCount

            # 循环计数器
            with lock:  
                if callCount >= maxCalls: return defaultValue  # 超限
                callCount += 1  # 计数加1

            # 执行目标函数
            return func(*args, **kwargs)
        return wrapper
    return decorator




# ================================================== 失败重试 ==================================================
def retry(
    maxAttempts: int = 3,
    delay: float = 0,
    exceptions: Union[Type[Exception], Type[Exception]] = Exception,
    showError: bool = True
) -> Callable:
    """
    失败重试装饰器工厂
    :param maxAttempts: 最大尝试次数
    :param delay: 重试延迟时间(秒)
    :param exceptions: 要捕获的异常类型
    :param showError: 是否显示错误信息
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @catch(showError = showError)
        def wrapper(*args, **kwargs) -> Callable:
            # 尝试执行目标函数
            for attempt in range(1, maxAttempts + 1):
                # 捕获异常并重试
                try: return func(*args, **kwargs)
                except exceptions as e:
                    if showError: print(f"第 {attempt} 次尝试失败: {str(e)}")
                    if attempt == maxAttempts: raise  # 最后一次尝试失败后抛出异常
                    time.sleep(delay)  # 重试前等待

            return func(*args, **kwargs)  # 最后一次尝试
        return wrapper
    return decorator




# ================================================== 缓存装饰器 ==================================================
def memoize(maxSize: int = 128, ttl: float = 0) -> Callable:
    """
    缓存装饰器工厂(线程安全+TTL支持)
    :param maxSize: 最大缓存条目数 (LRU淘汰)
    :param ttl: 缓存有效期(秒)，0表示永久
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        lock = Lock()
        lruKeys = []  # LRU队列

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            nonlocal lruKeys
            # 生成唯一缓存键(排除self参数)
            key = (args[1:] if args and hasattr(args[0], '__dict__') else args, tuple(sorted(kwargs.items())))
            
            with lock:
                # 检查缓存有效性
                if key in cache:
                    entry = cache[key]
                    if ttl == 0 or time.time() - entry['time'] < ttl:
                        # 更新LRU队列
                        lruKeys.remove(key)
                        lruKeys.append(key)
                        return entry['value']
                    del cache[key]
                    lruKeys.remove(key)

                # 执行函数并缓存结果
                result = func(*args, **kwargs)
                cache[key] = {'value': result, 'time': time.time()}
                lruKeys.append(key)

                # LRU淘汰机制
                if len(cache) > maxSize:
                    delKey = lruKeys.pop(0)
                    del cache[delKey]

                return result
        return wrapper
    return decorator




# ================================================== 速率限制装饰器 ==================================================
class RateLimiter:
    """速率限制控制器"""
    def __init__(self, maxCalls: int, period: float, value: Any):
        self.maxCalls = maxCalls
        self.period = period
        self.value = value
        self.timestamps = []
        self.lock = Lock()

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with self.lock:
                now = time.time()
                # 清除过期时间戳
                self.timestamps = [t for t in self.timestamps if t > now - self.period]
                
                # 检查是否超限
                if len(self.timestamps) >= self.maxCalls: return self.value
                
                # 记录本次调用
                self.timestamps = [t for t in self.timestamps if t > now - self.period]
                self.timestamps.append(now)
            
            return func(*args, **kwargs)
        return wrapper


def rateLimit(maxCalls: int = 1, period: float = 1, value: Any = None) -> RateLimiter:
    """
    速率限制装饰器工厂
    :param maxCalls: 周期内最大调用次数
    :param period: 时间周期(秒)
    """
    return RateLimiter(maxCalls, period, value)

