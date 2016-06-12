import csv
import json

from tabulate import tabulate
from vaca.json_encoder import DateTimeEncoder


class Query(object):
    def __init__(self, query='', connection=None):
        self.query = query
        self.query_ret = None
        self.connection = connection

    def _render_table(self):
        return tabulate(self.query_result, headers='firstrow',
            tablefmt='fancy_grid')

    def __str__(self):
        return self._render_table().encode('utf-8')

    def __unicode__(self):
        return self._render_table()

    @property
    def query_result(self):
        if self.query_ret is None:
            self.run()
        return self.query_ret

    def run(self):
        result = self.connection.run_query(self.query)
        self.query_ret = result
        return self

    def get(self):
        return self.query_result

    def get_raw(self):
        return self.get()[1:]

    def get_map(self):
        header = self.query_result[0]
        body = self.query_result[1:]

        for row in body:
            d = {}
            for i in range(len(header)):
                d[header[i]] = row[i]
            yield d

    def show(self):
        print(self._render_table())
        return self

    def transpose(self):
        return zip(*self.query_result)

    def save_as_json(self, name):
        with open(name, 'w') as f:
            f.write(json.dumps(self.query_result, cls=DateTimeEncoder))
        return self

    def save_as_csv(self, name, cvs_args=[]):
        with open(name, 'wb') as csvfile:
            writer = csv.writer(csvfile, *cvs_args)
            for r in self.query_result:
                writer.writerow(r)
        return self

    def save_as_text(self, name):
        text = self._render_table()

        with open(name, 'w') as f:
            f.write(text.encode('utf-8'))
        return self
