[ -t 0 ] && mesg n
umask 0022

export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

[ -d "$HOME/bin" ] && export PATH="$PATH:$HOME/bin"
[ -d "$HOME/man" ] && export MANPATH="$MANPATH:$HOME/man"

pyuserbase="$(python -msite --user-base)"
! test "$?" = 0 -a -d "$pyuserbase/bin" || export PATH=$PATH:$pyuserbase/bin

export PAGER=/usr/bin/less
export MANPAGER="$PAGER -is"
export LESS=-iS
export EDITOR=/usr/bin/vim
export VISUAL=$EDITOR

[ -z "$BASH" ] || . ~/.bashrc
