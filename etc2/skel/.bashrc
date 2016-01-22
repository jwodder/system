case $- in
    *i*) ;;
      *) return;;
esac

alias ls='LC_ALL=C ls'
alias toc='ls -ACF --color'

PreS1='\u@\h:'
PS1="$PreS1\w\\$ "
alias shortPrompt="PS1='$PreS1\W\\\$ '"
alias longPrompt="PS1='$PreS1\w\\\$ '"

shopt -s checkwinsize failglob globstar no_empty_cmd_completion
shopt -u progcomp
set -o ignoreeof

HISTCONTROL=ignoredups
#HISTSIZE=1000
#HISTFILESIZE=2000

[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

if [ -x /usr/bin/dircolors ]
then if [ -r ~/.dircolors ]
     then eval "$(dircolors -b ~/.dircolors)" 
     else eval "$(dircolors -b)"
     fi
fi
