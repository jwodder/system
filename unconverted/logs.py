import sqlalchemy as S
from   sqlalchemy.dialects.postgresql import INET

schema = S.MetaData()

apache_access = S.Table('apache_access', schema,
    S.Column('timestamp',  S.DateTime(timezone=True), nullable=False),
    S.Column('host',       S.Unicode(255),            nullable=False),
    S.Column('port',       S.Integer,                 nullable=False),
    S.Column('src_addr',   INET,                      nullable=False),
    S.Column('authuser',   S.Unicode(255),            nullable=False),
    S.Column('bytesIn',    S.Integer,                 nullable=False),
    S.Column('bytesOut',   S.Integer,                 nullable=False),
    S.Column('microsecs',  S.BigInteger,              nullable=False),
    S.Column('status',     S.Integer,                 nullable=False),
    S.Column('reqline',    S.Unicode(2048),           nullable=False),
    S.Column('method',     S.Unicode(255),            nullable=False),
    S.Column('path',       S.Unicode(2048),           nullable=False),
    S.Column('protocol',   S.Unicode(255),            nullable=False),
    S.Column('referer',    S.Unicode(2048),           nullable=False),
    S.Column('user_agent', S.Unicode(2048),           nullable=False),
)

authfail = S.Table('authfail', schema,
    S.Column('timestamp', S.DateTime(timezone=True), nullable=False),
    S.Column('username',  S.Unicode(255), nullable=False),
    S.Column('src_addr',  INET, nullable=False),
)

inbox_contacts = S.Table('inbox_contacts', schema,
    S.Column('id',            S.Integer, primary_key=True, nullable=False),
    S.Column('realname',      S.Unicode(2048), nullable=False),
    S.Column('email_address', S.Unicode(2048), nullable=False),
    S.UniqueConstraint('realname', 'email_address'),
)

inbox = S.Table('inbox', schema,
    S.Column('id',        S.Integer, primary_key=True, nullable=False),
    S.Column('timestamp', S.DateTime(timezone=True), nullable=False),
    S.Column('subject',   S.Unicode(2048), nullable=False),
    S.Column('sender',    S.Integer, S.ForeignKey(inbox_contacts.c.id), nullable=False),
    S.Column('size',      S.Integer, nullable=False),
    S.Column('date',      S.DateTime(timezone=True), nullable=False),
)

inbox_tocc = S.Table('inbox_tocc', schema,
    S.Column('msg_id',     S.Integer, S.ForeignKey(inbox.c.id), nullable=False),
    S.Column('contact_id', S.Integer, S.ForeignKey(inbox_contacts.c.id), nullable=False),
    S.UniqueConstraint('msg_id', 'contact_id'),
)
