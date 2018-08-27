Control system requirements:

- minimum Ansible version: 2.5

Target system requirements:

- Ubuntu
- minimum Ubuntu version: 16.04
- minimum Python 3 version: 3.5

Other assumptions made:

- The target system's DNS is managed by DigitalOcean

Required Variables
==================

`backup` role
-------------

    dropbox_appkey
    dropbox_appsecret
    dropbox_access_level
    dropbox_oauth_access_token
    dropbox_oauth_access_token_secret

`mail` role
-----------

    digitalocean_token
