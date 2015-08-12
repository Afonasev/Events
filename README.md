# Send/subscribe events library

## Requirements

Python >= 3.3

## Getting started

#### Event subscribing:

```python
@events.subscribe('foo')
def foo_handler(count):
    print(count)

def foo_handler_2(count):
    print(count)

events.subscribe('foo', foo_handler_2)
```

#### Event sending:
```python
events.send('foo', count=3)
```

#### Change default registry:
```python
events.set_default_registry(events.EventRegistry(auto_register=False))
```

#### If auto_register is False need register event before using
```python
events.register('foo')
events.send('foo', 3)
```

## License

Events is offered under the MIT license.
