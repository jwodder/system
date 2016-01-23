#!/bin/bash
set -ex
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt-get update
sudo apt-get install -y ansible

### cd ansible
### ansible-playbook playbook.yml
