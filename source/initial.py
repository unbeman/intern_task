from aiohttp import web
import argparse
import configparser


def get_config(path: str) -> None:
    config = configparser.ConfigParser()
    config.read(path)
    return config.__dict__['_sections']


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-c', '--config', dest='config', type=get_config)
    return parser.parse_args()


def init_app_settings(app: web.Application):
    config = parse_args().args
    server_settings = config['server_settings']
    app['host'] = server_settings.get('host')
    app['port'] = int(server_settings.get('port'))
