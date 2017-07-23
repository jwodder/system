- Uncommented the `$SUITE-backports` lines in `/etc/apt/sources.list` (Doable
  with `apt-add-repository`?)
- Work around <https://bugs.mutt.org/trac/ticket/2953> by replacing `source
  /usr/lib/mutt/source-muttrc.d|` in /etc/Muttrc with `source
  /etc/Muttrc.d/$FILE` lines for each file in /etc/Muttrc.d
- Comment out/delete the line `/usr/lib/python2.7/dist-packages` from
  `/usr/local/lib/python2.7/dist-packages/easy-install.pth` so that Python
  2.7's `sys.path` will make sense.  (How did that line even get there in the
  first place???)
- Version 2.2 or higher of bash-completion is needed for tab completion to play
  nicely with failglob.  Until Ubuntu provides such a version, install from
  source as follows:
    - Install the latest release (2.7 at time of writing) from
      <https://github.com/scop/bash-completion>
    - Replace `/etc/profile.d/bash_completion.sh` with a symlink to
      `/usr/local/etc/profile.d/bash_completion.sh`
    - Edit `/etc/bash.bashrc` to change
      `/usr/share/bash-completion/bash_completion` to
      `/usr/local/share/bash-completion/bash_completion`
