from   datetime                       import timedelta
from   email.utils                    import localtime
from   prettytable                    import PrettyTable
import sqlalchemy as S
from   sqlalchemy.dialects.postgresql import INET
from   .core                          import longint

### TODO: Is there any reason not to define these at module level?
schema = S.MetaData()

apache_access = S.Table('apache_access', schema,
    S.Column('timestamp',  S.DateTime(timezone=True), nullable=False),
    S.Column('host',       S.Unicode(255),            nullable=False),
    S.Column('port',       S.Integer,                 nullable=False),
    S.Column('src_addr',   INET,                      nullable=False),
    S.Column('authuser',   S.Unicode(255),            nullable=False),
    S.Column('bytesin',    S.Integer,                 nullable=False),
    S.Column('bytesout',   S.Integer,                 nullable=False),
    S.Column('microsecs',  S.BigInteger,              nullable=False),
    S.Column('status',     S.Integer,                 nullable=False),
    S.Column('reqline',    S.Unicode(2048),           nullable=False),
    S.Column('method',     S.Unicode(255),            nullable=False),
    S.Column('path',       S.Unicode(2048),           nullable=False),
    S.Column('protocol',   S.Unicode(255),            nullable=False),
    S.Column('referer',    S.Unicode(2048),           nullable=False),
    S.Column('user_agent', S.Unicode(2048),           nullable=False),
)

class ApacheAccess:
    def __init__(self, engine):
        schema.create_all(engine)
        self.engine = engine
        self.conn = None

    def __enter__(self):
        self.conn = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        return False

    def insert_entry(self, **kwargs):
        self.conn.execute(apache_access.insert().values(kwargs))

    def daily_report(self):
        report = 'Website activity in the past 24 hours:\n'
        tbl = PrettyTable(["Hits", "Request"])
        tbl.align['Hits'] = 'r'
        tbl.align['Request'] = 'l'
        bytesIn = 0
        bytesOut = 0
        for reqline, qty, byin, byout in self.conn.execute(
            S.select([
                apache_access.c.reqline,
                S.func.COUNT('*').label('qty'),
                S.func.SUM(apache_access.c.bytesin),
                S.func.SUM(apache_access.c.bytesout),
            ]).where(apache_access.c.timestamp >= localtime()-timedelta(days=1))
              .group_by(apache_access.c.reqline)
              .order_by(S.desc('qty'), S.asc(apache_access.c.reqline))
        ):
            tbl.add_row([qty, reqline])
            bytesIn  += byin
            bytesOut += byout
        report += tbl.get_string() + '\n'
        bytesIn  = longint(bytesIn)
        bytesOut = longint(bytesOut)
        width = max(len(bytesIn), len(bytesOut))
        report += 'Total bytes sent:     %*s\n' \
                  'Total bytes received: %*s\n' \
                  % (width, bytesOut, width, bytesIn)
        return report