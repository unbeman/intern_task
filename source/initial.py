import logging
import pathlib
from aiohttp import web
import argparse
import pytoml

BASE_DIR = pathlib.Path(__file__).parent.parent


def get_config_from_path(path: str) -> None:
    with open(path) as f:
        config = pytoml.load(f)
    return config


def parse_args(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-c', '--config', dest='config', type=get_config_from_path, help='Path to config file with '
                                                                                         'ini format\n '
                                                                                         'Schema:\n'
                                                                                         '[server_settings]\n'
                                                                                         'host\n'
                                                                                         'port\n'
                                                                                         'log_level - optional'
                                                                                         '[database_settings]\n'
                                                                                         'host\n'
                                                                                         'port\n'
                                                                                         'name\n'
                                                                                         'user\n'
                                                                                         'password\n'
                        )
    return parser.parse_args(argv)


def init_logging(log_level: str) -> None:
    fmt = '%(asctime)s %(levelname)s %(funcName)s L#%(lineno)d: %(message)s'
    logging.basicConfig(format=fmt, level=logging.getLevelName(log_level))


def get_config(argv):
    args = parse_args(argv)
    return args.config


def init_app_settings(app: web.Application, argv) -> None:
    config = get_config(argv)
    server_settings = config['server_settings']
    log_level = server_settings.get('log_level', 'DEBUG')
    init_logging(log_level)
    database_settings = config['database_settings']
    app['host'] = server_settings.get('host')
    app['port'] = int(server_settings.get('port'))
    app['database_settings'] = database_settings
