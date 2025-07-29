'''
CryptoBob config.
'''

__all__ = (
    'Config',
)

from logging import getLogger

from yaml import safe_load

from .exceptions import ConfigError

LOGGER = getLogger(__name__)


class Config:  # pylint: disable=too-few-public-methods
    '''
    Configuration class of CryptoBob.

    It basically reads the configuration settings from a simple YAML file,
    then stores it internally. The YAML parameters can then be accessed via
    instance attributes. If a parameter wasn't found, an exception is
    raised.
    '''

    @classmethod
    def load(cls, path):
        '''
        Load the configuration file.

        :param pathlib.Path path: The path to the config

        :return: The config instance
        :rtype: Config

        :raises ConfigError: When configuration file is missing or permissions too open
        '''
        LOGGER.debug('Loading configuration from %r', str(path))

        path = path.expanduser()
        loc  = str(path)

        if not path.is_file():
            raise ConfigError(f'Configuration file {loc!r} not found')

        if path.stat().st_mode & 0o77:
            raise ConfigError(f'Configuration file {loc!r} must only be accessible by owner')

        with path.open('r', encoding='utf-8') as file:
            return cls(**safe_load(file))

    def __init__(self, root='', **kwargs):
        self.root = root

        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__dict__[key] = Config(root=f'{root}.{key}', **value)
            else:
                self.__dict__[key] = value

    def __iter__(self):
        return iter(self.__dict__)

    def __getattr__(self, attr):
        '''
        Get attribute method to fetch config instances.

        :return: The config instance
        :rtype: Config

        :raises ConfigError: When configuration file is missing or permissions too open
        '''
        try:
            return self.__dict__[attr]
        except KeyError as ex:
            raise ConfigError(f'Missing configuration property {self.root}.{ex.args[0]}') from ex

    def get(self, attr, default=None):
        '''
        Get a config attribute.

        :param str attr: The attribute
        :param default: The default value when the attribute wasn't found
        :type default: mixed

        :return: The config attribute
        :rtype: mixed
        '''
        return self.__dict__.get(attr, default)

    def as_dict(self):
        '''
        Return config instance as dict.

        :return: Config instance
        :rtype: dict
        '''
        d = self.__dict__.copy()
        del d['root']
        return d
