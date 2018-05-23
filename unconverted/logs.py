import sqlalchemy as S
from   sqlalchemy.dialects.postgresql import INET

schema = S.MetaData()

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
