#!/bin/bash
((EUID == 0)) || exec sudo "$0" "$@"

function installed {
    test "$(dpkg-query -Wf '${db:Status-Abbrev}' "$1" 2>/dev/null)" = "ii "
}

if installed apache2
then service apache2 restart
fi

if installed postfix
then service postfix restart
fi
