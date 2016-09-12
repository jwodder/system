- Don't store this repository in `/opt/jwodder`; instead, have it always act
  like the target system is remote and install `bin/`, `etc/`, and `lib/` in
  `/opt/jwodder`

- Store host-specific files (domains, PostgreSQL passwords, `software/*`?,
  etc.) in `/opt/jwodder/etc/localhost/` outside of version control
    - The installation procedure should populate this folder with default
      config files, though
    - The following should be configurable via these config files:
        - `dailyreport`:
            - the e-mail address to which dailyreport sends its report
                - Minimize the amount of e-mail mistakenly sent to me
            - `mailbox`
            - `netdevice`
            - thresholds
        - what `backdroplet` should back up
        - the source & destination address for `xmission-done`
- Put on GitHub (after purging passwords from the repository, of course)
- Make the database-using programs get the DB password from
  `/opt/jwodder/etc/localhost/logger` instead of `/opt/jwodder/etc/logger.json`
- Have `backdroplet` exclude files listed in `cruft`
- Don't back up `/root` with `backdroplet`?
- Rename `/var/backups/jwodder` to `/var/backups/$HOSTNAME`?
- Add a role or playbook that updates all available packages, including forcing
  updates of virtualenvs
- Place the apache config in a file named `varonathe.org.conf` instead of using
  the default config files
- Make dailyreport automatically adjust if Apache isn't installed
- Replace dropboxadd with <https://github.com/andreafabrizi/Dropbox-Uploader>
- Have `apachelogs`, `authfail`, and `maillog` set up & access their DB tables
  using SQLAlchemy

- tmpban system:
    - Add support for IPv6
    - Rewrite to use a `Ban` class
    - Rewrite into a single script?
    - Add a command for listing current bans
    - Give `syncbans` a dry run option
    - Write all activity to a json-seq logfile
    - Give up?
    - Replace with fail2ban?
        - cf. <http://serverfault.com/a/303121/94797>

Ansible
-------
- Do everything in misc.txt
- Ensure everything in /opt/jwodder is world-readable and (when relevant)
  -executable
- Set up Apache
    - Set up Apache access monitoring
- Configure rsyslog
- Set up DNS?
- Set up tmpban
    - Add personal cronjob "0 9 * * * untmpban --auto"
- Split the setup of Google 2FA into a separate role?
- Restrict the `always_set_home` option in `/etc/sudoers` to only apply to
  `pip` & `pip3`?
- Add an option for whether to install jq from source or apt
- Add an option for whether to update jq
- Replace `get_bin_path` with just a call to `which`?
- Don't set up Google Authenticator for root?

- Set up two possible modes of behavior: one for running against localhost,
  another for running against remote hosts
    - The remote mode should install this repository in /opt/jwodder (with the
      synchronize module?), while the local mode should require that it already
      be installed there
- Cron output should still be logged somehow/somewhere even when Postfix isn't
  installed
    - cf. <http://unix.stackexchange.com/q/82093/11006>
    - Use nullmailer? dma? Mailgun?
- Set up root's home directory
- Make the `/opt/jwodder` (and `/var/log/jwodder`? `/var/backups/jwodder`?)
  path configurable
- ssl: If the domains in `/opt/jwodder/etc/localhost/certbot_domains` don't
  match those in the current cert(s) in `/etc/letsencrypt`, rerun
  `/opt/jwodder/bin/certbot`.

- Other packages to consider automatically installing:
    - pwgen
    - tree
