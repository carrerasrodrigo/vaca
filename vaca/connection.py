import json

from sqlalchemy import create_engine
from vaca.utils import get_val


class DbConnection(object):
    def __init__(self):
        self.connection = None

    def get_connection_query(self, db_type, db_name, user, password, host,
            db_options):
        if db_type == 'sqlite':
            return u'sqlite:///{db_name}?{db_options}'.format(db_name=db_name,
                db_options=db_options)
        else:
            return u'{db_type}://{db_user}:{db_password}@{host}/{db_name}' \
                '?{db_options}'.format(
                    db_type=db_type, db_name=db_name, db_user=user,
                    db_password=password, host=host, db_options=db_options)

    def create_connection(self, connection_config):
        cc = connection_config
        conn_query = self.get_connection_query(
            get_val(cc['db_type']),
            get_val(cc['db_name']),
            get_val(cc['db_user']),
            get_val(cc['db_password']),
            get_val(cc['db_host']),
            get_val(cc['db_options']))
        engine = create_engine(conn_query)
        self.connection = engine.connect()

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def run_query(self, query):
        result = self.connection.execute(query)

        rows = []
        if len(result.keys()) > 0:
            rows = [result.keys()] + result.fetchall()
            return rows
        else:
            return [result.rowcount]


class ConnectionConfig(object):
    def __init__(self):
        self.config = None

    def read_config(self, file_path):
        with open(file_path) as f:
            self.config = json.loads(f.read())

    def set_config(self, config):
        self.config = config

    def get_connection_config(self, name=None):
        if self.config is None:
            self.read_config()

        connections = self.config['connections']
        if name is None:
            return connections[0]

        for c in connections:
            if get_val(c['name']) == name:
                return c

        raise Exception('Invalid connection name')

    def get_django_links(self):
        return self.config.get('django', [])
