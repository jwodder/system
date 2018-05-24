from   prettytable                    import PrettyTable
import sqlalchemy as S
from   sqlalchemy.dialects.postgresql import INET
from   .core                          import SchemaConn, one_day_ago

### TODO: Is there any reason not to define these at module level?
schema = S.MetaData()

authfail = S.Table('authfail', schema,
    S.Column('timestamp', S.DateTime(timezone=True), nullable=False),
    S.Column('username',  S.Unicode(255), nullable=False),
    S.Column('src_addr',  INET, nullable=False),
)

class Authfail(SchemaConn):
    SCHEMA = schema

    def insert_entry(self, timestamp, username, src_addr):
        self.conn.execute(authfail.insert().values(
            timestamp = timestamp,
            username  = username,
            src_addr  = src_addr,
        ))

    def daily_report(self):
        tbl = PrettyTable(["Attempts", "IP Address"])
        tbl.align['Attempts'] = 'r'
        tbl.align['IP Address'] = 'l'
        for src_addr, qty in self.conn.execute(
            S.select([authfail.c.src_addr, S.func.COUNT('*').label('qty')])
             .where(authfail.c.timestamp >= one_day_ago())
             .group_by(authfail.c.src_addr)
             .order_by(S.desc('qty'), S.asc(authfail.c.src_addr))
        ):
            tbl.add_row([qty, src_addr])
        return 'Failed SSH login attempts in the past 24 hours:\n' + \
            tbl.get_string() + '\n'
