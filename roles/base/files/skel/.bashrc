[ -n "$PS1" ] || return

alias ls='LC_ALL=C.UTF-8 ls'
alias toc='LC_ALL=C.UTF-8 ls -ACF --color'
alias sort='LC_ALL=C.UTF-8 sort'

PS1='\u@\h:\w\$ '
alias shortps="PS1='${PS1/w/W}'"
alias longps="PS1='${PS1/W/w}'"

shopt -s checkwinsize failglob globstar no_empty_cmd_completion
shopt -u progcomp  # Prior to v2.2, bash-completion doesn't work with failglob
set -o ignoreeof -o pipefail

HISTCONTROL=ignoredups
HISTSIZE=1000
HISTFILESIZE=2000

[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

if [ -x /usr/bin/dircolors ]
then if [ -r ~/.dircolors ]
     then eval "$(dircolors -b ~/.dircolors)"
     else eval "$(dircolors -b)"
     fi
fi

function show_exit_status {
    CHILD_ERROR="${?:-0}"
    [ "$CHILD_ERROR" = 0 ] || printf '\033[1;31m[%d]\033[0m\n' "$CHILD_ERROR"
}

PROMPT_COMMAND=show_exit_status

BASH_COMPLETION_COMPAT_DIR=/etc/bash_completion.d
for compfile in /usr/local/share/bash-completion/bash_completion \
                /usr/share/bash-completion/bash_completion \
                /etc/bash_completion
do if test -f "$compfile"; then . "$compfile"; break; fi
done
