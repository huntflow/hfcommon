# -*- coding: utf-8 -*-
import re


_PATTERN = r'{{\s?([A-Za-z\.0-9]+)\s?}}'


def render(data, replacers):
    handled_replacers = dict([(k.lower(), v) for k, v in replacers.items()])
    keys = handled_replacers.keys()

    def replacer(matchobj):
        if matchobj.group(1) and matchobj.group(1).lower() in keys:
            return handled_replacers[matchobj.group(1).lower()]
        else:
            return matchobj.group(1)

    return re.sub(_PATTERN, replacer, data)
