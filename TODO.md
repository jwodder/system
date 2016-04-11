- Store host-specific files (domains, PostgreSQL passwords, `software/*`?,
  etc.) in `/opt/jwodder/etc/localhost/` outside of version control
- Apply changed configurations back to firefly
- Put on GitHub (after purging passwords from the repository, of course)
    - Make the `dailyreport` recipient address configurable in such a way as to
      minimize the amount of e-mail mistakenly sent to me
- Have `backdroplet` exclude files listed in `cruft`
- Make the e-mail passed to `letsencrypt` configurable
- Add a host-specific config file for specifying what `backdroplet` should back
  up
- Rename `/var/backups/jwodder` to `/var/backups/$HOSTNAME`?
- Add a role for setting up Transmission:
    - Install `transmission-daemon` and `transmission-cli`
    - Configure `/etc/transmission-daemon/settings.json` (cf.
      `settings.json.orig`)
    - Create `/usr/local/bin/xmission-done`
    - Open port 60069 (both TCP and UDP?)
    - To keep Transmission from starting on system startup: Ensure
      `/etc/init/transmission-daemon.override` exists and contains the line
      "`manual`"
    - `sudo service transmission-daemon reload`
- Add a role or playbook that updates all available packages, including forcing
  updates of virtualenvs
- On Xenial+, install letsencrypt and/or docker-compose via apt-get?
- Place the apache config in a file named `varonathe.org.conf` instead of using
  the default config files
- Make dailyreport automatically adjust if Apache isn't installed

- tmpban system:
    - Add support for IPv6
    - Rewrite to use a `Ban` class
    - Rewrite into a single script?
    - Add a command for listing current bans
    - Give `syncbans` a dry run option
    - Write all activity to a json-seq logfile
    - Replace with something based on <http://serverfault.com/a/303121/94797>?
    - Give up?

Ansible
-------
- Do everything in misc.txt
- Ensure everything in /opt/jwodder is world-readable and (when relevant)
  -executable
- Set up Apache
    - Set up Apache access monitoring
- Configure rsyslog
- Handle setting up /opt/jwodder/etc/domains
    - Set up DNS?
    - Use the presence of /opt/jwodder/etc/domains to determine whether or not
      to run the SSL role?
- Set up tmpban
    - Add personal cronjob "0 9 * * * untmpban --auto"
- ssl: Add flags to letsencrypt-auto for automatically accepting the user
  agreement
- Split the setup of Google 2FA into a separate role?
- Restrict the `always_set_home` option in `/etc/sudoers` to only apply to
  `pip` & `pip3`?
- Merge all of the roles into one, thereby ensuring that things are always run
  in the correct order and allowing features to be toggled via variables?

- Set up two possible modes of behavior: one for running against localhost,
  another for running against remote hosts
    - The remote mode should install this repository in /opt/jwodder (with the
      synchronize module?), while the local mode should require that it already
      be installed there
- Cron output should still be logged somehow/somewhere even when Postfix isn't
  installed
    - cf. <http://unix.stackexchange.com/q/82093/11006>
- Set up root's home directory
- Set up the admin user's home directory with home.git?
- Make the `/opt/jwodder` (and `/var/log/jwodder`? `/var/backups/jwodder`?)
  path configurable

- ssl: If the domains in /opt/jwodder/etc/domains don't match those in the
  current cert(s) in /etc/letsencrypt, rerun /opt/jwodder/bin/letsencrypt.
- Add an option for installing dropbox "normally" rather than in a virtualenv?
- devel: Install jq, with an option for controlling whether to install from
  source or apt
- Other packages to consider automatically installing:
    - apt-file
    - pwgen
    - tree
