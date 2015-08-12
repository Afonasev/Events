"""Send/subscribe events library

    import events

    @events.subscribe('foo')
    def foo_handler(count):
        print(count)

    def foo_handler_2(count):
        print(count)

    events.subscribe('foo', foo_handler_2)
    events.send('foo', 3)


    events.set_default_registry(events.EventRegistry(
        auto_register=False,
    ))

    events.register('foo')
    events.send('foo', 3)
"""

from .events import register, send, subscribe, set_default_registry
from .events import IExecutor, SyncExecutor, AsyncExecutor
from .events import IEventRegistry, EventRegistry
