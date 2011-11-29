from django.conf import settings
from django.utils.importlib import import_module


DEFAULT_LOGGED_SETTINGS = [
    'CACHE_BACKEND', 'CACHE_MIDDLEWARE_KEY_PREFIX', 'CACHE_MIDDLEWARE_SECONDS',
    'DATABASES', 'DEBUG', 'DEBUG_LOGGING_CONFIG', 'DEBUG_TOOLBAR_CONFIG',
    'DEBUG_TOOLBAR_PANELS', 'INSTALLED_APPS', 'INTERNAL_IPS',
    'MIDDLEWARE_CLASSES', 'TEMPLATE_CONTEXT_PROCESSORS', 'TEMPLATE_DEBUG',
    'USE_I18N', 'USE_L10N'
]


DEFAULT_CONFIG = {
    'SQL_EXTRA': False,
    'CACHE_EXTRA': False,
    'BLACKLIST': [],
    'LOGGING_HANDLERS': ('debug_logging.handlers.DBHandler',),
    'LOGGED_SETTINGS': DEFAULT_LOGGED_SETTINGS,
}


def _get_logging_config():
    """
    Extend the default config with the values provided in settings.py, and then
    instantiate each of the handlers.
    """
    global _logging_config
    if _logging_config is None:
        _logging_config = dict(DEFAULT_CONFIG,
                               **settings.get('DEBUG_LOGGING_CONFIG', {}))

        handlers = []
        for handler in _logging_config['LOGGING_HANDLERS']:
            if isinstance(handler, Handler):
                handlers.append(handler())
            elif isinstance(handler, basestring):
                i = path.rfind('.')
                module, attr = path[:i], path[i+1:]
                try:
                    mod = import_module(module)
                except ImportError, e:
                    raise ImproperlyConfigured(
                        'Error importing django-debug-logging handler module '
                        '%s: "%s"' % (module, e)
                    )
                try:
                    instance = getattr(mod, attr)
                except AttributeError:
                    raise ImproperlyConfigured(
                        'Module "%s" does not define a "%s" handler class'
                        % (module, attr)
                    )
                handlers.append(instance)
        _logging_config['LOGGING_HANDLERS'] = handlers

    return _logging_config


LOGGING_CONFIG = _get_logging_config()
