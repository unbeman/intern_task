import logging

from aiohttp import web
import argparse
import configparser


def get_config(path: str) -> None:
    config = configparser.ConfigParser()
    config.read(path)
    return config.__dict__['_sections']


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-c', '--config', dest='config', type=get_config, help='Path to config file with ini format\n'
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
    return parser.parse_args()


def init_logging(log_level: str) -> None:
    fmt = '%(asctime)s %(levelname)s %(funcName)s L#%(lineno)d: %(message)s'
    logging.basicConfig(format=fmt, level=logging.getLevelName(log_level))


def init_app_settings(app: web.Application) -> None:
    args = parse_args()
    config = args.config
    server_settings = config['server_settings']
    log_level = server_settings.get('log_level', 'INFO')
    init_logging(log_level)
    database_settings = config['database_settings']
    app['host'] = server_settings.get('host')
    app['port'] = int(server_settings.get('port'))
    app['database_settings'] = database_settings
