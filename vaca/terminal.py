import argparse
import os

from IPython import start_ipython


parser = argparse.ArgumentParser(description="Vaca", add_help=True)
parser.add_argument("--conf", help="The path of the configuration file. If it's not included it will take it from the env variable VACA_CONNECTION_CONFIG", required=False)
parser.add_argument("--connection", help="The name of the default connection that we want to use", required=False)


def start(*args):
    conf = parser.parse_args(args) if len(args) > 0 else parser.parse_args()

    if conf.conf is not None:
        os.environ['VACA_CONNECTION_CONFIG'] = conf.conf

    if conf.connection is not None:
        os.environ['VACA_DEFAULT_CONNECTION'] = conf.connection

    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.environ['PYTHONSTARTUP'] = os.path.join(p, 'vaca', 'ipython_config.py')
    start_ipython([])
