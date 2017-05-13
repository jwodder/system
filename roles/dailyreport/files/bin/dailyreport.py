#!/usr/bin/python
from   __future__    import division, unicode_literals
import email.charset
from   email.message import Message
from   email.utils   import formataddr
from   errno         import ENOENT
import os
import os.path
import socket
import subprocess
import sys
import time
from   prettytable   import PrettyTable
from   psycopg2      import connect

jwodder_root = os.path.join(os.path.dirname(__file__), os.path.pardir)

credsfile = os.path.join(jwodder_root, 'etc', 'localhost', 'logger')
mailbox = '/home/jwodder/Mail/INBOX'
netdevice = 'eth0'
disk_threshold = 50

mail_daemon = 'MAILER-DAEMON@mail.varonathe.org'

iso8601 = '%Y-%m-%dT%H:%M:%SZ'

tagseq = 'DISK LOGERR REBOOT MAIL'.split()
tagged = set()

with open(credsfile) as fp:
    dbpass = fp.read().strip()
db = connect(host='localhost', database='logs', user='logger', password=dbpass)
cursor = db.cursor()

def longint(n):
    n = str(n)
    nl = len(n)
    triples = [n[i:i+3] for i in xrange(nl % 3, nl, 3)]
    if nl % 3:
        triples = [n[:nl%3]] + triples
    return ' '.join(triples)

def filesize(path):
    try:
        about = os.stat(path)
    except EnvironmentError as e:
        if e.errno == ENOENT:
            return None
        else:
            raise
    return about.st_size

def check_errlogs():
    errlogs = [f for f in os.listdir('/var/log/jwodder')
                 if filesize(os.path.join('/var/log/jwodder', f)) > 0]
    if errlogs:
        tagged.add('LOGERR')
        return 'The following files in /var/log/jwodder are nonempty:\n' + \
               ''.join('    ' + f + '\n' for f in errlogs)

def check_load():
    with open('/proc/loadavg') as fp:
        return 'Load: ' + ', '.join(fp.read().split()[:3]) + '\n'

def check_disk():
    # <http://stackoverflow.com/a/12327880/744178>
    ### TODO: Switch to Python 3.3+ and use `shutil.disk_usage` instead
    usage   = os.statvfs('/')
    fssize  = usage.f_blocks * usage.f_frsize
    #fsavail = usage.f_bavail * usage.f_frsize
    fsavail = usage.f_bfree * usage.f_frsize
    fsused  = fssize - fsavail
    sused   = longint(fsused)
    ssize   = longint(fssize)
    width   = max(len(sused), len(ssize))
    pctused = 100 * fsused / fssize
    if pctused >= disk_threshold:
        tagged.add('DISK')
    return 'Space used on root partition:\n    %*s\n  / %*s\n   (%f%%)\n' \
            % (width, sused, width, ssize, pctused)

def check_authfail():
    cursor.execute('''
        SELECT src_addr, COUNT(*) AS qty FROM authfail
        WHERE timestamp >= (now() - interval '1 day')
        GROUP BY src_addr ORDER BY qty DESC, src_addr ASC
    ''')
    tbl = PrettyTable(["Attempts", "IP Address"])
    tbl.align['Attempts'] = 'r'
    tbl.align['IP Address'] = 'l'
    for addr, qty in cursor.fetchall():
        tbl.add_row([qty, addr])
    return 'Failed SSH login attempts in the past 24 hours:\n' + \
        tbl.get_string() + '\n'

def check_apache_access():
    report = 'Website activity in the past 24 hours:\n'
    cursor.execute('''
        CREATE TEMPORARY TABLE apache_today ON COMMIT DROP
        AS SELECT src_addr, reqline, bytesIn, bytesOut FROM apache_access
           WHERE timestamp >= (now() - interval '1 day')
    ''')
    cursor.execute('''
        SELECT reqline, count(*) AS qty FROM apache_today GROUP BY reqline
        ORDER BY qty DESC, reqline ASC
    ''')
    tbl = PrettyTable(["Hits", "Request"])
    tbl.align['Hits'] = 'r'
    tbl.align['Request'] = 'l'
    for reqline, qty in cursor.fetchall():
        tbl.add_row([qty, reqline])
    report += tbl.get_string() + '\n'
    cursor.execute('SELECT sum(bytesIn), sum(bytesOut) FROM apache_today')
    bytesIn, bytesOut = map(longint, cursor.fetchone())
    width = max(len(bytesIn), len(bytesOut))
    report += 'Total bytes sent:     %*s\n' \
              'Total bytes received: %*s\n' \
              % (width, bytesOut, width, bytesIn)
    return report

