tstringlogger
=============

> [!WARNING]
> This is just an early prototype of an idea based on reading
> [PEP 750](https://peps.python.org/pep-0750/). I might rewrite it, abandon it, or completely delete
> it - do not rely on it in any way.

Adds support for using t-strings in log messages while preserving all interpolated values.

Usage example:
```python
>>> import logging
>>> test1, test2 = "A", "B"
>>>
>>> logging.error(t"{test1=}, {test2}")
ERROR:root:Template(strings=('test1=', ', ', ''), interpolations=(Interpolation...
>>>
>>> import tstringlogger
>>> tstringlogger.enable()  # automatically adds t-string support to stdlib logging
>>>
>>> logging.error(t"{test1=}, {test2}")
ERROR:root:test1='A', B
```

In this example the `LogRecord` that was produced will have the data that was interpolated into the
message available as `record.args`. In the above example the data would be:
`{"test1": "A", "test2": "B"}`
