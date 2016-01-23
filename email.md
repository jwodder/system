- Set up SSL certificates
- Add a DNS A record (`mail.varonathe.org`) pointing to the mail server's IP
- Add a DNS MX record pointing to `mail.varonathe.org`
- Open port 25
- `apt-get install postfix postfix-doc postgrey procmail`
    - For postfix, choose "Internet Site" — `debconf-set-selections <<<'postfix
      postfix/main_mailer_type select Internet Site'`
- `service postfix stop`
- Comment out the entries in `/etc/postgrey/whitelist_recipients`
- Install postwhite:

        cd /usr/local
        sudo git clone https://github.com/jsarenik/spf-tools
        sudo git clone https://github.com/stevejenkins/postwhite
        sudo sed -i -e '/^spfttoolspath=/s:=.*:/usr/local/spf-tools:' \
            postwhite/postwhite
        sudo /usr/local/postwhite/postwhite
        printf '%s\n' '#!/bin/bash' \
            '/usr/local/postwhite/postwhite &> /dev/null' \
            | sudo tee /etc/cron.daily/postwhite > /dev/null
        chmod +x /etc/cron.daily/postwhite

- Configure `/etc/postfix/main.cf`
- Configure `/etc/aliases`
- Run `newaliases` to update Postfix's knowledge of `/etc/aliases`
- Create a "`muffins`" user account (belonging to the `mail` group) for dead
  letters
- Added myself to the `mail` group
- Create `/usr/local/bin/maillog` and `/etc/procmailrc`
- Create `/usr/local/bin/mailuser` and give `muffins` a `.procmailrc` for
  using it to sort messages into files with the same name as the recipients'
  "username" (but sanitized and with plus-addresses removed)
- Run:

        for f in maillog.err procmail.err fatal.email
        do sudo touch /var/log/jwodder/$f
           sudo chmod 0666 /var/log/jwodder/$f
        done

- Enable rotating non-jwodder mailboxes:

        mkdir ~/Mail
        echo 'DEFAULT=$HOME/Mail/INBOX' > ~/.procmailrc
        echo 'export MAIL=$HOME/Mail/INBOX' >> ~/.profile
        #mv -i /var/mail/jwodder ~/Mail/INBOX

        sudo install -d -o mail -g mail -m 0775 /var/mail.old

        ### Create /etc/logrotate.d/mailboxes
        sudo chown root:root /etc/logrotate.d/mailboxes
        # ↑ The manpage doesn't address the fact that you need to do this. ↑

- `service postfix start`
