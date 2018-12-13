Control system requirements:

- minimum Ansible version: 2.5

Target system requirements:

- Ubuntu
- minimum Ubuntu version: 18.04
- minimum Python 3 version: 3.5

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

    dropbox_oauth_access_token

`mail` role
-----------

    digitalocean_token

`ssl` role
----------

    certbot_domains
    digitalocean_token
