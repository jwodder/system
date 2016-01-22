#!/bin/bash
# Basic configuration to apply to any & all further servers created
# Run as root/with sudo

set -ex

apt-get update && apt-get install -y \
    apt-transport-https \
    fail2ban \
    git \
    htop \
    software-properties-common \
    unzip \
    zip

# Swapfile:
### NOTE: The amount of built-in RAM can be found by examining the "MemTotal"
### line in /proc/meminfo.
fallocate -l 1988M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
swapon /swapfile

# ufw:
ufw default deny incoming
ufw allow in 22
ufw allow in 80
ufw allow in 443
ufw enable
