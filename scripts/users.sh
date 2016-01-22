#!/bin/bash
# Run as root/with sudo

set -ex

apt-get update && apt-get install libpam-google-authenticator
echo auth required pam_google_authenticator.so >> /etc/pam.d/sshd
sed -i 's/^\(ChallengeResponseAuthentication\) no/\1 yes/' \
    /etc/ssh/sshd_config
#yes | google-authenticator

### Uncomment the lines enabling Bash completion in /etc/bash.bashrc

### Set /etc/skel ###

useradd -c 'John T. Wodder II' -d /home/jwodder -m -G adm,staff,sudo,users -U \
    -s /bin/bash jwodder

### Set password?

sudo -u jwodder mkdir /home/jwodder/.ssh
sudo -u jwodder tee -a /home/jwodder/.ssh/authorized_keys > /dev/null \
    < /root/.ssh/authorized_keys
yes | sudo -Hu jwodder google-authenticator

sudo sed -i 's/^\(PermitRootLogin\) yes/\1 no/' /etc/ssh/sshd_config

sudo service ssh restart
