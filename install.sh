#!/bin/bash
if ((EUID != 0))
then echo This script must be run as root.
     exit 1
fi

set -ex

if ! command -V ansible-playbook &> /dev/null
then command -V apt-add-repository &> /dev/null || \
         apt-get install -y software-properties-common
     apt-add-repository -y ppa:ansible/ansible
     apt-get update
     apt-get install -y ansible
fi

cd "$(dirname "$0")"
if [ "$(pwd)" != /opt/jwodder ]
then if [ -e /opt/jwodder ]
     then echo "/opt/jwodder already exists, and this isn't it!"
          exit 7
     fi
     mv -i "$(pwd)" /opt/jwodder
     cd /opt/jwodder
fi

cd ansible
ansible-playbook playbook.yml
