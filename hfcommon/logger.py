# -*- coding: utf-8 -*-
import logging

from raven.handlers.logging import SentryHandler
from tornado.log import access_log
from tortik.logger import LOGGER_NAME, RequestIdFilter


def configure_logging(logfile=None, log_format=None, log_level=logging.WARNING, debug=False, sentry_dsn=None):
    log_level = logging.DEBUG if debug else log_level

    handlers = []
    if logfile:
        h = logging.handlers.WatchedFileHandler(logfile)
        h.setFormatter(logging.Formatter(log_format))
        handlers.append(h)
    if sentry_dsn:
        h = SentryHandler(sentry_dsn, level=logging.ERROR)
        handlers.append(h)
    if not handlers:
        return

    for logger in logging.Logger.manager.loggerDict.values():
        if type(logger) != logging.Logger:
            continue

        logger.setLevel(log_level)
        for handler in handlers:
            logger.addHandler(handler)
        if logger.name == LOGGER_NAME:
            logger.addFilter(RequestIdFilter())


def tornado_log_function(handler):
    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error

    request_time = 1000.0 * handler.request.request_time()
    log_method("%s %d %s %.2fms", handler.request.headers.get('X-Request-Id'),
               handler.get_status(), handler._request_summary(), request_time)
