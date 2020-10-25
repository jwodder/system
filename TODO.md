- Set admin user's password
- Problem: Since `base` disables root login, and the existence of the `admin`
  role implies that there is initially no non-root account available for login
  (and thus that we're logging in as root the first time the playbook is run),
  the host's SSH details will have to be modified after the first play first
  runs.  In particular, having multiple plays in the playbook will not work out
  well on the first run.
    - In addition, the "synchronize" task in the `base` role doesn't work when
      the `ansible_user` isn't root.
- Require hosts to define a `features: list[str]` variable listing which of the
  optional roles to run
- Give every task a name
- Replace `features` variable with Ansible tags?
- Expand README (Describe what the playbook sets up etc.)
- Set up SPF by adding the following DNS record:
    - Type: `TXT`
    - Name: `@`
    - Data: `v=spf1 mx -all`
    - (Provisions for Mailgun in this record seem to be unnecessary due to
      Mailgun's `Sender:` rewriting making use of the mg.varonathe.org SPF
      entry instead)
- Set admin user's password on creation

Completeness
============
- Do everything in `misc.md`
- Ensure everything in `/opt/jwodder` is world-readable and (when relevant)
  -executable
- PGP-encrypt backups

Structure & Configuration
=========================
- Make the `/var/backups/jwodder` path configurable?
- Store host-specific files (domains, PostgreSQL passwords, etc.) in
  `/opt/jwodder/etc`
    - The following should be configurable via these config files:
        - `dailyreport`:
            - the e-mail address to which dailyreport sends its report
                - Minimize the amount of e-mail mistakenly sent to me
            - `MAILBOX`
            - `NETDEVICE`
        - what `backdroplet` should back up
        - the Dropbox path to which `backdroplet` should upload the backup
        - the source & destination address for `xmission-done`
- Rethink whether having `mail_origin` and `mail_hostname` be different values
  makes sense
- Merge `loginmsg` into `base`?
- Run cronjobs through systemd?

Changes & New Features
======================
- Make `backdroplet` exclude files listed in `cruft`
- Add a role or playbook that updates all available packages
- Add an `update_all` variable that, when set (default: false), sets the
  default for all other `update_*` variables and (if true) causes `apt-get
  upgrade` to be run at the beginning of the playbook
- Set up DNS?
- Cron output should still be logged somehow/somewhere even when Postfix isn't
  installed
    - cf. <http://unix.stackexchange.com/q/82093/11006>
    - Use nullmailer? dma? Mailgun? ssmtp? msmtp?
- Set up root's home directory
    - Use the same files as `/etc/skel`?
- ssl: If the domains in `{{certbot_domains}}` don't match those in the current
  cert(s) in `/etc/letsencrypt`, rerun the Certbot command
- Convey the Google Authenticator details back to the user running Ansible
- Support adding SSH keys to the admin user's `authorized_keys` other than
  those in root's `authorized_keys`
- Automatically regenerate the backup PGP key if it's expired or near
  expiration
- `admin/pydev`: Add options for updating pip and the other Python packages the
  role installs
- `logsdb`: Add an option for recreating the virtualenv
