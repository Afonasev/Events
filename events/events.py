import abc
import time
import collections
import concurrent.futures


class IExecutor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def submit(self, callback, *args, **kw):
        pass


class SyncExecutor(IExecutor):

    def submit(self, callback, *args, **kw):
        callback(*args, **kw)


class AsyncExecutor(IExecutor):

    _future2start = {}

    def __init__(self, pool=None):
        self.pool = pool or concurrent.futures.ThreadPoolExecutor(5)

    def submit(self, callback, *args, **kw):
        for future in list(self._future2start):
            if future.running():
                continue

            future.result()
            self._future2start.pop(future)

        future = self.pool.submit(callback, *args, **kw)
        self._future2start[future] = time.time()


class IEventRegistry(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def register(self, event):
        pass

    @abc.abstractmethod
    def send(self, event, msg):
        pass

    @abc.abstractmethod
    def subscribe(self, event, subscriber):
        pass


class EventRegistry(IEventRegistry):

    def __init__(self, executor=None, auto_register=True):
        self.executor = executor or AsyncExecutor()

        if auto_register:
            self.events2subscribers = collections.defaultdict(set)
        else:
            self.events2subscribers = {}

    def register(self, event):
        self.events2subscribers.setdefault(event, set())

    def send(self, event, *args, **kw):
        for subscriber in self.events2subscribers[event]:
            self.executor.submit(subscriber, *args, **kw)

    def subscribe(self, event, subscriber):
        self.events2subscribers[event].add(subscriber)


__default_registry = EventRegistry()


def register(event, registry=None):
    return _or_default(registry).register(event)


def send(event, *args, registry=None, **kw):
    return _or_default(registry).send(event, *args, **kw)


def subscribe(event, subscriber=None, registry=None):
    if subscriber is not None:
        return _or_default(registry).subscribe(event, subscriber)

    def decorator(subscriber):
        _or_default(registry).subscribe(event, subscriber)
        return subscriber

    return decorator


def set_default_registry(registry):
    global __default_registry
    __default_registry = registry


def _or_default(registry):
    return registry or __default_registry
