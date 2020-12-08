- Uncommented the `$SUITE-backports` lines in `/etc/apt/sources.list` (Doable
  with `apt-add-repository`?)
    - Already done on DigitalOcean's 20.04 image

- Work around <https://bugs.mutt.org/trac/ticket/2953> by replacing `source
  /usr/lib/mutt/source-muttrc.d|` in `/etc/Muttrc` with `source
  /etc/Muttrc.d/$FILE` lines for each file in `/etc/Muttrc.d`
    - New bug link: <https://gitlab.com/muttmua/trac-tickets/-/blob/master/tickets/open/2953-A_source_command_in_etcMuttrc_prevents_screens_altscreen_fro.txt>

- Uncomment `de_DE.UTF-8 UTF-8` in `/etc/locale.gen` and rerun `locale-gen`

- Comment out the `echo` commands under `"disabled")` in
  `/etc/update-motd.d/80-livepatch`
    - Not a thing anymore on 20.04?

- Run `chmod g-w /usr/local/lib/python3.8` to keep me from running `pip
  install` without `--user`
