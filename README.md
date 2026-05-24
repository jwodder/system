Control system requirements:

- minimum Ansible version: 13.7

Target system requirements:

- Ubuntu 24.04 or higher
- Python 3.12 or higher must already be installed
- There must already exist a non-root user with sudo powers that the control
  system can SSH in as.  Use this user as the `ansible_user`.
    - It is acceptable for this user to also be the `admin_user`.

Other assumptions made:

- The target system's DNS is managed by DigitalOcean
- The `mail` role assumes that the SSL cert is valid for both `mail_origin` and
  `mail_hostname`
- The `apache` role assumes that the SSL cert is valid for `default_web_domain`
  both with & without leading "www."

Required Variables
==================

`backup` role
-------------

    backup_dropbox_oauth_app_key
    backup_dropbox_oauth_app_secret
    backup_dropbox_oauth_app_refresh_token

`logsdb` role
-------------

    dailyreport_recipient  # if dailyreport enabled

`mail` role
-----------

    digitalocean_token

`ssl` role
----------

    certbot_domains
    certbot_email
    digitalocean_token

`xmission` role
---------------

    xmission_recipient
