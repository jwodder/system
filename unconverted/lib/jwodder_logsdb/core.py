from   datetime    import timedelta
from   email.utils import localtime
from   pathlib     import Path
import sqlalchemy as S

JWODDER_ROOT = Path(__file__).parents[2]

class SchemaConn:
    def __init__(self, engine):
        self.SCHEMA.create_all(engine)
        self.engine = engine
        self.conn = None

    def __enter__(self):
        self.conn = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        return False


def connect() -> 'Engine':
    dbpass = (JWODDER_ROOT/'etc'/'logger').read_text().strip()
    return S.create_engine(S.engine.url.URL(
        drivername = 'postgresql',
        host       = 'localhost',
        database   = 'logs',
        username   = 'logger',
        password   = dbpass,
    ))

def longint(n):
    n = str(n)
    nl = len(n)
    triples = [n[i:i+3] for i in range(nl % 3, nl, 3)]
    if nl % 3:
        triples = [n[:nl%3]] + triples
    return ' '.join(triples)

def one_day_ago():
    return localtime() - timedelta(days=1)
