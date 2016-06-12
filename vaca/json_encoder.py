import datetime
import json
from sqlalchemy.engine.result import RowProxy


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, RowProxy):
            return list(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
