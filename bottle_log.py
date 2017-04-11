import logging
import inspect
import time
import sys

import bottle

DEFAULT_FORMAT = '[%(asctime)s] %(levelname)s: %(name)s: %(message)s'
DEFAULT_LOGLEVEL = 'warning'


class WSGIHandler(logging.Handler):
    def emit(self, record):
        if 'wsgi.errors' in bottle.request.environ:
            try:
                msg = self.format(record).rstrip()
                msg = '{0}\n'.format(msg)
                stream = bottle.request.environ['wsgi.errors']
                stream.write(msg)
                stream.flush()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.handleError(record)


class LoggingPlugin():
    name = 'logging'
    api = 2

    def __init__(self, config, keyword='logger'):
        self.loglevel = getattr(logging, config.get('logging.level', DEFAULT_LOGLEVEL).upper())
        self.logformat = config.get('logging.format', DEFAULT_FORMAT)
        self.logutc = config.get('logging.utc', True)
        self.keyword = keyword
        self.exc_logger = None
        self.logger = None

    def setup(self, app):
        for other in app.plugins:
            if isinstance(other, LoggingPlugin):
                raise bottle.PluginError('Existing LoggingPlugin instance found.')
            elif getattr(other, 'keyword', None) and other.keyword == self.keyword:
                raise bottle.PluginError('Keyword "{0}" conflicts with plugin "{1}".'.format(self.keyword), other.name)
        _setup_root_logger(self.loglevel, self.logformat, self.logutc)
        self.exc_logger = _setup_exc_logger()
        self.logger = _setup_logger(self.loglevel)

    def apply(self, callback, context):
        if (sys.version_info > (3, 0)):
            orig_args = inspect.signature(context.callback).parameters
        else:
            orig_args = inspect.getargspec(context.callback)[0]

        def wrapper(*args, **kwargs):
            if self.keyword in orig_args:
                kwargs[self.keyword] = self.logger
            try:
                return callback(*args, **kwargs)
            except Exception as exc:
                self.exc_logger.exception('An exception occured:')
                raise exc

        return wrapper


def _setup_root_logger(loglevel, logformat, logutc):
    handler = WSGIHandler()
    formatter = logging.Formatter(logformat)
    if logutc:
        formatter.converter = time.gmtime
    handler.setFormatter(formatter)
    logging.basicConfig(level=loglevel, handlers=[handler])


def _setup_exc_logger():
        logger = logging.getLogger('bottle.exception')
        logger.addHandler(logging.NullHandler())
        logger.propagate = False
        logger.setLevel(logging.ERROR)
        return logger


def _setup_logger(loglevel):
        logger = logging.getLogger('bottle')
        logger.setLevel(loglevel)
        return logger
