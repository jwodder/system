#!/bin/bash

# This keeps UFW messages from being logged to files other than ufw.log:
sudo sed -i 's/^#& \(~\|stop\)$/\& ~/' /etc/rsyslog.d/20-ufw.conf

sudo sed -i -e '/^#cron\.\*[ \t]\+\/var\/log\/cron.log$/s/^#//' \
            -e '/^#user\.\*[ \t]\+-\/var\/log\/user.log$/s/^#//' \
            /etc/rsyslog.d/50-default.conf

sudo install -d -g syslog -m 0775 /var/log/jwodder

### CREATE /usr/local/bin/authfail ###

sudo tee /etc/rsyslog.d/99-authfail.conf > /dev/null <<'EOT'
module(load="omprog")

if ($syslogfacility-text == "auth" or $syslogfacility-text == "authpriv") and $msg contains "Failed" and $programname == "sshd" then action(type="omprog" binary="/opt/jwodder/bin/authfail" template="RSYSLOG_FileFormat")
EOT

sudo service rsyslog restart
