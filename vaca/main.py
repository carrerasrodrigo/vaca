from vaca.connection import ConnectionConfig, DbConnection
from vaca.query import Query
from vaca.send_mail import send_email as lsend_email


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
