- Put on GitHub (after purging passwords from the repository, of course)

Completeness
============
- Do everything in misc.txt
- Ensure everything in /opt/jwodder is world-readable and (when relevant)
  -executable
- Set up Apache
    - Set up Apache access monitoring
        - If `bin/apachelogs` is changed by the `copy` task, restart Apache
- Configure rsyslog
    - If `bin/authfail` is changed by the `copy` task, restart rsyslog

Structure & Configuration
=========================
- Make the `/var/log/jwodder` path configurable?
    - Alternatively, move it to `{{jwodder_root}}/var/logs`
- Make the `/var/backups/jwodder` path configurable?
    - Rename `/var/backups/jwodder` to `/var/backups/$HOSTNAME`?
- Store host-specific files (domains, PostgreSQL passwords, `software/*`?,
  etc.) in `/opt/jwodder/etc`
    - The following should be configurable via these config files:
        - `dailyreport`:
            - the e-mail address to which dailyreport sends its report
                - Minimize the amount of e-mail mistakenly sent to me
            - `mailbox`
            - `netdevice`
            - `mail_daemon`
        - what `backdroplet` should back up
        - the source & destination address for `xmission-done`
- Place the apache config in a file named `varonathe.org.conf` instead of using
  the default config files
- Install virtualenvs in `/opt/jwodder/virtualenvs`?

Changes & New Features
======================
- Make `backdroplet` exclude files listed in `cruft`
- Don't back up `/root` with `backdroplet`?
- Add a role or playbook that updates all available packages, including forcing
  updates of virtualenvs
- Make dailyreport automatically adjust if Apache isn't installed
- Replace dropboxadd with <https://github.com/andreafabrizi/Dropbox-Uploader>
- Have `apachelogs`, `authfail`, and `maillog` set up & access their DB tables
  using SQLAlchemy
- Set up DNS?
- Split the setup of Google 2FA into a separate role?
- Restrict the `always_set_home` option in `/etc/sudoers` to only apply to
  `pip` & `pip3`?
- Add an option for whether to install jq from source or apt
- Add an option for whether to update jq
- Replace `get_bin_path` with just a call to `which`?
- Don't set up Google Authenticator for root?
- Add an `update_all` variable that, when set (default: false), sets the
  default for all other `update_*` variables and (if true) causes `apt-get
  upgrade` to be run at the beginning of the playbook
- Cron output should still be logged somehow/somewhere even when Postfix isn't
  installed
    - cf. <http://unix.stackexchange.com/q/82093/11006>
    - Use nullmailer? dma? Mailgun?
- Set up root's home directory
- ssl: If the domains in `{{certbot_domains}}` don't match those in the current
  cert(s) in `/etc/letsencrypt`, rerun `/opt/jwodder/bin/certbot`.
- Try to combine `bin/certbot`, `bin/certbot-renew`, and `lib/certbot-common`
  into a single script

- Other packages to consider automatically installing:
    - pwgen
    - tree
    - [devel] pyflakes
