from   datetime             import timezone
from   email.headerregistry import Address
from   email.utils          import localtime
import subprocess
import sqlalchemy as S
from   .core                import SchemaConn, one_day_ago

### TODO: Is there any reason not to define these at module level?
schema = S.MetaData()

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

class MailLog(SchemaConn):
    SCHEMA = schema

    def get_contact_id(self, contact):
        cid = self.conn.execute(
            S.select([inbox_contacts.c.id])
             .where(inbox_contacts.c.realname      == contact.display_name)
             .where(inbox_contacts.c.email_address == contact.addr_spec)
        ).scalar()
        if cid is None:
            cid = self.conn.execute(inbox_contacts.insert().values(
                realname      = contact.display_name,
                email_address = contact.addr_spec,
            )).inserted_primary_key[0]
        return cid

    def insert_entry(self, subject, sender, date, recipients, size):
        """
        :type subject: str
        :type sender: email.headerregistry.Address
        :type date: datetime.datetime
        :type recipients: Iterable[email.headerregistry.Address]
        :type size: int
        """
        with self.conn.begin():
            sid = self.get_contact_id(sender)
            recips = set(map(self.get_contact_id, recipients))
            mid = self.conn.execute(inbox.insert().values(
                timestamp = localtime(),
                subject   = subject[:2048],
                sender    = sid,
                size      = size,
                date      = date,
            )).inserted_primary_key[0]
            self.conn.execute(
                inbox_tocc.insert(),
                [{"msg_id": mid, "contact_id": r} for r in recips],
            )

    def daily_report(self):
        title = 'E-mails received in the past 24 hours:'
        newmail = self.conn.execute(
            S.select([
                inbox.c.id,
                inbox.c.subject,
                inbox_contacts.c.realname,
                inbox_contacts.c.email_address,
                inbox.c.size,
                inbox.c.date,
            ]).select_from(inbox.join(inbox_contacts))
              .where(inbox.c.timestamp >= one_day_ago())
              .order_by(S.asc(inbox.c.timestamp), S.asc(inbox.c.id))
        ).fetchall()
        if not newmail:
            return title + ' none\n'
        report = title + '\n---\n'
        dests = subprocess.check_output(
            ['postconf', '-hx', 'mydestination'],
            universal_newlines=True,
        ).strip().lower().split(', ')
        for mid, sub, sender_name, sender_addr, size, date in newmail:
            recips = ', '.join(map(formataddr, self.conn.execute(
                S.select([
                    inbox_contacts.c.realname,
                    inbox_contacts.c.email_address,
                ])
                .select_from(inbox_tocc.join(inbox_contacts))
                .where(inbox_tocc.c.msg_id == mid)
                .where(
                    # `split_part` is a PostgreSQL-specific function.  Ignoring
                    # the case of addresses without a '@', the standard SQL
                    # equivalent is something like:
                    #
                    #   lower(substring(
                    #       email_address FROM position('@' IN email_address)+1
                    #   )) IN ($dests)
                    S.func.split_part(inbox_contacts.c.email_address, '@', 2)
                     .in_(dests)
                )
                .order_by(
                    S.asc(inbox_contacts.c.realname),
                    S.asc(inbox_contacts.c.email_address),
                )
            )))
            report += (
                'From:    {}\n'
                'To:      {}\n'
                'Subject: {}\n'
                'Date:    {}\n'
                'Size:    {}\n'
                '---\n'
            ).format(
                formataddr((sender_name, sender_addr)),
                recips,
                sub,
                date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                size,
            )
        return report


def formataddr(addr):
    # email.utils.formataddr performs an undesirable encoding of non-ASCII
    # characters
    realname, address = addr
    return str(Address(realname, addr_spec=address))
