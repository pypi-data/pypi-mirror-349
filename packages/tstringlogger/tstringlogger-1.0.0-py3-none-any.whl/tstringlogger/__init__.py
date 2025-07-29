#!/usr/bin/env python

"""Use t-strings in log messages"""

import functools
from logging import LogRecord
from string import Formatter
from string.templatelib import Template, Interpolation


_FORMATTER = Formatter()


def _patch_init(func):
    @functools.wraps(func)
    def wrapper(self, name, level, pathname, lineno, msg, args, *args_, **kwargs):
        # When logging a t-string, pull the values out of it and prepend
        # them to any provided args
        if isinstance(msg, Template):
            args = (
                {x.expression: x.value for x in msg if isinstance(x, Interpolation)},
                *args
            )
        return func(self, name, level, pathname, lineno, msg, args, *args_, **kwargs)

    return wrapper


def _patch_getMessage(func):
    @functools.wraps(func)
    def wrapper(self):
        if isinstance(self.msg, Template):
            return "".join(
                (
                    _FORMATTER.format_field(
                        _FORMATTER.convert_field(x.value, x.conversion),
                        x.format_spec
                    )
                ) if isinstance(x, Interpolation)
                else x
                for x in self.msg
            )
        return func(self)
    return wrapper


_enabled = False

def enable():
    """Add support for t-strings to the stdlib logging library"""
    global _enabled
    if _enabled:
        return

    LogRecord.__init__ = _patch_init(LogRecord.__init__)
    LogRecord.getMessage = _patch_getMessage(LogRecord.getMessage)
    _enabled = True