def check_inbox():
    title = 'E-mails received in the past 24 hours:'
    cursor.execute('''
        SELECT inbox.id, inbox.subject, inbox_contacts.realname,
               inbox_contacts.email_address, inbox.size, inbox.date
        FROM inbox JOIN inbox_contacts ON inbox.sender = inbox_contacts.id
        WHERE inbox.timestamp >= (now() - interval '1 day')
        ORDER BY inbox.timestamp ASC, inbox.id ASC
    ''')
    inbox = cursor.fetchall()
    if not inbox:
        return title + ' none\n'
    report = title + '\n---\n'
    ### TODO: Handle non-ASCII characters in `dests`
    dests = subprocess.check_output(['postconf', '-hx', 'mydestination'])\
                      .strip().lower().split(', ')
    for mid, sub, sender_name, sender_addr, size, date in inbox:
        cursor.execute('''
            SELECT c.realname, c.email_address
            FROM inbox_tocc AS t JOIN inbox_contacts AS c ON t.contact_id = c.id
            WHERE t.msg_id = %s
                  AND lower(substring(c.email_address
                                      FROM position('@' IN c.email_address)+1))
                      = ANY(%s)
            ORDER BY c.realname ASC, c.email_address ASC
        ''', (mid, dests))
        recips = cursor.fetchall()
        if sys.version_info[0] == 2:
            sub = sub.decode('utf-8')
            sender_name = sender_name.decode('utf-8')
            sender_addr = sender_addr.decode('utf-8')
            recips = [(r.decode('utf-8'), e.decode('utf-8')) for r,e in recips]
        recips = ', '.join(map(formataddr, recips))
        report += 'From:    ' + formataddr((sender_name, sender_addr)) + '\n' \
                  'To:      ' + recips + '\n' \
                  'Subject: ' + sub + '\n' \
                  'Date:    ' + date.strftime(iso8601) + '\n' \
                  'Size:    ' + str(size) + '\n' \
                  '---\n'
    return report

def check_mailbox():
    size = filesize(mailbox)
    if size is not None and size > 0:
        tagged.add('MAIL')

def check_reboot():
    if filesize('/var/run/reboot-required') is not None:
        tagged.add('REBOOT')
        try:
            with open('/var/run/reboot-required.pkgs') as fp:
                pkgs = fp.read().splitlines()
        except IOError:
            pkgs = []
        report = 'Reboot required by the following packages:'
        if pkgs:
            report += '\n' + ''.join('    ' + s + '\n' for s in pkgs)
        else:
            report += ' UNKNOWN\n'
        return report

def check_vnstat():
    vnstat = subprocess.check_output(['vnstat', '--dumpdb', '-i', netdevice])
    yesterday = [s for s in vnstat.splitlines() if s.startswith('d;1;')]
    assert len(yesterday) == 1
    _, _, mrx, mtx, krx, ktx, _ = map(int, yesterday[0].split(';')[1:])
    sent = longint(mtx * 1024 + ktx)
    received = longint(mrx * 1024 + krx)
    width = max(len(sent), len(received))
    return 'Data sent yesterday:     %*s KiB\n' \
           'Data received yesterday: %*s KiB\n' \
           % (width, sent, width, received)

body = ''
for check in [
        check_mailbox,
        check_errlogs,
        check_reboot,
        check_load,
        check_disk,
        check_vnstat,
        check_inbox,
        check_authfail,
        check_apache_access,
    ]:
    report = check()
    if report is not None and report != '':
        if body:
            body += '\n'
        body += report
if not body:
    body = 'Nothing to report\n'

subject = ''
for tag in tagseq:
    if tag in tagged:
        subject += '[' + tag + '] '
        tagged.remove(tag)
for tag in sorted(tagged):
    subject += '[' + tag + '] '
subject += 'Status Report: %s, %s' % (socket.gethostname(),
                                      time.strftime(iso8601, time.gmtime()))

msg = Message()
msg['Subject'] = subject
msg['To'] = 'jwodder@gmail.com'
chrset = email.charset.Charset('utf-8')
chrset.body_encoding = email.charset.QP
msg.set_payload(body, chrset)
msg = str(msg)

if sys.stdout.isatty():
    subprocess.Popen([os.environ.get('PAGER', 'less')], stdin=subprocess.PIPE)\
              .communicate(msg)
else:
    print msg
