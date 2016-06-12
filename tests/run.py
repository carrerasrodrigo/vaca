# -*- coding: utf-8 -*-
import os
import sqlite3
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "vaca"))

from vaca.connection import ConnectionConfig, DbConnection
from vaca.main import Vaca
from vaca import sql


class VacaTest(unittest.TestCase):
    test_path = os.path.dirname(__file__)

    def create_db(self):
        if os.path.isfile('vaca.db'):
            os.remove('vaca.db')

        conn = sqlite3.connect('vaca.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE `user` (
            `id` int(11) NOT NULL,
            `username` varchar(250) NOT NULL DEFAULT ''
        );''')
        c.execute(u'''INSERT INTO user VALUES(0, "batman");''')
        c.execute(u'''INSERT INTO user VALUES(1, "luke");''')
        c.execute(u'''INSERT INTO user VALUES(2, "leía");''')
        c.execute(u'''INSERT INTO user VALUES(2, "á´b´d");''')
        conn.commit()

    def setUp(self):
        self.create_db()

        to_clean = ['VACA_CONNECTION_CONFIG']
        for k in to_clean:
            if k in os.environ:
                del os.environ['VACA_CONNECTION_CONFIG']

        to_delete = ['csv.test', 'json.test', 'text.test']
        for k in to_delete:
            if os.path.isfile(k):
                os.remove(k)

    def test_load_config(self):
        cc = ConnectionConfig()
        cc.read_config(file_path='config.json')
        config = cc.get_connection_config('default')
        self.assertEqual(config['name'], 'default')

    def test_create_connection(self):
        cc = ConnectionConfig()
        cc.read_config(file_path='config.json')
        config = cc.get_connection_config('default')
        con = DbConnection()
        con.create_connection(config)
        rows = con.run_query('''select * from user limit 1;''')
        self.assertEqual(len(rows), 2)

    def test_connection_db_insert_query(self):
        cc = ConnectionConfig()
        cc.read_config(file_path='config.json')
        config = cc.get_connection_config('default')
        con = DbConnection()
        con.create_connection(config)
        rows = con.run_query('''INSERT INTO user VALUES(2, "chuck norris");''')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], 1)

    def test_connection_db_encoding(self):
        cc = ConnectionConfig()
        cc.read_config(file_path='config.json')
        config = cc.get_connection_config('default')
        con = DbConnection()
        con.create_connection(config)
        rows = con.run_query(u'''select * from user where username="leía"''')
        self.assertEqual(len(rows), 2)

    def test_vaca_get(self):
        v = Vaca(config_file='config.json', connection_name='default')
        rows = v.q('''select * from user limit 1;''').get()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], 'id')
        self.assertEqual(rows[1][0], 0)

    def test_vaca_get_raw(self):
        v = Vaca(config_file='config.json', connection_name='default')
        rows = v.q('''select * from user limit 1;''').get_raw()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], 'batman')

    def test_vaca_get_map(self):
        v = Vaca(config_file='config.json', connection_name='default')
        m = v.q('''select * from user limit 1;''').get_map()
        m = list(m)
        self.assertEqual(len(m), 1)
        self.assertEqual(m[0]['username'], 'batman')

    def test_vaca_transpose(self):
        v = Vaca(config_file='config.json', connection_name='default')
        rows = v.q('''select * from user limit 1;''').transpose()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], 'id')
        self.assertEqual(rows[1][0], 'username')
        self.assertEqual(rows[0][1], 0)
        self.assertEqual(rows[1][1], 'batman')

    def test_vaca_run(self):
        v = Vaca(config_file='config.json', connection_name='default')
        q = v.q('''select * from user limit 1;''').run()
        self.assertEqual(len(q.query_ret), 2)

    def test_vaca_show(self):
        v = Vaca(config_file='config.json', connection_name='default')
        q = v.q('''select * from user limit 1;''').show()
        self.assertEqual(len(q.query_ret), 2)

    def test_vaca_show_encoding(self):
        v = Vaca(config_file='config.json', connection_name='default')
        q = v.q('''select * from user;''').show()
        self.assertEqual(len(q.query_ret), 5)

    def test_vaca_save_as_text(self):
        v = Vaca(config_file='config.json', connection_name='default')
        v.q('''select * from user;''').save_as_text('text.test')
        self.assertTrue(os.path.isfile('text.test'))

    def test_vaca_save_as_json(self):
        v = Vaca(config_file='config.json', connection_name='default')
        v.q('''select * from user;''').save_as_text('json.test')
        self.assertTrue(os.path.isfile('json.test'))

    def test_vaca_save_as_csv(self):
        v = Vaca(config_file='config.json', connection_name='default')
        v.q('''select * from user;''').save_as_text('csv.test')
        self.assertTrue(os.path.isfile('csv.test'))

    def test_query_format(self):
        v = Vaca(config_file='config.json', connection_name='default')
        q = v.q('''select * from user where id={d};''', data=dict(d=1)).run()
        self.assertEqual(len(q.query_ret), 2)


if __name__ == '__main__':
    unittest.main()
