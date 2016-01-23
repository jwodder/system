[ -t 0 ] && mesg n
umask 022

export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

[ -d "$HOME/bin" ] && export PATH="$PATH:$HOME/bin"
[ -d "$HOME/man" ] && export MANPATH="$MANPATH:$HOME/man"

export PAGER=/usr/bin/less
export MANPAGER="$PAGER -is"
#export LESSHISTFILE=-
export LESS=-iS
export EDITOR=/usr/bin/vim
export VISUAL=$EDITOR

[ -n "$BASH" ] && . ~/.bashrc
