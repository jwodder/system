- Added myself to the `www-data` group
- Ran:

        sudo chgrp -R www-data /etc/apache2 /var/www
        sudo chmod -R g+wX /etc/apache2 /var/www

        sudo chmod -R o+rX /var/log/apache2

- Added "`ServerName www.varonathe.org`" to `/etc/apache2/apache2.conf`
- Edited `/etc/apache2/sites-available/000-default.conf`
- Added `minsize 512k` and set `rotate 10` in `/etc/logrotate.d/apache2`
- Edited `/etc/apache2/conf-*/other-vhosts-access-log.conf`:
    - Changed the basename of the logfile from `other_vhosts_access.log` to
      `access.log`
    - Added the below line after writing a script `/opt/jwodder/bin/apachelogs`
      for storing log entries in PostgreSQL (also, `mkdir /var/log/jwodder`):

            CustomLog "||/opt/jwodder/bin/apachelogs" "%{%Y-%m-%d %H:%M:%S %z}t|%v|%p|%a|%I|%O|%D|%>s|[\"%u\", \"%r\", \"%m\", \"%U%q\", \"%H\", \"%{Referer}i\", \"%{User-Agent}i\"]"

- Added the following settings to `/etc/apache2/mods-available/ssl.conf`:

        SSLProtocol all -SSLv2 -SSLv3
        SSLHonorCipherOrder on
        SSLCipherSuite "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS"

- `a2enmod ssl`
- `a2enmod rewrite`
- `a2enmod cgi`
- Set `LogLevel` to `info` in `/etc/apache2/apache2.conf` (Needed for fail2ban
  to detect 404's)
