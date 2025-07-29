#!/usr/bin/env python

from string.templatelib import Interpolation, Template

from tstringlogger import get_logger

log = get_logger(__name__)
log.error(Template("this is a ", Interpolation("value", "key", "s", "")))
key = "value"
log.error(t"this is a {key}")
