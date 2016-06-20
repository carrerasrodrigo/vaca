import os
import sys

from vaca.connection import ConnectionConfig, DbConnection
from vaca.query import Query
from vaca.send_mail import send_email as lsend_email
from vaca.utils import get_val

try:
    import django
    HAS_DJANGO = True
except ImportError:
    HAS_DJANGO = False


class Vaca():
    def __init__(self, config_file=None, config_dict=None,
            connection_name='default'):

        if config_file is not None and config_dict is not None:
            raise Exception('you can use either config_file ot config_dict')

        self.conn = DbConnection()
        self.conn_config = ConnectionConfig()
        if config_dict is not None:
            self.conn_config.set_config(config_dict)
        elif config_file is not None:
            self.conn_config.read_config(config_file)

        config = self.conn_config.get_connection_config(connection_name)
        self.conn.create_connection(config)

        self._load_django_conf(self.conn_config.get_django_links())

    def _load_django_conf(self, paths):
        for p in paths:
            self.link_django_app(get_val(p))

    def change_connection(self, connection_name):
        config = self.conn_config.get_connection_config(connection_name)
        self.conn.create_connection(config)

    def q(self, *args, **kwargs):
        return Query(connection=self.conn, *args, **kwargs)

    def send_email(self, sfrom, to, subject, body, cc=[], bcc=[], files=[],
            smtp_config=None):
        if smtp_config is None:
            smtp_config = self.conn_config.config['smtp']
        lsend_email(sfrom, to, subject, body, cc, bcc, files, **smtp_config)

    def link_django_app(self, project_settings_path):
        if not HAS_DJANGO:
            raise ImportError('please install django')

        if project_settings_path.endswith('.py'):
            project_settings_path = project_settings_path[:-3]

        abs_path = os.path.abspath(project_settings_path)
        settings_path = '.'.join(abs_path.split(os.sep)[-2:])
        sys.path.append(os.sep.join(abs_path.split(os.sep)[:-2]))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_path)
        django.setup()
